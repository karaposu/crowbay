# filepath: src/services/clarifier_registry.py

"""The catalog-as-code registry — the canon-coupling spine (BOM §2).

This module is the ONLY place detection entry codes, severities, executors,
and response templates live in code. It mirrors devdocs/task_consumer_catalog.md
§4; CATALOG_VERSION is pinned against that document's version note by a hard
CI test (test_clarifier_contracts.py). The engine routes by it, the prompt
builder renders from it, and the mock backend derives its rules from it —
three consumers, one source.

Extension convention: adding a catalog entry = adding one Entry here (codes
are strings on detection_records rows — no migration). Readers tolerate
unknown codes (lookup() returns None) so old logs survive future entries.

ToS posture: matrix v1 RATIFIED 2026-06-12 (adopt-all-as-recommended;
devdocs/inquiries/2026-06-12_14-37__tos-posture-decision/finding.md).
CJ-K3 gates public reviews + spam and holds political; CJ-C5 carries the
two-sided disclosure for allowed engagement; every run logs tos_category;
CLARIFIER_TOS_KILLED_ROWS is the per-row kill-switch.
"""

from dataclasses import dataclass, field

CATALOG_VERSION = "1.3"

# ToS-posture matrix v1 (ratified): category -> disposition.
TOS_CATEGORIES = (
    "engagement",  # allow + two-sided disclosure (CJ-C5 warn)
    "public_review",  # gate (CJ-K3; private-feedback repair path)
    "spam",  # gate (CJ-K3)
    "political",  # hold (CJ-K3 uncertain -> operator)
    "fraud_adjacent",  # gate (existing canon: K2/K3/verifiability)
    "neutral",  # allow, no warn
    "unknown",  # warn + log (matrix-v2 calibration data)
)
_TOS_DISPOSITIONS = {
    "engagement": "warn",
    "public_review": "gate",
    "spam": "gate",
    "political": "hold",
    "fraud_adjacent": "gate",
    "neutral": "allow",
    "unknown": "warn",
}


def tos_disposition(category: str | None, killed_rows: list[str] | None = None) -> str:
    """Matrix row -> allow | warn | gate | hold. A killed row (incident
    kill-switch, config) gates instantly regardless of its normal value.
    Unknown/None categories warn+log (never silently allow)."""
    if category is None or category not in _TOS_DISPOSITIONS:
        category = "unknown"
    if killed_rows and category in killed_rows:
        return "gate"
    return _TOS_DISPOSITIONS[category]

# Severities (catalog §2.2)
GATE = "gate"
CLARIFY = "clarify"
WARN = "warn"

# Executors (catalog §2.4)
CODE = "code"
LLM = "llm"
CODE_LLM = "code+llm"

# Results (catalog §2.3) — "not-evaluated" is runner-set, never LLM-emitted.
RESULTS = ("clear", "fired", "uncertain", "not-evaluated")

# Classes in execution order (catalog §2.5).
CLASS_ORDER = ("channel", "kind", "instance", "composition")


@dataclass(frozen=True)
class Entry:
    code: str
    name: str
    klass: str  # channel | kind | instance | composition
    severity: str  # gate | clarify | warn
    executor: str  # code | llm | code+llm
    source: str  # meta-definition attribute, or "new design"
    version: int = 1
    # At most one declared escalation rule (catalog §2.1; v1: only CJ-X1).
    escalation: str | None = None
    # Gates only: repairable -> archetype decline-with-repair-path.
    repairable: bool | None = None
    # Declared keep-option beyond standard stet (v1: only CJ-I7).
    override: str | None = None
    # Response templates; legal keys constrained by severity (catalog §2.2):
    # gate -> decline (+transform when repairable); clarify -> proposal and/or
    # question (+transform); warn -> warn_note. ⟨...⟩ are runtime slots.
    templates: dict[str, str] = field(default_factory=dict)


