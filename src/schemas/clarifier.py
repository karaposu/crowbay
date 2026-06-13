# filepath: src/schemas/clarifier.py

"""Clarifier wire contracts (BOM §2).

Three boundaries, three shapes:
- LLMOutput   — what any backend (mock or real) must return (catalog §2.4).
- RunResult   — engine -> card composition, internal (catalog §2.3 routing).
- CardPayload — the consent-bearing card the API composes and BOTH clients
                render verbatim; persisted as-shown on the run (catalog §5).

Versioning: every shape carries catalog_version; detection results carry
entry_version — log rows are uninterpretable without them (catalog §2.6).
All marks/chips are platform-neutral semantics; clients map them to their
own widgets (no client markup in the payload).
"""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from schemas.task import TaskCreate

ResultValue = Literal["clear", "fired", "uncertain", "not-evaluated"]
Severity = Literal["gate", "clarify", "warn"]
Archetype = Literal[
    "green",  # all clear -> one-tap receipt
    "clarify",  # marked-up-draft card
    "transform",  # transform-lead card (e.g. the CJ-I7 split)
    "decline_repair",  # repairable gate -> decline + post-repair preview
    "decline",  # unrepairable gate -> renders alone
    "hold",  # CJ-K3 uncertain -> operator look; no card
]


class NormalizedSlots(BaseModel):
    """The task normal form's slots (meta-definition; catalog §2.1/§6).

    actions + end_state are the BINDING PAIR: immutable once a Jumper is
    active. goal is context, never binding. Copied onto tasks.normalized_slots
    at launch — the output contract matching/verification consume.
    """

    goal: str | None = None
    target: str | None = None
    actions: list[str] = Field(default_factory=list)
    end_state: str | None = None
    bound: str | None = None


class EntryResult(BaseModel):
    """One detection entry's judgment (LLM-emitted or code-executed)."""

    code: str
    result: ResultValue
    entry_version: int = 1
    # Why it fired — feeds the rationale line + the calibration log.
    evidence: str | None = None
    # Typed payload per the entry's response shape: a slot fill, candidate
    # end-states, split drafts, a cleaned-text proposal, ...
    proposed_value: dict | list | str | None = None


class LLMOutput(BaseModel):
    """What every clarifier backend returns from the single pass.

    No numeric confidence at v1 — the three-valued result IS the granularity
    (catalog §2.3). Backends never emit "not-evaluated" (runner-set only);
    the engine enforces this.
    """

    catalog_version: str
    results: list[EntryResult]
    slots: NormalizedSlots = Field(default_factory=NormalizedSlots)
    # The normal-form restatement draft ("[Do actions] on [target] until ...").
    restatement: str | None = None
    # ToS matrix v1 row (registry.TOS_CATEGORIES); logged on EVERY run —
    # clear rows included — as matrix-v2 evidence (ratified posture, T5).
    tos_category: str | None = None


class RunResult(BaseModel):
    """Engine output -> card composition input (internal, BOM §2).

    Suppression has already been applied: entries the runner suppressed carry
    result="not-evaluated" and MUST NOT render (catalog §2.5).
    """

    catalog_version: str
    backend: Literal["off", "mock", "real"]
    degraded: bool = False  # backend failure -> code-only run (visible fail-open)
    submission_hash: str
    results: list[EntryResult]
    slots: NormalizedSlots
    restatement: str | None = None
    tos_category: str | None = None
    worst_severity: Severity | None = None
    archetype: Archetype


# --- Card payload (catalog §5.2 zones; platform-neutral) ---

DiffKind = Literal["replacement", "addition", "unchanged"]
ChipKind = Literal["confirm", "select", "keep_original", "override", "action", "escape"]


class CardDiff(BaseModel):
    """One restatement fragment. The Launcher's original must be
    reconstructible from the card alone (consent rule, catalog §5.2)."""

    kind: DiffKind
    slot: str  # which normal-form slot this fragment fills
    text: str
    original: str | None = None  # required when kind="replacement"

    @model_validator(mode="after")
    def _replacement_carries_original(self) -> "CardDiff":
        if self.kind == "replacement" and not self.original:
            raise ValueError("replacement diffs must carry the Launcher's original text")
        return self


class CardChip(BaseModel):
    kind: ChipKind
    entry_code: str
    label: str
    value: dict | list | str | None = None


class CardItem(BaseModel):
    """One fired entry's card presence: question or proposal + chips."""

    entry_code: str
    severity: Severity
    blocking: bool  # counts against the question cap; locks the CTA
    text: str  # the question or proposal line
    rationale: str | None = None  # one line, Launcher-benefit phrasing
    chips: list[CardChip] = Field(default_factory=list)  # always incl. escape


class CardPayload(BaseModel):
    """The card as shown — persisted verbatim on the run (catalog §5.4)."""

    catalog_version: str
    archetype: Archetype
    header: str
    restatement: list[CardDiff] = Field(default_factory=list)
    items: list[CardItem] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    freeze_notice: str | None = None
    preview_line: str | None = None
    cta_locked: bool = True  # unlocks when all blocking items resolve


# --- Consensus snapshot -> TaskCreate (BOM §2) ---


def build_task_create(draft_payload: dict) -> TaskCreate:
    """Validate the draft's payload into the TaskCreate the existing
    launch service consumes (approval path, BOM §6).

    The payload IS TaskCreate-shaped (collected by the unchanged wizard);
    validation re-runs the code executors' field rules (budget coverage
    etc.). The normalized slots do NOT travel through TaskCreate — the
    approval service copies them onto tasks.normalized_slots (+
    clarifier_run_id) after creation, per the catalog §6 output contract.
    """
    return TaskCreate.model_validate(draft_payload)
