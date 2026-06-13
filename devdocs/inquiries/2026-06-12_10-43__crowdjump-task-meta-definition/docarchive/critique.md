# Critique — Crowdjump Task Meta-Definition

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_10-43__crowdjump-task-meta-definition/_branch.md` — candidates from `innovation.md` (S1–S11 + assembly) evaluated against `sensemaking.md` SV6 commitments and the branch goal.

## Phase 0 — Dimensions (extracted from sensemaking; weights by purpose-fitness)

| # | Dimension | Weight | Extracted from | Success criterion |
|---|---|---|---|---|
| D1 | Generativity (clarifier derivable) | CRITICAL .20 | C4, WHY-enable-the-clarifier | per attribute, a question template is mechanically reachable from its test — **substance criterion: actually derive one on task #2** |
| D2 | Verifiability alignment | CRITICAL .20 | C1, C6 | completion-criterion → observable-evidence contract; no test promises what verification can't check |
| D3 | Launcher feasibility / friction | HIGH .15 | Human perspective, FP2 | plain-language questions; instance axis clarifies, never silently rejects |
| D4 | Task-universe coverage | HIGH .125 | A7, SVI taxonomy | each SVI task type expressible — **substance criterion: render a non-engagement type in the candidate's form** |
| D5 | Open-parameter discipline | MED .10 | C5, Phase/Calibration anchor | ToS posture + capability envelope remain named OPEN slots |
| D6 | Codebase coherence | MED .10 | SP3, schema/wizard/matching | no contradiction with existing structures — **external anchors: schemas/task.py fields; bot launch steps; services/matching.unmet_requirements** |
| D7 | Leanness | MED .075 | Strategic/MVP, balance flag | minimal machinery; no audit-theater fields |
| D8 | Definitional overreach (project risk) | MED .075 | MQ4 exclusions, Layer Commitment | meaning-layer only; sufficiency not maximization; no pipeline/code |
| D9 | Dispute safety | MED .075 | Risk anchor, trials transfer | definitions stay usable under conflict |

**Frame-premise test** (candidate space rests on inherited commitments): (i) *two-axis structure* — already prosecuted by Innovation's audit; survived as presentation layer over per-attribute flags (S2). (ii) *attribute-based form* — prosecuted via S1's competing normal-form organization; reconciled as dual rendering (slots ARE attributes). (iii) *normative stance* — what-if-wrong: descriptive reading would describe an empty/failed population (only dev rows + task #2 exist — empirical anchor: the dev DB and the wizard transcript); normative stands. Premises named and independently prosecuted.

## Phase 1 — Landscape

- **Viable region:** meaning-layer candidates that raise D1/D2 at low D3 cost and respect D5/D8.
- **Dead region:** anything silently resolving ToS (D5), demanding world-knowledge at launch (D2/D6), or smuggling implementation (D8).
- **Boundary region:** lifecycle-extenders (S6, S10) and verifier-information separation (S8) — strong D9, weaker actionability.
- **Unexplored (flagged, low topological promise):** final attribute NAMES (bikeshed-level), numeric score thresholds (needs production data — correctly deferred).

## Phase 2/3 — Adversarial Evaluation + Verdicts

**S1 — Task normal form ("[Do action(s)] on [target] until [observable end-state], by any matching Jumper, within [bound]")**
- Prosecution (strongest): templates ossify; duration tasks and multi-action tasks strain one sentence; Launchers will free-write anyway and the form goes dead. **Substance probe executed:** task #2 repaired renders cleanly ("Open instagram.com/<handle>, like the 3 most recent photos, until all 3 hearts show filled, in one session"); engagement-with-duration renders ("watch video V until the player shows ≥30s elapsed"); form-fill renders ("open form F, complete fields A–C, submit, until the confirmation page is visible") — D4 substance passes.
- Defense: 3-mechanism convergence; slot-filling is the clarifier's entire future UX; slots are optional-per-type.
- Collision: ossification risk dissolves once the form is the canonical RENDERING target, not the input format — Launchers keep free text; the clarifier maps into the form.
- **Verdict: SURVIVE** (caveat: the doc must state form = rendering, not input).

**S2 — Per-attribute enforcement flags, axis-derived defaults**
- Prosecution: flag flexibility invites config drift (someone flips `atomic` to gate and kills conversion); two clean postures were the simpler story (D7).
- Defense: axes survive as the default story; flags localize future exceptions (e.g., policy escalation) without restructuring.
- Collision: drift bounded by rule: flag changes = version-note events (couples to P5 convention).
- **Verdict: SURVIVE** (caveat: defaults normative; deviations versioned).

**S3 — Tests read text-not-world (definedness ≠ truth)**
- Prosecution (user-perspective axis): a Launcher whose fake/missing target passes definedness feels gaslit later ("it said my task was fine").
- Defense: the separation is what keeps launch cheap (D3), tests submission-evaluable (D6), and verification authoritative (D2).
- Collision: defense wins given the explicit handoff sentence in the doc ("definedness is about the spec; truth is verified at submission").
- **Verdict: SURVIVE** (caveat: handoff stated, not implied).

**S4 — `undefined_requirements()` mirrors matching's unmet-list shape**
- Prosecution: implementation detail in a meaning-layer artifact (D8).
- Defense: external anchor verified — `services/matching.py` `unmet_requirements()` exists with exactly this shape; naming the symmetry is a consumer note, not code.
- **Verdict: SURVIVE** as a P5 consumer note only.

**S5 — Optional example-violation field (quad-lite)**
- Prosecution: examples overfit the future LLM checker to one violation shape.
- Defense: optional; few-shot anchors materially improve weak-model judgment; D1 gain.
- **Verdict: SURVIVE** (optional per attribute).

**S6 — Completion-criterion immutability once a Jumper is active**
- Prosecution (failure-case axis): blocks legitimate post-launch repair; the clarifier's whole spirit is iterating specs.
- Defense: binds only the completion criterion, only after first active Jumper; repairs before activity are free; protects Jumpers from moving goalposts (D9's core case).
- **Verdict: SURVIVE.**

**S7 — Graded definedness score with checklist rendering**
- Prosecution: scores invite threshold-gaming and false precision (D7).
- Defense: analytics and soft-clarify UX need graded signal.
- Collision: resolved by positioning — score is INTERNAL aggregation; the NORMATIVE statement stays the checklist ("defined = all attributes satisfied").
- **Verdict: SURVIVE** (caveat: numeric thresholds deliberately unset — unexplored region, needs data).

**S8 — Launcher-spec vs verifier-expectation separation** — boundary region; D9-strong, actionability blocked on verification component. **Verdict: DEFER** (revival: verification BOM). Constructive: carries the fraud-lens seed forward.

**S9 — Feedback register (definition as calibration artifact)**
- Prosecution: empty machinery today (D7 — audit-theater risk).
- Defense: one empty section costs nothing; without a designated home, future dispute-evidence scatters.
- **Verdict: REFINE** → include the register as a STUB section in the definition doc now; population mechanism stays deferred (revival: clarifier v1).

**S10 — Continuous admissibility via Jumper flagging** — moderation-layer concern, not task-ness (D8). **Verdict: DEFER** (revival: moderation/abuse work). Constructive: admissibility re-check belongs to lifecycle policy.

**S11 — Bindingness note (ask-order ≠ bindingness-order; actions+completion bind)**
- Prosecution: two orderings confuse readers (D3/D7).
- Defense: the distinction kills two real future bugs — clarifier asking in binding order (bad UX) and disputes adjudicating on goal text (bad rulings).
- **Verdict: SURVIVE.**

**ASSEMBLY — attribute registry + normal form + sufficiency rule + lifecycle rules + five consumers**
- Prosecution (user-perspective, strongest): scope creep — the user asked for "a meta definition using attributes," and the seed words (achievable, recordable) no longer appear as attributes; "the user's words vanished."
- Defense: every element is definitional content; the user's stated WHY ("to generate these first") demands exactly the registry+form generativity; MQ4 exclusions respected (zero pipeline/code).
- Collision: prosecution lands ONE hit — traceability.
- **Verdict: SURVIVE with one REFINE requirement: the definition doc MUST carry a seed-mapping table (user's seed word → where it landed and why).** Ranked #1.

**Specification-gap probe** (mandatory): "satisfaction test = LLM-judgment predicate" — the runtime determination mechanism (who runs the test) is the DEFERRED pipeline by explicit Layer Commitment; the doc states tests as human-or-LLM-runnable questions. Gap is declared, not silent. Pass.

## Phase 3.5 — Assembly Check (across survivors)

S6 + S11 fuse into one elegant rule none stated alone: **the binding pair** — actions + completion-criterion are simultaneously what BINDS the Jumper's obligation and what FREEZES at first activity. One concept serves ordering, disputes, and immutability. Folded into the assembly (no new candidate needed; evaluated as part of assembly's D9/D7 strength).

## Phase 4 — Coverage + Convergence

- **Accumulator:** 12 evaluations logged; 0 new kills (Innovation's 3 kills inherited: count-cap, revision-policy-attribute, two-axis-as-deep-structure); refinement record: S9 stub-now, assembly seed-mapping; mechanism-independence: **validated** (external anchors cited: `services/matching.py`, `src/schemas/task.py`, bot launch steps, the task #2 transcript, SVI capability taxonomy).
- **Coverage map:** SV5 frame fully evaluated; unexplored: attribute naming (bikeshed), score thresholds (data-dependent) — neither topologically promising for new viable candidates.
- **Convergence:** landscape STABLE (candidates landed where sensemaking predicted; the only structural move — S2 — came from Innovation's audit, already absorbed); clean SURVIVE exists.
- **Signal: TERMINATE.** Ranked survivors: 1) Assembly (with seed-mapping refinement) · 2) S1 normal form · 3) S3 text-not-world · 4) S11+S6 binding pair · 5) S2 flags · 6) S7 score/checklist · 7) S5 examples · 8) S4 consumer note. Deferred with triggers: S8, S9(stub now), S10.

## Convergence Telemetry

- Dimension coverage: 9/9 applied; all candidates faced critical-weight dimensions
- Adversarial strength: STRONG (substance probes executed: live task-#2 rewrite, non-engagement renders; user-perspective objections landed one refinement)
- Landscape stability: STABLE
- Clean SURVIVE exists: YES (assembly, post-refinement requirement)
- Failure modes observed: none (rubber-stamp counter: 2 REFINEs + 3 DEFERs + caveats on every SURVIVE; nitpick counter: defense mandatory, severity weighted)
- **Overall: PROCEED**
