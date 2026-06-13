# filepath: src/tests/test_clarifier_contracts.py

"""Canon-coupling + foundations tests for the clarifier (BOM §1–§2).

The version-pin test is HARD: registry drift against the catalog doc fails CI.
The code-literal scan is ADVISORY: it warns, never fails (BOM §2).
"""

import re
import warnings

import pytest
from pydantic import ValidationError

from config import PROJECT_ROOT
from db.models import ClarifierRun, DetectionRecord, DraftStatus, Task, TaskDraft, User
from schemas.clarifier import (
    CardDiff,
    CardPayload,
    EntryResult,
    LLMOutput,
    NormalizedSlots,
    build_task_create,
)
from services import clarifier_registry as registry

CATALOG_PATH = PROJECT_ROOT / "devdocs" / "task_consumer_catalog.md"


# --- canon coupling (the spine) ---


def test_catalog_version_pin_hard():
    """HARD: the registry's pinned version must equal the catalog doc's
    status-line version. A catalog edit without a registry review (or vice
    versa) fails here — drift becomes CI failure, not silent divergence."""
    text = CATALOG_PATH.read_text(encoding="utf-8")
    m = re.search(r"\*\*Status:\*\* canonical · v(\d+\.\d+)", text)
    assert m, "catalog status line not found — did the doc's header format change?"
    assert m.group(1) == registry.CATALOG_VERSION, (
        f"canon drift: catalog doc is v{m.group(1)} but registry pins "
        f"v{registry.CATALOG_VERSION} — review the registry against the "
        "catalog's version note, then bump CATALOG_VERSION."
    )


def test_registry_mirrors_catalog_inventory():
    """20 entries, 4 classes, unique codes, valid enums — catalog v1.3 §3/§4
    (CJ-C5 joined composition at the ToS-posture ratification)."""
    entries = registry.entries_in_order()
    assert len(entries) == 20
    codes = [e.code for e in entries]
    assert len(set(codes)) == 20
    by_class = {k: len(registry.entries_for_class(k)) for k in registry.CLASS_ORDER}
    assert by_class == {"channel": 4, "kind": 4, "instance": 7, "composition": 5}
    for e in entries:
        assert e.klass in registry.CLASS_ORDER
        assert e.severity in (registry.GATE, registry.CLARIFY, registry.WARN)
        assert e.executor in (registry.CODE, registry.LLM, registry.CODE_LLM)
        assert e.version >= 1
        assert e.source


def test_severity_template_legality():
    """Catalog §2.2: gates must carry a decline; clarifies a proposal or
    question (or transform); warns a warn_note. Repairable gates carry a
    transform (the repair preview)."""
    for e in registry.entries_in_order():
        keys = set(e.templates)
        if e.severity == registry.GATE:
            assert "decline" in keys, e.code
            assert e.repairable is not None, f"{e.code}: gates declare repairable"
            if e.repairable:
                assert "transform" in keys, f"{e.code}: repairable gate needs a repair preview"
            assert "warn_note" not in keys, e.code
        elif e.severity == registry.CLARIFY:
            assert keys & {"proposal", "question", "transform"}, e.code
            assert "decline" not in keys and "warn_note" not in keys, e.code
            assert e.repairable is None, e.code
        else:  # WARN
            assert "warn_note" in keys, e.code
            # A warn entry may carry a decline ONLY via a declared escalation
            # rule (catalog §2.1; v1: CJ-X1's warn->gate).
            if "decline" in keys:
                assert e.escalation, f"{e.code}: decline on a warn needs a declared escalation"


def test_declared_exceptions_are_singular():
    """Catalog §2.1: exactly one escalation rule (CJ-X1) and one declared
    override (CJ-I7) exist at v1."""
    entries = registry.entries_in_order()
    assert [e.code for e in entries if e.escalation] == ["CJ-X1"]
    assert [e.code for e in entries if e.override] == ["CJ-I7"]


def test_unknown_code_tolerance():
    """Future catalog entries need no migration; old readers never raise."""
    assert registry.lookup("CJ-Z9") is None
    assert registry.lookup("CJ-I7") is not None


def test_tos_matrix_dispositions():
    """ToS matrix v1 (ratified 2026-06-12): row -> disposition, kill-switch
    gates instantly, unknown/None warn-and-log (never silently allow)."""
    assert registry.tos_disposition("engagement") == "warn"
    assert registry.tos_disposition("public_review") == "gate"
    assert registry.tos_disposition("spam") == "gate"
    assert registry.tos_disposition("political") == "hold"
    assert registry.tos_disposition("fraud_adjacent") == "gate"
    assert registry.tos_disposition("neutral") == "allow"
    assert registry.tos_disposition("unknown") == "warn"
    assert registry.tos_disposition(None) == "warn"
    assert registry.tos_disposition("something-new") == "warn"
    # incident kill-switch: a killed row gates regardless of its normal value
    assert registry.tos_disposition("engagement", killed_rows=["engagement"]) == "gate"


