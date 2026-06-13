# Routelister — Task-Consumer LLM Detections & Scenarios (Route-Map)

## User Input

territory: `/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/` (this inquiry's artifacts — `_branch.md` + the six discipline outputs). goal: "a catalog of detection entries (trigger + suggestion shape) and scenario flows for the task-consumer LLM, grounded in the task meta-definition, consumption-time only — serving clarifier-startup, launch quality, Launcher UX, prompt-seeding, and test coverage (per _branch.md Goal, openness preserved)". Save the route-map to `routelister.md`; persistent index at `_route.md` (fresh — none existed).

## Map Header

**Identities: 18 · High-priority: 5** · mode: root/project-space (breadth) · entry: fresh

## Route Index

| # | Direction | grain | kind | engagement | Priority |
|---|---|---|---|---|---|
| 1 | the detection inventory (~15 named entries, three classes) | project-space | teleological | DEVELOP | HIGH |
| 2 | the detection framework schema (fields, severities, uncertainty, executor) | project-space | teleological | DEVELOP | HIGH |
| 3 | the marked-up-draft card (diff + chips + stet + rationales) | project-space | teleological | DEVELOP | HIGH |
| 4 | the clarifier component BOM (structural layer) | project-space | teleological | INVESTIGATE-FRONTIER | HIGH |
| 5 | the ToS-posture decision (open parameter) | project-space | teleological | INVESTIGATE-FRONTIER | HIGH |
| 6 | severity-routed rendering tree (green channel / batch / 4a / 4b) | project-space | teleological | DEVELOP | MED |
| 7 | the output contract / normalizer role | project-space | teleological | DEVELOP | MED |
| 8 | the hybrid executor boundary (code vs llm) | project-space | epistemic | TEST | MED |
| 9 | per-detection case files (fire/clear/uncertain exemplars) | project-space | teleological | PURSUE-SEED | MED |
| 10 | prompt-seed rendering (catalog → system prompt) | project-space | teleological | DEVELOP | MED |
| 11 | the thin-submission scenario | project-space | teleological | DEVELOP | MED |
| 12 | policy-floor semantic-intent entries + hold path | project-space | teleological | DEVELOP | MED |
| 13 | adversarial red-team of the consumer (hostile submissions) | project-space | epistemic | TEST | MED |
| 14 | approval semantics (consensus snapshot; binding-pair freeze) | project-space | epistemic | REFINE | MED |
| 15 | canon coupling (catalog ↔ meta-definition version conventions) | project-space | epistemic | CONSOLIDATE | MED |
| 16 | the eval matrix (archetype × acid case) | project-space | teleological | PURSUE-SEED | MED |
| 17 | threshold calibration (question cap, confidence biases) | project-space | epistemic | TEST | LOW |
| 18 | deferred ecosystem hooks (duplicate-detect · risk routing · trust signal) | project-space | teleological | PURSUE-SEED | LOW |

## Route Records

**1. The detection inventory** — Goal: the catalog · project-space · teleological · DEVELOP
Movement: build the ~15 sketched entries (channel/kind/instance+composition) into full instances of the entry schema.
WHY: the inquiry stabilized classes, seeds, and anchor cases (sensemaking SV6; innovation T4/T11/T15) but entries exist as sketches; the goal IS this content.
Priority: HIGH · Confidence: HIGH · Guidance: compact — start from the meta-definition's 11 triples (mechanical), then the composition four, then channel three (bc: authority descends from canon to new design).

**2. The detection framework schema** — project-space · teleological · DEVELOP
Movement: fix the entry schema (name, code, class, executor, trigger, severity, result, proposal, question, transform) + severity/uncertainty semantics + ordering/short-circuit as one normative section.
WHY: every entry instantiates it (decomposition P1 is every piece's contract).
Priority: HIGH · Confidence: HIGH · Guidance: compact — the executor field and uncertainty routing are the two pieces with no prior art in-project (bc: the rest inherits from the meta-definition's form).

**3. The marked-up-draft card** — project-space · teleological · DEVELOP
Movement: specify the card: diff-style restatement, choice-chips, stet/override scope rule, one-line rationales, preview line, ≤3-question budget.
WHY: 4-mechanism convergence (innovation) named this the interaction model; critique locked its consent guards.
Priority: HIGH · Confidence: MED · Guidance: compact — prototype as bot message + web mock before spec-freezing (bc: chip ergonomics differ between the two clients).

**4. The clarifier component BOM** — project-space · teleological · INVESTIGATE-FRONTIER
Movement: open the structural layer — `devdocs/scoped/be/clarifier/` BOM consuming the catalog (placement, endpoints, invocation, revision loop).
WHY: the branch's Layer Commitment names it the next layer; the prior finding's COULD is gated on canon that now exists.
Priority: HIGH · Confidence: MED · Guidance: compact — mirror the matching component's BOM pattern (bc: same decisions-table + sections discipline already worked twice).

**5. The ToS-posture decision** — project-space · teleological · INVESTIGATE-FRONTIER
Movement: enter the open parameter: decide the target-platform ToS posture that the policy-floor entries' final wording and severity depend on.
WHY: surfaced in both inquiries as the blocking open product decision (PROJECT.md Open Decisions; critique T11's hold-path).
Priority: HIGH · Confidence: HIGH (that it blocks) · Guidance: none — it is a product call, not a design task.

**6. Severity-routed rendering tree** — project-space · teleological · DEVELOP
Movement: finalize the routing: green-channel receipt / batched card / decline-with-repair-path (4b) / decline-alone (4a).
WHY: critique's strongest prosecution produced the 4a/4b split; the tree is committed but unspecified at wording level.
Priority: MED · Confidence: HIGH · Guidance: none.

**7. The output contract / normalizer role** — project-space · teleological · DEVELOP
Movement: specify approved/declined output shapes, normalized slots, detection log schema; map consumers (matching, verification, Jumper display, feedback register).
WHY: frame-exit analysis made the consumer the pipeline's normalizer; three components await the slots.
Priority: MED · Confidence: MED · Guidance: compact — the location-slot adoption belongs to the matching component's standing decision; hand it over, don't flip it here (bc: scope discipline D8).

**8. The hybrid executor boundary** — project-space · epistemic · TEST
Movement: validate the code|llm assignment per entry against the actual codebase (which existing validations already cover which entries).
WHY: the Inherited Frame Audit produced the hybrid; the per-entry assignments are asserted, not verified against `src/`.
Priority: MED · Confidence: MED · Guidance: compact — grep the wizard/schema validations first (bc: that's where silent overlap would hide).

**9. Per-detection case files** — project-space · teleological · PURSUE-SEED
Movement: write 2–3 canonical examples (fire/clear/uncertain) per entry as first-class content.
WHY: innovation T7 (prompt+eval dual use) survived but no cases exist beyond the acid set.
Priority: MED · Confidence: HIGH · Guidance: none.

**10. Prompt-seed rendering** — project-space · teleological · DEVELOP
Movement: define the mechanical rendering from catalog entries + case files into the consumer's system prompt.
WHY: the prompt-seed motivation (branch WHY-axis) requires the catalog→prompt path to be generative, mirroring the meta-definition→catalog generativity.
Priority: MED · Confidence: MED · Guidance: compact — keep vendor-neutral; the catalog is canon, the prompt is a build artifact (bc: critique A1 of the prior inquiry settled this altitude question).

**11. The thin-submission scenario** — project-space · teleological · DEVELOP
Movement: specify the variant's trigger (empty-slot aggregate) and its single re-description ask.
WHY: committed at sensemaking (one-card rule's escape hatch) but unshaped.
Priority: MED · Confidence: MED · Guidance: none.

**12. Policy-floor semantic-intent entries + hold path** — project-space · teleological · DEVELOP
Movement: write the policy entries as semantic-intent judgments with euphemism few-shots and the conservative-hold routing.
WHY: critique T11 survived with the hold-path dependency; entries are the platform's policy mouth.
Priority: MED · Confidence: MED · Guidance: compact — wording stays posture-parameterized until route 5 resolves (bc: open parameter).

**13. Adversarial red-team of the consumer** — project-space · epistemic · TEST
Movement: probe the designed consumer with hostile submissions (injection, euphemism, consent-gaming via chips) before any implementation hardens.
WHY: channel defenses and chip-consent guards are designed but untested; risk perspective flagged all three.
Priority: MED · Confidence: MED · Guidance: none.

**14. Approval semantics** — project-space · epistemic · REFINE
Movement: sharpen what approval commits — the consensus snapshot's content, the binding-pair freeze notice, dispute weight of the approved reading.
WHY: innovation T9 set the framing; the dispute-facing precision is unrefined and dispute resolution consumes it.
Priority: MED · Confidence: MED · Guidance: none.

**15. Canon coupling** — project-space · epistemic · CONSOLIDATE
Movement: consolidate the extension/versioning conventions of the catalog and the meta-definition into one coherent canon-pair rule (attribute change ↔ detection change).
WHY: two living canons now exist with separate version notes; drift between them is the new silent failure mode.
Priority: MED · Confidence: MED · Guidance: none.

**16. The eval matrix** — project-space · teleological · PURSUE-SEED
Movement: build the archetype × acid-case matrix into a runnable eval set.
WHY: test-coverage motivation (branch WHY-axis); P7 sketched the matrix, nothing runs.
Priority: MED · Confidence: MED · Guidance: compact — reuse the acid set + case files (routes 9, 1) as the corpus (bc: no real submissions exist yet).

**17. Threshold calibration** — project-space · epistemic · TEST
Movement: validate the provisional numbers (question cap 3, confidence biases) against real launched tasks.
WHY: every number is uncalibrated by declared stance.
Priority: LOW (now) · Confidence: HIGH (that it must happen) · Guidance: none — blocked on production data by nature.

**18. Deferred ecosystem hooks** — project-space · teleological · PURSUE-SEED
Movement: take up, at their gates, the three deferred candidates — duplicate-task detection (needs history access), risk-score routing (needs review queue), repeat-policy trust signal (needs trust component).
WHY: innovation T12–T14 passed testing but lack host components; each carries a named revival gate.
Priority: LOW · Confidence: MED · Guidance: none.

## Excluded

- **Model/vendor selection for the consumer LLM** — implementation-layer choice; engaging it now advances no part of the catalog goal (and is selection-shaped besides).
- **Multi-turn agent with memory (production-stance consumer)** — explicitly out-of-frame at MVP stance (sensemaking Phase/Calibration); engaging now sharpens nothing the goal rests on.
- **Wizard replacement by the consumer** — killed in innovation (K2) for MVP; a lifecycle direction beyond consumption-time bounds, preserved only as a note in the output-contract record.
- **Verification evidence design** — neighboring component's territory (MQ4 exclusion); the consumer only PRODUCES the completion criterion.
- **"Conclude the inquiry" / "start the next iteration"** — control-flow, not concept-directions (NOT-list).

## Telemetry

- mode: root/project-space · entry: fresh
- identities: 18 · teleological 12 / epistemic 6 · high-priority 5
- individuations: 21 considered → 18 identities (3 lean-to-split decisions kept separate: red-team vs channel entries; prompt-rendering vs clarifier BOM; thresholds vs eval matrix) · uncertain-individuations flagged: 1 (prompt-rendering could be a BOM manifestation — kept split per asymmetry) · stale: 0 (fresh index)
- convergence: sweep cycles 2; second cycle yielded no new identities · frontier flags: none (territory compact)
- failure modes checked: LAYER 1 (Over-merge, Under-coverage, Wrong-grain, Goal-loss, Type-misassignment, Index-drift) + LAYER 2 (Selection-creep, Process-coupling, Description-collapse, Manifestation-dump) — none fired; control-flow candidates routed to Excluded
- **Self-assessment: PROCEED**
