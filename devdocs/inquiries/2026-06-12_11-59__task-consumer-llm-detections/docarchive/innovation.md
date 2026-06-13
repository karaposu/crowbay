# Innovation — Task-Consumer LLM Detections & Scenarios

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/_branch.md` — seed inherited via sensemaking SV6 + decomposition P1–P7 (Production-task mode: generate catalog content per piece).

## Seed & Methodology Mode

- **Seed:** design the catalog's content within the SV5 frame (three classes, entry schema, four archetypes, one-card rule, output contract) — a Question+Gap seed.
- **Inherited mode:** Standard default (4G+3F). **Alternative considered:** Generator-weighted exploration (maximize detection breadth) — would yield exotic detections, but the meta-definition bounds the inventory naturally, so breadth has a cap and framing challenges matter more. **Decision: default mode.**
- **Meta-decision pieces:** P1 (schema + severity semantics = evaluation-criterion), P4 (coins composition-detection vocabulary), P5 (one-card framing-semantic), P6 (output-contract commitments) → piece-level Inversion mandatory. P2, P3, P7 = content-production. No intervention-shape commitments (definitional/process artifact) → content-axis Inversions satisfy.

## Phase 2 — Generate (7 mechanisms × generic / focused / contrarian)

### 1. Lens Shifting (Framer)
- **Generic — first-contact lens:** the card is most Launchers' first encounter with platform rules → every fired detection's response carries a one-line rationale ("…so we can verify on-screen and pay instantly"). Detections double as onboarding. (→ T5)
- **Focused — Jumper lens:** the rewrite proposal is not for the Launcher's taste — it IS the Jumper's future instruction card. Acceptance phrasing: "Jumpers will see exactly this." Sharpenss the diff-restatement's purpose.
- **Contrarian — adversarial-Launcher lens:** some will euphemize prohibited intent ("boost visibility" for fake reviews). Policy detections must be semantic-intent judgments with euphemism few-shots, not keyword filters. (→ T11)

### 2. Combination (Generator)
- **Generic:** detection results × the EXISTING audience-preview endpoint → the card shows "as understood, your task currently matches N verified Jumpers" computed from the NORMALIZED location — clarifier and preview close into one loop. (→ T10)
- **Focused:** normal form × TaskCreate → approval submits normalized slots straight into the API payload; MVP seat: post-description enrichment of the existing confirm card; wizard-replacement is post-MVP. 
- **Contrarian:** detection log × trust — Launchers repeatedly firing policy detections accumulate a risk signal. Cross-component. (→ T13, deferred)

### 3. Inversion (Framer; depth-checked)
- **Generic:** "the consumer questions the Launcher" → inverted to system level: the artifact of consumption is a **consensus reading, co-authored** — the card invites correction ("did I get anything wrong?"), approval = consensus snapshot, not interrogation passed. (→ T9)
- **Focused (P5 inversion, required):** "one card batches everything" → first inversion: stream one-by-one (component-level, rejected — interrogation). Inverted again to system level: **interaction granularity should equal severity granularity** — a GATE decline must render ALONE (never buried among proposals); batching is for clarify/warn only. (→ T2; genuine keying refinement)
- **Contrarian:** "detections protect the platform" → "detections protect the LAUNCHER" — every message phrased as Launcher benefit, not compliance-speak. Tone canon. (folds into T5)

### 4. Constraint Manipulation (Framer; ADD + REMOVE both exercised)
- **ADD (generic):** "perceived response <5s" → single pass, no lookups mid-judgment, pre-rendered templates. Kills any browsing/lookup detection; confirms the MVP shape and the text-not-world inheritance.
- **ADD (focused):** "questions answerable by TAP where possible" → proposals as **choice-chips** (e.g., three candidate completion criteria derived from the stated actions; "pick one or type your own"). The bot's inline keyboards already support this. (→ T3)
- **REMOVE (contrarian):** remove "the submission = the desc field" → the consumer reads the WHOLE wizard context → new cross-field composition detections: **pay-vs-effort sanity** (1 USDT for an hour-long task → warn), **filter-task coherence** (German-only audience, English-review task → warn). (→ T4; the strongest new inventory content)

### 5. Absence Recognition (Generator; patch + redesign, bidirectional)
- **Patch-level:** missing channel entries — PII/profanity in task text (Jumper-facing hygiene) (→ T15); duplicate-resubmission detection (needs task-history lookup → conflicts with the single-pass constraint; deferred) (→ T14).
- **Redesign (missing):** a **per-detection case file** — every detection ships with 2–3 canonical examples (fire / clear / uncertain) as first-class content; the prompt AND the eval suite both read it. (→ T7)
- **Redesign (already-present-in-other-form):** the platform ALREADY runs deterministic detections (budget guard re-ask, schema validation, audience-preview warnings). Absent an explicit map, the LLM re-implements (worse) what code does. → **deterministic-first principle: every detection entry declares its executor — `code` or `llm` — and LLM is used only where judgment is irreducible.** (→ feeds T1)

### 6. Domain Transfer (Generator; native source included)
- **Native (software) — linters/compilers:** severity taxonomy, rule CODES (E501-style), `--fix` autofixes, per-rule suppression, "explain rule" affordance → detection codes `CJ-K*/CJ-I*/CJ-C*/CJ-X*` (→ T8), transforms-as-quick-fixes (chips), an "explain" affordance per fired rule.
- **Different — editorial desk:** a copy editor returns ONE marked-up draft with queries in margins; the style book = the meta-definition; **"stet"** = the author overrules a suggestion and the original stands → an explicit **override affordance**: the Launcher may reject a clarify-proposal and keep their wording (logged); approval is not all-or-nothing. (→ T6)
- **Different — customs channels:** red/green channel routing by risk → **green-channel fast path**: a clean submission gets a minimal one-tap receipt card, not a heavy review. Archetype 1 must be nearly frictionless. (→ T16)

### 7. Extrapolation (Generator)
- **Generic:** volume grows → detection results become routing signals (high-risk → human review queue) → log schema carries a risk-score placeholder. (→ T12, deferred)
- **Focused:** models improve → detections migrate from "ask" to "confident proposal"; the uncertainty routing is the dial — entries must support both behaviors WITHOUT rewrite. Confirms the clear/fired/uncertain trichotomy.
- **Contrarian:** Launchers learn → submissions arrive pre-shaped in normal form → the consumer's role drifts repair→receipt; keep archetype 1 cheap (confirmed) and **publish the normal form as a public writing guide** to accelerate the drift. (→ T17)

## Inherited Frame Audit

- **Seed central assumptions:** (a) **"the consumer is an LLM"** (user-given) — scanned: NO candidate challenged it → **audit fires**. Type: Design choice + Belief → Absence-redesign + Inversion applied: *what if the consumer is NOT an LLM — pure deterministic code + forms?* What follows: most field checks survive (they're code today), but slot-extraction from free text, euphemism-reading policy judgment, and rewrite-proposal are irreducibly judgmental. **Refined, not rejected: the consumer is a HYBRID — a deterministic shell plus an LLM judgment core; the catalog's executor field (code|llm) is the boundary made explicit.** (→ T1 absorbed the audit's product.) (b) "single-pass interaction" — challenged by the streaming inversion (refined into T2's decline-alone carve-out). Audit satisfied after one integration cycle.
- Piece commitments: P1 schema challenged (executor field extends it) ✓; P4 composition vocabulary challenged (cross-field detections extend it) ✓; P5 one-card challenged (severity-granularity inversion) ✓; P6 contract challenged (preview integration + risk placeholder) ✓.

## Phase 3 — Test (5-test cycle; dispositions)

| # | Candidate | Verdict notes | Disposition |
|---|---|---|---|
| T1 | Executor field (code\|llm) + deterministic-first principle | survives strongest objection ("schema bloat") — one field prevents the LLM re-doing code checks worse; grounded: budget guard/schema checks exist in code today | **ACTIONABLE** |
| T2 | Decline renders ALONE (severity-granularity interaction) | objection "fragmenting feedback" fails: burying a decline among chips is worse; gates are rare | **ACTIONABLE** |
| T3 | Choice-chip proposals (tap-not-type) | grounded: inline keyboards exist in bot; web client mirrors | **ACTIONABLE** |
| T4 | Cross-field composition detections (pay-vs-effort; filter-task coherence) | objection "paternalism on pricing" → severity=warn only, never blocks | **ACTIONABLE** |
| T5 | One-line rule rationales in responses (Launcher-benefit tone) | costs tokens; teaches once — worth it | **ACTIONABLE** |
| T6 | Override/"stet" affordance on clarify-proposals (logged) | objection "undermines definedness" fails: definedness requires the slot FILLED, not the LLM's wording; original may fill it | **ACTIONABLE** |
| T7 | Per-detection case file (fire/clear/uncertain few-shots) | prompt+eval dual use; mechanism-independent (Absence + linter transfer) | **ACTIONABLE** |
| T8 | Detection codes (CJ-K1…) | trivial, aids log/eval/explain | **ACTIONABLE** |
| T9 | Consensus-reading approval framing ("did I get anything wrong?") | wording-level, cheap | **ACTIONABLE** |
| T10 | Card-integrated audience preview from normalized location | endpoint exists; objection "two features in one card" fails — preview already lives on the confirm card today | **ACTIONABLE** |
| T11 | Semantic-intent policy entries with euphemism few-shots | the only defensible shape for policy floor; conservative-hold bias applies | **ACTIONABLE** |
| T16 | Green-channel fast path (archetype 1 = one-tap receipt) | confirms + sharpens archetype 1 | **ACTIONABLE** |
| T17 | Publish the normal form as a public writing guide | one doc note | **ACTIONABLE** |
| T12 | Risk-score placeholder in log | needs review-queue to mean anything | **DEFERRED** — revival: human-review queue exists |
| T13 | Repeat-policy-fire trust signal | trust component territory | **DEFERRED** — revival: trust score implementation |
| T14 | Duplicate-task detection | requires task-history lookup → breaks single-pass/submission-only purity | **DEFERRED** — revival: spam observed in production |
| K1 | Streaming question-by-question interaction | killed (interrogation, conversion death) — salvage absorbed as T2's decline carve-out | new-seed |
| K2 | Consumer replaces wizard now | killed for MVP (wizard fields are field-backed canon) — preserved as post-MVP note in P6 mapping | new-seed |
| K3 | Lookup-based truth detections (URL exists? account real?) | killed — violates definedness≠truth inheritance and the 5s constraint | reinforces boundary |

**Convergence signal:** 4 mechanisms (linter transfer's marked-up-draft+fixes, ADD-constraint chips, editorial stet, consensus inversion) independently converge on one interaction model: **the card is a marked-up draft with tap-able fixes and override-able queries.** Shared-input check: they arrive from different grounds (tooling pattern / UX constraint / editorial practice / framing inversion) — independent.

**Assembly check:** T1+T2+T3+T5+T6+T16 compose the consumer's interaction architecture: deterministic shell first (code-executor detections), LLM core produces the marked-up draft (diff restatement + chips + rationales), severity-routed rendering (decline alone / green-channel receipt / batched card), override-able proposals, consensus approval. The inventory candidates (T4, T11, T15) populate P2–P4; T7+T8 make every entry calibratable; T10 enriches P6's contract. Axis coverage: executor-axis ✓ severity-axis ✓ interaction-axis ✓ content-axis ✓ lifecycle-axis (deferred trio) ✓. Per-piece trace: P1[T1,T8] · P2[T15 + injection/language/degenerate entries] · P3[T11 + descope suggestions] · P4[T4 + splitability anchor + thin-submission] · P5[T2,T3,T6,T9,T16] · P6[T10 + T12-deferred + K2-note] · P7[T7 case files + acid set].

## Telemetry

- Generators applied: 4/4 · Framers applied: 3/3
- Convergence: **YES** — marked-up-draft interaction model (4 independent mechanisms)
- Survivors tested: 16/16 explicit (+3 kills logged as seeds)
- Per-piece Inversion compliance: P1 satisfied (executor inversion via audit) · P4 satisfied (composition-vocabulary challenge) · P5 satisfied (one-card severity inversion) · P6 satisfied (contract challenges) · P2/P3/P7 content-production (n/a)
- Failure modes observed: none (uncomfortable candidate — "not an LLM at all" — was generated by the audit and integrated rather than dodged)
- **Overall: PROCEED**
