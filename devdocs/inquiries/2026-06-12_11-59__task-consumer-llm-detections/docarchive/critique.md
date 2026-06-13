# Critique — Task-Consumer LLM Detections & Scenarios

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/_branch.md` — candidates from `innovation.md` (T1–T17 + assembly) against `sensemaking.md` SV6 and the branch goal.

## Phase 0 — Dimensions (extracted; purpose-fitness weighted)

| # | Dimension | Weight | Extracted from | Success criterion |
|---|---|---|---|---|
| D1 | Commitment faithfulness (rewrite-and-approve; suggestions never silent rejection; never auto-apply) | CRITICAL .20 | user statement, C2, FP2 | no candidate weakens the approval gate or the suggestion shape |
| D2 | Meta-definition fidelity | CRITICAL .175 | C1, C3, C4 | operates the canon without re-deriving/contradicting — **external anchor: devdocs/task_meta_definition.md** |
| D3 | Conversion safety / friction | HIGH .15 | C5, one-card rule | nothing reintroduces interrogation; card stays scannable |
| D4 | Single-pass feasibility & prompt-expressibility | HIGH .125 | Resource anchor | one LLM call, <5s perceived, no lookups — **substance criterion: each candidate expressible as prompt content** |
| D5 | Calibratability | MED .10 | FP3, Strategic | named+versioned entries, case files, log enable per-detection miss rates |
| D6 | Downstream-consumer service | MED .10 | normalizer anchor | contract serves matching / verification / Jumpers / feedback register — **external anchors: matching parse gap; preview endpoint** |
| D7 | Adversarial robustness | MED .075 | C7, Risk | injection, euphemism, conservative policy routing |
| D8 | Scope discipline (project risk) | MED .075 | MQ4, A6 inheritance note | process-layer only; no silent flips of other components' standing decisions |

**Frame-premise test** (candidate space rests on inherited commitments): (i) *the meta-definition's attribute set is right* — what-if-wrong prosecution: detections would misfire systematically; mitigation exists independently (per-detection calibration D5 + the prior finding's monitoring questions); inheritance acceptable and NAMED. (ii) *one-card UX* — challenged in-pipeline (T2's severity inversion). (iii) *consumer-is-LLM* — challenged by Innovation's audit (hybrid refinement). Premises named, independently prosecuted.

## Phase 1 — Landscape

- **Viable:** candidates raising D1–D4 cheaply (most of the marked-up-draft cluster).
- **Dead:** auto-apply anything; lookup-based truth checks; interrogation patterns; warn-severities that block.
- **Boundary:** the deferred trio (risk score, trust signal, duplicate detection) — real value, missing host components.
- **Unexplored (deliberate):** prompt wording, model selection, invocation plumbing — implementation layer, excluded by Layer Commitment.

## Phase 2/3 — Adversarial Evaluation + Verdicts

**T1 — Hybrid consumer + executor field (code|llm)**
- Prosecution (strongest): premature schema bureaucracy — MVP could let the LLM do everything and split later.
- Defense (external anchor): deterministic checks ALREADY run in code today (budget guard re-ask, schema validation, preview warnings); without the field the catalog implicitly orders the LLM to re-do them — creating code-vs-LLM disagreement on the same submission.
- Collision: one enum field vs a class of contradictions. **SURVIVE.**

**T2 — Decline renders alone**
- Prosecution: fragmenting feedback — a Launcher polishes instance details, resubmits, and only THEN hits the gate problem; wasted effort, double interaction.
- Defense: you don't polish an inadmissible task; decline-alone prevents wasted work.
- Collision: prosecution lands a real case — the REPAIRABLE gate (e.g., descope the credential part). **REFINE →** archetype 4 splits: **4a decline-unrepairable (renders alone)**; **4b decline-with-repair-path (may include the post-repair instance preview: "drop the login step and here's the cleaned task…")**. Constructive output folded into the assembly.

**T3 — Choice-chip proposals**
- Prosecution: chips manufacture consent — Launchers tap through the LLM's framing without reading.
- Defense: the diff-style restatement is the consent guard (changes visible), stet exists, typing always available.
- Collision: defense holds. **SURVIVE** (caveat: diff prominence is load-bearing; chips never hide the original).

**T4 — Cross-field composition detections (pay-vs-effort; filter-task coherence)**
- Prosecution: platform second-guessing market pricing is paternalism and annoyance.
- Defense: warn severity ONLY — never blocks; coherence checks are pure error-prevention.
- Collision: **SURVIVE** with warn-severity locked (D1/D3).

**T5 — One-line rule rationales** — prosecution: card bloat; defense: teaches each rule once, capped at one line. **SURVIVE** (cap is the caveat).

**T6 — Stet/override affordance**
- Prosecution: override licenses bad wording — definedness theater.
- Defense: definedness = slot FILLED; override applies only to WORDING proposals where the original also fills the slot; empty slots have nothing to stet — questions can't be overridden away.
- Collision: **SURVIVE** with that scope rule (override ≠ skip).

**T7 — Per-detection case files** (fire/clear/uncertain few-shots) — dual prompt+eval use; substance-probed: expressible directly as prompt content. **SURVIVE.**

**T8 — Detection codes** — trivial, aids logs/eval/explain affordance. **SURVIVE.**

**T9 — Consensus-approval framing** — wording-level, supports D1. **SURVIVE.**

**T10 — Audience preview in the card**
- Prosecution: card overload (D3) — diff + chips + warnings + preview = wall.
- Defense (external anchor): the preview line ALREADY lives on today's confirm card (`POST /tasks/audience-preview` wired into the bot's step-6 summary).
- Collision: **SURVIVE** (layout note: preview is the card's last line).

**T11 — Semantic-intent policy entries with euphemism few-shots**
- Prosecution: semantic judgment yields false positives on legitimate marketing; chilling effect.
- Defense: uncertain → conservative HOLD for human look (at MVP scale the operator IS the review queue), never auto-decline; few-shots narrow the judgment.
- Collision: **SURVIVE** (hold-path dependency named).

**T15 — PII/profanity channel detection** — cheap, Jumper-facing hygiene, clarify/warn severity. **SURVIVE.**

**T16 — Green-channel fast path** — archetype 1 as one-tap receipt; conversion guard. **SURVIVE.**

**T17 — Publish the normal form as a public writing guide** — one doc note; accelerates pre-shaped submissions. **SURVIVE.**

**T12 / T13 / T14 (deferred trio)** — risk-score placeholder; repeat-policy trust signal; duplicate-task detection. Screened: each blocked on a missing host (review queue / trust component / history lookup at consume time). **DEFER** with the revival gates already named in innovation.

**ASSEMBLY — the full catalog architecture**
- Prosecution (user-perspective, strongest): the ask was "main detections and scenarios" — the answer risks drowning the LIST in architecture (executor fields, severity routing, contracts).
- Defense: the altitude was adjudicated at sensemaking (operational catalog); the framework is exactly what makes the list runnable and calibratable; without it the list is prose.
- Collision: prosecution lands a PRESENTATION hit, not a content hit. **SURVIVE with one REFINE requirement: the finding leads with the detection inventory and scenario table; the framework follows.** Ranked #1.

**Specification-gap probe:** who invokes the consumer, with which model — implementation, explicitly deferred by the branch's Layer Commitment (Process now, Structural next). Declared, not silent. Pass.

## Phase 3.5 — Assembly Check

T2-refined (4a/4b) + T16 compose with the archetypes into a clean severity-routed rendering tree: green-channel receipt / batched marked-up card / decline-with-repair-path / decline-alone. Absorbed into the assembly; no new candidate needed.

## Phase 4 — Coverage + Convergence

- **Accumulator:** 17 evaluations; 0 new kills (Innovation's 3 inherited: streaming, wizard-replacement-now, lookup-truth-checks); refinements: T2→4a/4b, assembly→inventory-first presentation; mechanism-independence: **validated** (anchors cited: `devdocs/task_meta_definition.md`, `POST /tasks/audience-preview` + bot step-6 integration, bot inline keyboards, code-side budget guard, matching's raw-statement decision).
- **Coverage:** all SV5 regions evaluated; unexplored regions are implementation-layer by design — not topologically promising for THIS inquiry's question.
- **Convergence:** landscape STABLE; clean SURVIVEs exist.
- **Signal: TERMINATE.** Ranked: 1) Assembly (inventory-first) · 2) T1 hybrid/executor · 3) T2-refined severity routing (4a/4b) · 4) T3 chips · 5) T6 stet · 6) T4 cross-field detections · 7) T7 case files · 8) T11 policy entries · 9) T16 green channel · 10) T10 preview line · 11) T5 rationales · 12) T15 PII/profanity · 13) T8 codes · 14) T9 framing · 15) T17 guide. Deferred: T12, T13, T14.

## Convergence Telemetry

- Dimension coverage: 8/8 applied; every candidate faced the critical pair (D1, D2)
- Adversarial strength: STRONG — the T2 prosecution flipped a design (4a/4b split); the assembly prosecution forced a presentation requirement
- Landscape stability: STABLE
- Clean SURVIVE exists: YES (assembly, post-refinement)
- Failure modes observed: none (2 REFINEs + 3 DEFERs against 15 SURVIVEs; defenses mandatory throughout)
- **Overall: PROCEED**