def test_code_literal_scan_advisory():
    """ADVISORY: entry-code literals belong in the registry (and tests).
    Offenders elsewhere produce a warning, never a failure (BOM §2)."""
    allowed = {"clarifier_registry.py"}
    pattern = re.compile(r"CJ-[XKIC]\d")
    offenders = []
    src = PROJECT_ROOT / "src"
    for path in src.rglob("*.py"):
        if path.name in allowed or "tests" in path.parts or "migrations" in path.parts:
            continue
        if pattern.search(path.read_text(encoding="utf-8")):
            offenders.append(str(path.relative_to(PROJECT_ROOT)))
    if offenders:
        warnings.warn(
            "entry-code literals outside the registry (advisory): "
            + ", ".join(offenders),
            stacklevel=1,
        )


# --- §1 foundations: tables + columns ---


def _mk_user(db) -> User:
    u = User(email="clarifier-test@example.com", password_hash="x")
    db.add(u)
    db.flush()
    return u


def test_draft_run_record_roundtrip(db_session):
    db = db_session
    u = _mk_user(db)
    draft = TaskDraft(owner_id=u.id, payload={"desc": "like my photos"})
    db.add(draft)
    db.flush()
    assert draft.status == DraftStatus.CLARIFYING.value

    run = ClarifierRun(
        draft_id=draft.id,
        submission_hash="a" * 64,
        catalog_version=registry.CATALOG_VERSION,
        backend="mock",
        llm_output={"results": []},
        card_payload={"archetype": "clarify"},
        normalized_slots={"actions": ["like the 3 most recent photos"]},
    )
    db.add(run)
    db.flush()

    rec = DetectionRecord(
        run_id=run.id,
        code="CJ-I7",
        entry_version=1,
        result="fired",
        severity_at_fire="clarify",
        response_shown={"transform": "split into 2 tasks"},
    )
    db.add(rec)
    db.commit()

    loaded = db.get(TaskDraft, draft.id)
    assert loaded.runs[0].detections[0].code == "CJ-I7"
    # Resolutions are updated post-run (catalog §2.6).
    loaded.runs[0].detections[0].resolution = "override"
    db.commit()
    assert db.get(DetectionRecord, rec.id).resolution == "override"


def test_run_idempotency_unique_constraint(db_session):
    """(draft_id, submission_hash) unique — the cached-run guarantee's
    DB-level backstop (catalog §2.5)."""
    from sqlalchemy.exc import IntegrityError

    db = db_session
    u = _mk_user(db)
    draft = TaskDraft(owner_id=u.id, payload={"desc": "x"})
    db.add(draft)
    db.flush()
    def _run() -> ClarifierRun:
        return ClarifierRun(
            draft_id=draft.id, submission_hash="h1", catalog_version="1.2", backend="mock"
        )

    db.add(_run())
    db.commit()
    db.add(_run())
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_task_carries_output_contract_columns(db_session):
    """tasks.normalized_slots + clarifier_run_id exist and persist (catalog §6)."""
    db = db_session
    u = _mk_user(db)
    t = Task(
        owner_id=u.id,
        desc="like the 3 most recent photos",
        total_budget=10,
        you_earn=1,
        num_jumpers=10,
        normalized_slots={"actions": ["like"], "end_state": "3 filled hearts"},
    )
    db.add(t)
    db.commit()
    assert db.get(Task, t.id).normalized_slots["end_state"] == "3 filled hearts"
    assert db.get(Task, t.id).clarifier_run_id is None


# --- §2 wire contracts ---


def test_llm_output_roundtrip():
    out = LLMOutput(
        catalog_version=registry.CATALOG_VERSION,
        results=[
            EntryResult(code="CJ-I1", result="fired", evidence="goal vague",
                        proposed_value="more visible engagement"),
            EntryResult(code="CJ-K1", result="clear"),
        ],
        slots=NormalizedSlots(actions=["like the 3 most recent photos"]),
        restatement="Like the 3 most recent photos on ⟨target⟩ until all 3 show a filled heart.",
    )
    again = LLMOutput.model_validate(out.model_dump())
    assert again.results[0].proposed_value == "more visible engagement"
    # "not-evaluated" is a legal RESULT VALUE (runner-set; suppression rows
    # must round-trip through the same schema).
    EntryResult(code="CJ-X3", result="not-evaluated")


def test_card_diff_consent_rule():
    """Replacement diffs must carry the Launcher's original (catalog §5.2 —
    the original must be reconstructible from the card alone)."""
    CardDiff(kind="replacement", slot="actions", text="like 3 photos", original="like photos")
    CardDiff(kind="addition", slot="bound", text="one sitting, ~2 min")
    with pytest.raises(ValidationError):
        CardDiff(kind="replacement", slot="actions", text="like 3 photos")


def test_card_payload_shape():
    payload = CardPayload(
        catalog_version=registry.CATALOG_VERSION,
        archetype="clarify",
        header="Here's how I understood your task",
        restatement=[CardDiff(kind="addition", slot="end_state", text="all 3 show a filled heart")],
        items=[],
        cta_locked=True,
    )
    assert CardPayload.model_validate(payload.model_dump()).cta_locked


def test_build_task_create_mapping():
    payload = {"desc": "like my 3 photos", "total_budget": 10, "you_earn": 1, "num_jumpers": 10}
    tc = build_task_create(payload)
    assert tc.num_jumpers == 10
    with pytest.raises(ValidationError):
        # budget must cover payouts — the code executors' field rules re-run
        build_task_create({"desc": "x", "total_budget": 5, "you_earn": 1, "num_jumpers": 10})
