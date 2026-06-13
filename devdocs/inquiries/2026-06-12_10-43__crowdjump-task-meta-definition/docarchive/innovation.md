# Innovation — Crowdjump Task Meta-Definition

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_10-43__crowdjump-task-meta-definition/_branch.md` — seed inherited via sensemaking SV6 + decomposition P1–P5 (Production-task mode: generate candidates per piece for the two-axis, triple-form, normative meta-definition).

## Seed & Methodology Mode

- **Seed:** design the content of the meta-definition within SV5's fixed frame (≈11 attribute triples, two axes, two open parameters) — a Gap+Question seed ("the platform's central noun is undefined").
- **Inherited mode:** Standard default (4G+3F) — the framing says "create," not "challenge"; structure was freshly adjudicated upstream.
- **Alternative considered:** Contrarian-rethink (Framer-weighted) — would produce candidates attacking the two-axis frame itself (e.g., "no definition at all; example-driven clarifier"), at the cost of concrete attribute design. **Decision: default mode**, because the per-piece Inversion rule + Inherited Frame Audit below still force frame challenges; the run's marginal value is concrete design.
- **Meta-decision pieces:** P1 (evaluation-criterion + framing-semantic), P2 (evaluation-criterion), P3 (evaluation-criterion + coins "Jumper-comprehensibility"), P5 (extension convention) → piece-level Inversion mandatory for each. P4 = content-production. No piece commits an intervention shape (this is a definitional artifact, not spec maintenance) → property (v) fires nowhere; content-axis Inversions satisfy compliance.

## Phase 2 — Generate (7 mechanisms × generic / focused / contrarian)

### 1. Lens Shifting (Framer)
- **Generic — MVP lens:** before the AI clarifier exists, the primary consumer is the human Launcher in the wizard → the attribute QUESTION TEMPLATES double as wizard microcopy NOW. The definition ships value pre-pipeline.
- **Focused — Jumper lens:** write every instance-axis satisfaction test from the Jumper's POV ("a stranger Jumper reading this knows exactly which page to open / what to do / what the proof shows"). The Jumper-comprehensibility test becomes the axis's master phrasing convention.
- **Contrarian — fraud lens:** a maximally-defined PUBLIC spec also scripts the cheater (fabricate exactly the expected evidence). Under this lens, definedness has an information-separation consequence: Launcher-facing spec ≠ verifier-facing expectation detail. (→ S8)

### 2. Combination (Generator)
- **Generic:** triples × the existing wizard FSM → instance attributes map onto launch steps; the definition becomes the wizard's table of contents (launch = a walk through the definition).
- **Focused:** definedness checks × matching's `unmet_requirements()` pattern → `undefined_requirements(task) -> list[str]`, the same gate shape the codebase already speaks; one mental model: "gates return unmet lists." (→ S4)
- **Contrarian:** kind-axis × Jumper reporting → admissibility as a CONTINUOUS property (Jumpers can flag non-doable/non-allowed tasks post-launch), not a launch-time stamp. (→ S10)

### 3. Inversion (Framer)
- **Generic (depth-iterated to system level):** "the definition validates tasks" → "tasks validate the definition" → system-level: the definition is a CALIBRATION ARTIFACT — every clarifier miss and dispute is labeled evidence about the attribute set; the doc should carry a feedback register. (→ S9)
- **Focused (P3 inversion, depth-iterated):** "goal must be clear first" → "goal may be fuzzy if actions are exact" → system-level: **the binding contract is the ACTIONS + COMPLETION-CRITERION pair; goal/target are disambiguation aids.** Ask-order (goal-first, good UX) ≠ bindingness-order (actions/completion load-bearing). (→ S11)
- **Contrarian:** "more defined is better" → over-definition kills conversion and violates path tolerance (FP3) → definedness has an OPTIMUM: "defined enough" = all attributes satisfied; beyond that, warn AGAINST over-constraint. (→ folded into P1 semantics: sufficiency, not maximization)

### 4. Constraint Manipulation (Framer; ADD + REMOVE both exercised)
- **ADD (generic):** "every satisfaction test reads ONLY the submission text+fields" → sharp separation: **definedness ≠ truth.** "Does the text name a target URL?" is definitional; "does that URL exist?" is verification's job. (→ S3)
- **ADD (focused):** "≤6 attributes per axis" cap → forces merges (performable+bounded) → TESTED AND KILLED: merging destroys question granularity. Salvage: GROUPING for presentation (work-content group / feasibility group) without merging.
- **REMOVE (contrarian):** remove "evaluated at launch time" → attributes become lifecycle-wide invariants; disputes cite the completion-criterion attribute → **disputes are a fifth consumer** of the definition. (→ S6 partner; P5 update)

### 5. Absence Recognition (Generator; patch + redesign, bidirectional)
- **Patch-level:** the triple lacks a few-shot anchor → add an optional **example-violation field** per attribute (quad-lite: definition/test/question/example). (→ S5)
- **Redesign-level (missing):** nothing in the project states a **canonical task normal form**. From scratch, the definition implies one: *"[Do action(s)] on [target] until [observable end-state], by any matching Jumper, within [bound]."* Attributes = slots; **definedness = slot-filling**; clarification = asking for empty slots. (→ S1)
- **Redesign-level (already-present-in-other-form):** budget/slots/deadline/audience are ALREADY structurally enforced wizard fields — the definition must mark them as field-backed attributes rather than re-deriving them, or the doc looks incomplete while duplicating the schema.

### 6. Domain Transfer (Generator; native source included)
- **Native (software):** agile Definition-of-Done + Gherkin → the completion criterion is defined when writable as a **Then-clause over screen-observable events** ("Then the follow button reads 'Following'"). Concrete phrasing rule for the test field. (→ converges with S1/S3)
- **Different field — clinical trials:** eligibility-vs-endpoint separation mirrors audience-vs-completion; the transferable principle is **endpoint pre-registration**: the completion criterion is immutable once Jumpers are active; changing it = a new task version. Anti-moving-goalposts, protects Jumpers in disputes. (→ S6)
- **Different field — freelance marketplaces:** gig anatomy (deliverable + revision policy) → TESTED AND KILLED as an attribute (revision/redo is lifecycle policy, not task-ness); preserved as a note for the verification BOM.

### 7. Extrapolation (Generator)
- **Generic:** clarifier maturity grows → dispute outcomes become labeled under-definition examples → converges with S9 (feedback register).
- **Focused:** task volume grows → per-attribute checks become the platform's quality-analytics schema → aggregation should be a **graded score with checklist rendering**, not a bare checklist — resolves SV5's open aggregation question. (→ S7)
- **Contrarian:** the capability envelope will widen (API-based evidence channels beyond screen recording) → verifiable-in-principle must say "observable via the platform's approved evidence channel (currently: screen recording)" — converges with the capability-versioned anchor.

## Inherited Frame Audit

- **Seed central assumptions:** (a) "attribute-based form" (user-prescribed); (b) "two-axis structure" (SV6 commitment).
- **Challenge scan:** (a) challenged by S1 (slot/sentence normal form is a competing organization — reconciled: slots ARE the attributes rendered as a template; the forms are dual). (b) was UNCHALLENGED → **audit fires**; type = Design choice → Absence Recognition redesign-level applied: *from scratch, would two axes exist?* Alternative: ONE flat attribute list where each attribute carries its own enforcement flag (gate | clarify). What follows: more flexible (any attribute could gate), simpler deep structure; the axes survive as DEFAULT flag groupings. **Tested → refined into S2:** per-attribute enforcement flag with axis-derived defaults; two axes remain the presentation/derivation layer. Audit satisfied after one return-to-Phase-2 cycle.
- Piece-level commitments: P1 triple challenged (S5 quad-lite) ✓; P2 gate-at-launch challenged (S10 continuous admissibility) ✓; P3 ordering challenged (S11 bindingness inversion) ✓; P5 four-consumer list challenged (disputes as fifth) ✓.

## Phase 3 — Test (5-test cycle; dispositions)

| # | Candidate | N | S | F | A | MI | Disposition |
|---|---|---|---|---|---|---|---|
| S1 | Task normal form (slot sentence; definedness = slot-filling) | ✓ | ✓ (objection "too rigid for diverse types" — fails: slots are optional-per-type and SVI's taxonomy maps cleanly) | ✓✓ (clarifier = slot-filling; wizard steps; analytics) | ✓ | ✓ Absence + DomainTransfer + Combination converge | **ACTIONABLE** |
| S2 | Per-attribute enforcement flag, axis-default (audit product) | ✓ | ✓ | ✓ | ✓ | audit-forced, then confirmed by Inversion-contrarian sufficiency view | **ACTIONABLE** (refines P1; RE-TEST ran on P1's "two postures" claim — semantics preserved, mechanism generalized) |
| S3 | Tests read text-not-world (definedness ≠ truth) | ✓ | ✓ (objection: "fake URLs pass" — correct and intended; existence is verification's job) | ✓ | ✓ | ✓ ConstraintAdd + Gherkin | **ACTIONABLE** |
| S4 | `undefined_requirements()` mirrors matching's unmet-list shape | ✓ | ✓ | ✓ | ✓ | grounded: services/matching.unmet_requirements exists | **ACTIONABLE** (P5 consumer note; implementation later) |
| S5 | Quad-lite: optional example-violation per attribute | ✓ | ✓ | ✓ | ✓ | single-mechanism but trivially additive | **ACTIONABLE** |
| S6 | Completion-criterion immutability once Jumpers active (pre-registration transfer) | ✓ | ✓ (refined from "immutable post-launch": edits harmless before first jump) | ✓ | ✓ | ✓ trials + disputes-consumer | **ACTIONABLE** |
| S7 | Graded definedness score + checklist rendering | ✓ | ✓ | ✓ | ✓ | Extrapolation + clarifier-UX | **ACTIONABLE** (resolves open aggregation) |
| S8 | Launcher-spec vs verifier-expectation information separation | ✓ | ✓ | ✓ | needs verification component | single-lens | **DEFERRED** — revival: verification BOM start |
| S9 | Feedback register (definition as calibration artifact) | ✓ | ✓ | ✓ | needs running clarifier | ✓ Inversion + Extrapolation | **DEFERRED** — revival: clarifier v1 ships |
| S10 | Continuous admissibility via Jumper flagging | ✓ | ✓ | ✓ | needs moderation surface | single-mechanism | **DEFERRED** — revival: moderation/abuse work |
| S11 | Bindingness note: actions+completion are the binding pair; ask-order ≠ bindingness-order | ✓ | ✓ | ✓ | ✓ | Inversion depth + dispute logic | **ACTIONABLE** (refines P3) |
| K1 | Attribute-count cap | killed (granularity loss) — salvaged as grouping | | | | | new-seed |
| K2 | Revision-policy-as-attribute | killed (lifecycle, not task-ness) — note to verification BOM | | | | | new-seed |
| K3 | Two-axis as deep structure | killed-as-deep-structure, survives as presentation (S2) | | | | | refined |

**Assembly check:** S1+S2+S3+S5+S7 compose into an emergent architecture none holds alone — **an attribute REGISTRY (per attribute: name, definition, text-only test, question, example, enforcement flag, axis tag) + a task NORMAL FORM whose slots map to registry attributes + a graded sufficiency rule + lifecycle rules (S6) + five consumers**. The registry makes the sentence checkable; the sentence makes the registry usable. Axis coverage: form-axis (registry/sentence), enforcement-axis (flags), evaluation-axis (text-only, graded), lifecycle-axis (immutability, continuous admissibility) — all varied. Per-piece mechanism trace: P1[ConstraintADD, Inversion-contrarian, S2], P2[Extrapolation-contrarian, Combination-contrarian], P3[Inversion-focused, LensShift-focused, DomainTransfer-native], P4[acid candidates from S1 normal form], P5[ConstraintREMOVE, LensShift-contrarian].

## Telemetry

- Generators applied: 4/4 · Framers applied: 3/3
- Convergence: **YES** — 3 mechanisms (Absence-redesign, Domain Transfer-Gherkin, Combination-wizard) converge on S1 (normal form / slot-filling); shared-input check: they reach it from different grounds (design absence vs imported pattern vs existing FSM) — independent, not spurious
- Survivors tested: 11/11 (+3 killed, logged as seeds)
- Per-piece Inversion compliance: P1 satisfied · P2 satisfied · P3 satisfied · P5 satisfied · P4 content-production (n/a)
- Failure modes observed: none (uncomfortable fraud-lens candidate deliberately tested → S8 deferred on actionability, not comfort)
- **Overall: PROCEED**
