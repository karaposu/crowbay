# filepath: src/services/clarifier.py

"""The clarifier detection engine (BOM §4).

One submission revision -> one recorded ClarifierRun:

    rate cap -> content hash (cached?) -> code executors -> single backend
    pass -> merge (code authoritative) -> suppression -> ToS routing ->
    archetype -> persist run + detection records + draft status.

Field-backed data (budget, slots, pay, deadlines) is NEVER re-asked — the
schema validators own it; the engine only reads it as wizard context.
Routing (catalog §2.3) is data, not if-chains. Suppression rows are
runner-set "not-evaluated" and never render (catalog §2.5).
"""

import hashlib
import json
from datetime import timedelta

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy.orm import Session

from config import settings
from db.base import utcnow
from db.models import ClarifierRun, DetectionRecord, DraftStatus, TaskDraft
from schemas.clarifier import EntryResult, LLMOutput, NormalizedSlots, RunResult
from services import audit
from services import clarifier_registry as registry
from services.clarifier_backend import ClarifierBackendError, get_backend

# --- routing matrix (catalog §2.3) as data ----------------------------------
# (severity, result) -> blocking action. The SOLE per-entry exception is
# CJ-K3 uncertain -> hold (the conservative human look).
ROUTING: dict[tuple[str, str], str] = {
    (registry.GATE, "fired"): "decline",
    (registry.GATE, "uncertain"): "ask",  # an uncertain gate asks, never declines
    (registry.CLARIFY, "fired"): "card",
    (registry.CLARIFY, "uncertain"): "ask",
    (registry.WARN, "fired"): "note",
    (registry.WARN, "uncertain"): "silent",  # warn discipline: wrong warns are noise
}
ROUTING_EXCEPTIONS: dict[tuple[str, str], str] = {
    ("CJ-K3", "uncertain"): "hold",
}

_INSTANCE_LIKE = ("instance", "composition")