_ENTRIES: tuple[Entry, ...] = (
    # ---- Channel class (the submission as untrusted input; runs first) ----
    Entry(
        code="CJ-X1", name="instruction-content / injection", klass="channel",
        severity=WARN, executor=LLM, source="new design",
        escalation="warn->gate when the text is primarily steering (no recoverable task)",
        templates={
            "warn_note": "Part of your text reads as instructions to the system, "
                         "not to Jumpers — I treated it as plain task text: ⟨stripped fragment⟩.",
            "decline": "This is mostly instructions to the platform rather than a task "
                       "for Jumpers, so it can't launch as written. Describe what a "
                       "Jumper should do on-screen.",
        },
    ),
    Entry(
        code="CJ-X2", name="language mismatch", klass="channel",
        severity=CLARIFY, executor=LLM, source="new design",
        templates={
            "proposal": "Jumpers matching your filters likely read ⟨language⟩. "
                        "Use this version? ⟨translated draft⟩ (your original is kept).",
            "question": "Your task is written in ⟨detected⟩ but your audience is "
                        "⟨filter⟩ — which language should Jumpers see?",
        },
    ),
    Entry(
        code="CJ-X3", name="degenerate input", klass="channel",
        severity=CLARIFY, executor=CODE_LLM, source="new design",
        templates={
            "question": "Tell me in a sentence or two: what should each Jumper DO, "
                        "WHERE, and what should be VISIBLE on their screen when "
                        "they're done?",
        },
    ),
    Entry(
        code="CJ-X4", name="PII / profanity in task text", klass="channel",
        severity=CLARIFY, executor=LLM, source="new design",
        templates={
            "proposal": "I removed ⟨item⟩ from the public task text — Jumpers don't "
                        "need it to do the work. OK?",
            "question": "Your task shows ⟨item⟩ to every matched Jumper. Intended?",
        },
    ),
    # ---- Kind class (meta-definition Axis 1 gates) ----
    Entry(
        code="CJ-K1", name="non-digital work", klass="kind",
        severity=GATE, executor=LLM, source="digital", repairable=False,
        templates={
            "decline": "Crowdjump tasks happen entirely on-screen — '⟨off-screen "
                       "fragment⟩' happens in the physical world, so this can't "
                       "launch. (rule: digital)",
            "question": "Does this happen entirely on a screen?",
        },
    ),
    Entry(
        code="CJ-K2", name="credential transfer / non-self-contained", klass="kind",
        severity=GATE, executor=LLM, source="self-contained", repairable=True,
        templates={
            "decline": "Jumpers work only from their own accounts — '⟨credential "
                       "fragment⟩' needs yours, so this can't launch as written. "
                       "(rule: self-contained)",
            "transform": "Without that step it works: ⟨post-repair preview⟩. "
                         "Launch the reduced version?",
            "question": "Will Jumpers use only their OWN accounts for every step?",
        },
    ),
    Entry(
        code="CJ-K3", name="policy floor", klass="kind",
        severity=GATE, executor=LLM, source="policy-permissible + ToS matrix v1",
        repairable=True,
        # Uncertain -> HOLD (the sole uncertainty exception, catalog §2.3).
        # v1.3: gates incentivized PUBLIC reviews + spam-at-scale; political/
        # coordinated engagement -> uncertain (hold). Allowed engagement is
        # CJ-C5's territory, never K3's.
        templates={
            "decline": "This asks Jumpers to ⟨restated intent⟩, which is ⟨named "
                       "category⟩ — Crowdjump can't host it. (rule: policy floor)",
            "transform": "Public paid reviews can't carry the legally required "
                         "disclosure — want this as a private-feedback task "
                         "instead? ⟨private-feedback preview⟩",
            "question": "__HOLD__: This one needs a quick human review — usually "
                        "within ⟨SLA⟩.",
        },
    ),
    Entry(
        code="CJ-K4", name="unverifiable in principle", klass="kind",
        severity=GATE, executor=LLM, source="verifiable-in-principle", repairable=True,
        templates={
            "decline": "'⟨fragment⟩' has no on-screen moment a recording could show, "
                       "so it can't be verified. (rule: verifiable-in-principle)",
            "transform": "If what you want is ⟨per-Jumper reading⟩, this works: "
                         "⟨proxy preview⟩.",
            "question": "Is there anything that would show on a Jumper's screen when "
                        "this is achieved?",
        },
    ),
    # ---- Instance class (meta-definition Axis 2, clarification order) ----
    Entry(
        code="CJ-I1", name="goal unclear", klass="instance",
        severity=CLARIFY, executor=LLM, source="goal-clear",
        templates={
            "proposal": "I read this as: you want ⟨inferred goal⟩. Right?",
            "question": "What outcome do you want from this task?",
        },
    ),
    Entry(
        code="CJ-I2", name="target missing / ambiguous", klass="instance",
        severity=CLARIFY, executor=LLM, source="target-identified",
        templates={
            "proposal": "Target: ⟨inferred URL or handle⟩?",
            "question": "Which exact page/profile/app should Jumpers open? Paste the "
                        "link or handle.",
        },
    ),
    Entry(
        code="CJ-I3", name="actions unspecified", klass="instance",
        severity=CLARIFY, executor=LLM, source="actions-specified",
        templates={
            "proposal": "Each Jumper: ⟨derived action list⟩. That's the whole job?",
            "question": "What exactly should each Jumper do, step by step?",
        },
    ),
    Entry(
        code="CJ-I4", name="completion criterion missing", klass="instance",
        severity=CLARIFY, executor=LLM, source="completion-criterion-observable",
        templates={
            "proposal": "Done when: ⟨candidate end-states as chips⟩ — this is what "
                        "Jumpers must prove on recording.",
            "question": "What will be visible on the Jumper's screen when the task "
                        "is complete?",
        },
    ),
    Entry(
        code="CJ-I5", name="not performable", klass="instance",
        severity=CLARIFY, executor=LLM, source="performable",
        templates={
            "proposal": "This needs ⟨requirement⟩ — add it to your audience filters "
                        "so only matching Jumpers see it?",
            "question": "Does this need any special account, skill, or access beyond "
                        "your audience filters?",
        },
    ),
    Entry(
        code="CJ-I6", name="unbounded", klass="instance",
        severity=CLARIFY, executor=LLM, source="bounded",
        templates={
            "proposal": "One sitting, about ⟨estimate⟩ min: ⟨bounded draft⟩?",
            "question": "Can one Jumper finish this in a single sitting? Roughly how "
                        "long?",
        },
    ),
    Entry(
        code="CJ-I7", name="non-atomic (non-unit task)", klass="instance",
        severity=CLARIFY, executor=LLM, source="atomic",
        override="keep_as_one",  # actions slot is filled; bundling is judgment
        templates={
            "transform": "This looks like ⟨N⟩ different jobs. As separate tasks: "
                         "⟨split drafts⟩. You'll set budget & pay per task.",
            "question": "Is this the same single job for every Jumper? If not, split "
                        "into separate tasks.",
        },
    ),
    # ---- Composition class (cross-field) ----
    Entry(
        code="CJ-C1", name="contradiction (desc vs fields)", klass="composition",
        severity=CLARIFY, executor=LLM, source="new design",
        templates={
            "question": "Your text says ⟨desc value⟩ but the task is set up with "
                        "⟨field value⟩ — which is right?",
        },
    ),
    Entry(
        code="CJ-C2", name="over-specification", klass="composition",
        severity=WARN, executor=LLM, source="sufficiency-not-maximization",
        templates={
            "warn_note": "Jumpers may reach ⟨end-state⟩ by any valid path — exact "
                         "clicks aren't enforceable. Keeping just the end-state makes "
                         "verification cleaner.",
        },
    ),
    Entry(
        code="CJ-C3", name="pay-vs-effort mismatch", klass="composition",
        severity=WARN, executor=CODE_LLM, source="new design",
        templates={
            "warn_note": "≈⟨m⟩ min of work for ⟨pay⟩ USDT (~⟨rate⟩/h) — this may "
                         "fill slowly.",
        },
    ),
    Entry(
        code="CJ-C4", name="filter-task coherence", klass="composition",
        severity=WARN, executor=LLM, source="new design",
        templates={
            "warn_note": "⟨filter⟩ audience for a ⟨task language/geo⟩ task — loosen "
                         "the filter, or adjust the task?",
        },
    ),
    Entry(
        code="CJ-C5", name="tos-sensitive category", klass="composition",
        severity=WARN, executor=LLM, source="ToS-posture matrix v1 (ratified 2026-06-12)",
        # The disclosure half of allow-with-honesty: fires on ALLOWED gray rows
        # (engagement, unknown); gated/held rows are CJ-K3's. Uncertain -> treat
        # as fired with tos_category=unknown (this warn IS the consent surface;
        # silent-when-uncertain deliberately does not apply).
        templates={
            "warn_note": "⟨platform⟩'s rules prohibit paid engagement — purges can "
                         "remove results; you're choosing this risk.",
            "jumper_notice": "Doing this may risk your ⟨platform⟩ account.",
        },
    ),
)

REGISTRY: dict[str, Entry] = {e.code: e for e in _ENTRIES}


def lookup(code: str) -> Entry | None:
    """Tolerant lookup: unknown codes return None (never raise).

    Old detection_records rows must stay readable after the catalog grows or
    retires entries (catalog §2.6 / unknown-code tolerance).
    """
    return REGISTRY.get(code)


def entries_in_order() -> list[Entry]:
    """All entries in execution order: channel -> kind -> instance -> composition."""
    rank = {k: i for i, k in enumerate(CLASS_ORDER)}
    return sorted(_ENTRIES, key=lambda e: (rank[e.klass], e.code))


def entries_for_class(klass: str) -> list[Entry]:
    return [e for e in entries_in_order() if e.klass == klass]