def submission_hash(payload: dict) -> str:
    """Canonical content hash — identical submission+context => cached run."""
    relevant = {
        "desc": payload.get("desc", ""),
        "filters": payload.get("filters"),
        "total_budget": payload.get("total_budget"),
        "you_earn": payload.get("you_earn"),
        "num_jumpers": payload.get("num_jumpers"),
    }
    blob = json.dumps(relevant, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def enforce_rate_cap(db: Session, owner_id: int) -> None:
    """Token-abuse guard (BOM §0): runs per user per hour, 429 beyond."""
    cutoff = utcnow() - timedelta(hours=1)
    n = (
        db.query(ClarifierRun)
        .join(TaskDraft, ClarifierRun.draft_id == TaskDraft.id)
        .filter(TaskDraft.owner_id == owner_id, ClarifierRun.created_at >= cutoff)
        .count()
    )
    if n >= settings.CLARIFIER_RUNS_PER_USER_PER_HOUR:
        raise HTTPException(
            http_status.HTTP_429_TOO_MANY_REQUESTS,
            "Clarifier rate cap reached — try again in a bit.",
        )


def _code_executor_results(desc: str) -> dict[str, EntryResult]:
    """Deterministic checks that never reach the LLM (code halves)."""
    out: dict[str, EntryResult] = {}
    if len(desc.strip()) < settings.CLARIFIER_MIN_TASK_CHARS:
        out["CJ-X3"] = EntryResult(
            code="CJ-X3", result="fired",
            evidence=f"desc shorter than {settings.CLARIFIER_MIN_TASK_CHARS} chars",
        )
    return out


def _merge_results(
    llm: LLMOutput | None, code: dict[str, EntryResult], degraded: bool
) -> dict[str, EntryResult]:
    """Every registry entry gets exactly one result row.

    Code is authoritative on its sub-checks; backends must not emit
    "not-evaluated" (runner-set only) — offending rows are coerced to clear
    with an evidence marker. Degraded/off runs mark llm-executor entries
    not-evaluated (honest logging, catalog §2.5)."""
    merged: dict[str, EntryResult] = {}
    llm_by_code = {r.code: r for r in (llm.results if llm else [])}
    for e in registry.entries_in_order():
        r = llm_by_code.get(e.code)
        if r is not None and r.result == "not-evaluated":
            r = EntryResult(code=e.code, result="clear", entry_version=e.version,
                            evidence="backend emitted not-evaluated (coerced)")
        if r is None:
            if (llm is None or degraded) and e.executor != registry.CODE:
                r = EntryResult(code=e.code, result="not-evaluated",
                                entry_version=e.version)
            else:
                r = EntryResult(code=e.code, result="clear", entry_version=e.version)
        merged[e.code] = r
    for code_key, r in code.items():  # code authoritative over llm
        if r.result == "fired":
            merged[code_key] = r
    return merged


def _apply_suppression(merged: dict[str, EntryResult]) -> None:
    """Catalog §2.5 short-circuits — runner-set, never rendered, log-honest."""
    x1 = merged.get("CJ-X1")
    x1_escalated = (
        x1 is not None and x1.result == "fired"
        and isinstance(x1.proposed_value, dict) and x1.proposed_value.get("escalate")
    )
    if x1_escalated:
        for code, r in merged.items():
            if code != "CJ-X1" and r.result != "not-evaluated":
                merged[code] = EntryResult(code=code, result="not-evaluated",
                                           entry_version=r.entry_version)
        return
    if merged.get("CJ-X3") is not None and merged["CJ-X3"].result == "fired":
        for e in registry.entries_in_order():
            if e.klass in _INSTANCE_LIKE:
                prev = merged[e.code]
                merged[e.code] = EntryResult(code=e.code, result="not-evaluated",
                                             entry_version=prev.entry_version)


def _apply_tos_routing(
    merged: dict[str, EntryResult], tos_category: str | None
) -> None:
    """ToS matrix v1 (ratified): the engine enforces the row's disposition
    even when the backend under-fired — incl. the per-row kill-switch."""
    if tos_category is None:
        return
    disposition = registry.tos_disposition(
        tos_category, settings.CLARIFIER_TOS_KILLED_ROWS
    )
    if disposition == "warn" and merged["CJ-C5"].result not in ("fired",):
        merged["CJ-C5"] = EntryResult(code="CJ-C5", result="fired",
                                      evidence=f"tos row: {tos_category} (engine)")
    elif disposition == "gate" and merged["CJ-K3"].result not in ("fired",):
        merged["CJ-K3"] = EntryResult(
            code="CJ-K3", result="fired",
            evidence=f"tos row {tos_category!r} gated"
            + (" by kill-switch" if tos_category in settings.CLARIFIER_TOS_KILLED_ROWS
               else ""),
        )
    elif disposition == "hold" and merged["CJ-K3"].result == "clear":
        merged["CJ-K3"] = EntryResult(code="CJ-K3", result="uncertain",
                                      evidence=f"tos row: {tos_category} (engine)")


def _route(merged: dict[str, EntryResult]) -> tuple[str | None, str]:
    """(worst blocking severity, archetype) per catalog §5.1.

    Warns never block: a warn-only run stays green (receipt + notices)."""
    x1 = merged.get("CJ-X1")
    if (
        x1 is not None and x1.result == "fired"
        and isinstance(x1.proposed_value, dict) and x1.proposed_value.get("escalate")
    ):
        # CJ-X1's declared escalation (warn -> gate): primarily-steering text
        # has no recoverable task — decline alone (catalog §2.1/§4).
        return registry.GATE, "decline"
    k3 = merged.get("CJ-K3")
    if k3 is not None and k3.result == "uncertain":
        if ROUTING_EXCEPTIONS.get(("CJ-K3", "uncertain")) == "hold":
            return registry.GATE, "hold"
    gates_fired = [
        registry.lookup(c) for c, r in merged.items()
        if r.result == "fired" and registry.lookup(c).severity == registry.GATE
    ]
    if gates_fired:
        repairable = any(
            e.repairable and _has_repair(merged[e.code]) for e in gates_fired
        )
        return registry.GATE, "decline_repair" if repairable else "decline"
    i7 = merged.get("CJ-I7")
    if i7 is not None and i7.result == "fired" and _has_repair(i7):
        return registry.CLARIFY, "transform"
    clarifies = [
        c for c, r in merged.items()
        if r.result in ("fired", "uncertain")
        and registry.lookup(c).severity == registry.CLARIFY
        and r.result != "not-evaluated"
    ]
    if clarifies:
        return registry.CLARIFY, "clarify"
    return None, "green"


def _has_repair(r: EntryResult) -> bool:
    return isinstance(r.proposed_value, dict) and (
        "repair" in r.proposed_value or "splits" in r.proposed_value
    )


_STATUS_BY_ARCHETYPE = {
    "hold": DraftStatus.HELD.value,
    "decline": DraftStatus.DECLINED.value,
    "decline_repair": DraftStatus.DECLINED.value,
    "green": DraftStatus.AWAITING_APPROVAL.value,
    "clarify": DraftStatus.AWAITING_APPROVAL.value,
    "transform": DraftStatus.AWAITING_APPROVAL.value,
}


def run_clarifier(
    db: Session, draft: TaskDraft, *, request_id: str | None = None
) -> ClarifierRun:
    """The single pass (BOM §4). Returns the cached run on identical content."""
    enforce_rate_cap(db, draft.owner_id)

    payload = draft.payload or {}
    desc = payload.get("desc", "")
    h = submission_hash(payload)

    cached = (
        db.query(ClarifierRun)
        .filter(ClarifierRun.draft_id == draft.id, ClarifierRun.submission_hash == h)
        .first()
    )
    if cached is not None:
        return cached

    backend = get_backend()
    llm_out: LLMOutput | None = None
    degraded = False
    if backend is not None:
        try:
            llm_out = backend.run(desc, payload)
        except ClarifierBackendError as e:
            degraded = True
            audit.record(
                db, "clarifier.skipped",
                actor_id=draft.owner_id, target_type="task_draft", target_id=draft.id,
                payload={"reason": str(e)[:200]}, request_id=request_id,
            )

    merged = _merge_results(llm_out, _code_executor_results(desc), degraded)
    _apply_suppression(merged)
    tos_category = llm_out.tos_category if llm_out else None
    _apply_tos_routing(merged, tos_category)
    worst, archetype = _route(merged)

    run = ClarifierRun(
        draft_id=draft.id,
        submission_hash=h,
        catalog_version=registry.CATALOG_VERSION,
        backend=settings.CLARIFIER_BACKEND,
        status="degraded" if degraded else "complete",
        llm_output=llm_out.model_dump() if llm_out else None,
        normalized_slots=llm_out.slots.model_dump() if llm_out else None,
        tos_category=tos_category,
    )
    db.add(run)
    db.flush()

    for code, r in merged.items():
        entry = registry.lookup(code)
        fired_ish = r.result in ("fired", "uncertain")
        db.add(DetectionRecord(
            run_id=run.id,
            code=code,
            entry_version=r.entry_version,
            result=r.result,
            severity_at_fire=entry.severity if (entry and fired_ish) else None,
            response_shown=None,  # card composition (§5) fills what rendered
        ))

    draft.status = _STATUS_BY_ARCHETYPE[archetype]
    db.flush()
    return run


def run_result(run: ClarifierRun) -> RunResult:
    """Rehydrate the internal RunResult from a persisted run (for §5)."""
    llm = LLMOutput.model_validate(run.llm_output) if run.llm_output else None
    merged = _merge_results(
        llm, _code_executor_results((run.draft.payload or {}).get("desc", "")),
        run.status == "degraded",
    )
    _apply_suppression(merged)
    _apply_tos_routing(merged, run.tos_category)
    worst, archetype = _route(merged)
    return RunResult(
        catalog_version=run.catalog_version,
        backend=run.backend,  # type: ignore[arg-type]
        degraded=run.status == "degraded",
        submission_hash=run.submission_hash,
        results=list(merged.values()),
        slots=NormalizedSlots.model_validate(run.normalized_slots or {}),
        restatement=llm.restatement if llm else None,
        tos_category=run.tos_category,
        worst_severity=worst,  # type: ignore[arg-type]
        archetype=archetype,  # type: ignore[arg-type]
    )
