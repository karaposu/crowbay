# Routelister — Clarifier Component BOM (Route-Map)

## User Input

territory: `/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/` (this inquiry's artifacts — `_branch.md` + the six discipline outputs). goal: "a BOM document for the clarifier component under `devdocs/scoped/be/clarifier/` — decisions table + data model + service/module layout + endpoints + client integration + revision/approval mechanics + test plan, in implementable order, consuming `task_consumer_catalog.md` v1.2 + `task_meta_definition.md` as canon — serving enable-next-build-session, close-the-mvp-pipeline-gap, de-risk-integration, sustain-route-map-momentum (per `_branch.md` Goal, openness preserved)". Save the route-map to `routelister.md`; persistent index at `_route.md` (fresh — none existed for this territory).

## Map Header

**Identities: 16 · High-priority: 3** · mode: root/project-space (breadth) · entry: fresh

## Route Index

| # | Direction | grain | kind | engagement | Priority |
|---|---|---|---|---|---|
| 1 | the BOM document (decisions table + 9 sections, survivors folded in) | project-space | teleological | DEVELOP | HIGH |
| 2 | implementation of the BOM's sections (P1→P8 build) | project-space | teleological | INVESTIGATE-FRONTIER | HIGH |
| 3 | the mock backend as MVP product | project-space | teleological | DEVELOP | HIGH |
| 4 | the canon-as-code spine (registry + drift guards + tolerance) | project-space | teleological | DEVELOP | MED |
| 5 | the card payload schema (zones, platform-neutral marks) | project-space | teleological | DEVELOP | MED |
| 6 | the two-client card prototype (freeze gate) | project-space | epistemic | TEST | MED |
| 7 | the off-flag parity contract (enumerated fields) | project-space | epistemic | TEST | MED |
| 8 | the operator capability (minimal gate → real roles) | project-space | teleological | INVESTIGATE-FRONTIER | MED |
| 9 | draft data lifecycle (TTL knob, cleanup, PII retention posture) | project-space | epistemic | REFINE | MED |
| 10 | prompt-seed rendering (prompt-builder contract → actual builder) | project-space | teleological | INVESTIGATE-FRONTIER | MED |
| 11 | detection-log → calibration loop (feedback register wiring) | project-space | teleological | INVESTIGATE-FRONTIER | LOW-MED |
| 12 | replay/eval harness | project-space | teleological | PURSUE-SEED | LOW-MED |
| 13 | real-vendor reference backend (+ smoke checklist) | project-space | teleological | INVESTIGATE-FRONTIER | LOW-MED |
| 14 | async migration seam (polling → background jobs) | project-space | teleological | INVESTIGATE-FRONTIER | LOW |
| 15 | hold-path operations (SLA, re-ping) | project-space | teleological | PURSUE-SEED | LOW |
| 16 | task-table draft merge (K2's preserved seed) | project-space | teleological | PURSUE-SEED | LOW |

## Route Records

**1. The BOM document** — Goal: the catalog'd spec · project-space · teleological · DEVELOP
Movement: write `devdocs/scoped/be/clarifier/bom.md` — §0 decisions table (A1–A6 + K1/K2 grounds + canon bindings) + the 8 pieces as ordered checkbox sections with critique's survivors folded in as line-items.
WHY: the goal IS this artifact; every discipline output exists to feed it; critique ranked the assembly #1 with the presentation constraint (work-order, not treatise).
Priority: HIGH · Confidence: HIGH · Guidance: compact — mirror the backbone BOM's §0+checkbox pattern; decisions table ≤ a screen (bc: critique's presentation requirement is binding).

**2. Implementation of the BOM's sections** — project-space · teleological · INVESTIGATE-FRONTIER
Movement: open the build: P1∥P2 → P3∥P4 → P5 → P6 → P7 → P8 in dependency order, section by section.
WHY: the branch's WHY-axis (enable-next-build-session) and articulation 4's extent reading ("lets do this" as build consent) — the user decides at finding time.
Priority: HIGH · Confidence: HIGH · Guidance: compact — start P1+P2 in one session (contract producers; everything else consumes them) (bc: dependency order).

**3. The mock backend as MVP product** — project-space · teleological · DEVELOP
Movement: build the deterministic catalog-shaped mock to full acid coverage; treat it as the demoable product, not a stub.
WHY: it makes the whole component shippable and testable before any API key exists (sensemaking KI4; innovation V-L2); CI stays keyless.
Priority: HIGH · Confidence: HIGH · Guidance: none.

**4. The canon-as-code spine** — project-space · teleological · DEVELOP
Movement: registry module mirroring catalog §4 entries + version-pin test (hard) + literal-scan (advisory) + unknown-code tolerance — designed as ONE unit.
WHY: critique bound T2+T5 with the caveat "never split across sections"; this materializes the detections inquiry's canon-coupling route in code.
Priority: MED · Confidence: HIGH · Guidance: compact — the registry's shape should make adding an entry a one-place change (bc: extension trigger is the catalog's living mechanism).

**5. The card payload schema** — project-space · teleological · DEVELOP
Movement: specify zones/diff-marks/chips as platform-neutral semantic objects (no client markup), with composition budget rules.
WHY: T1+T6 survived; the payload is the consent-bearing artifact both clients render and §5.4 persists.
Priority: MED · Confidence: MED · Guidance: none.

**6. The two-client card prototype** — project-space · epistemic · TEST
Movement: render the acid cards as a real bot message + web mock; validate chip ergonomics, thinking-state, and the 4096 budget against actual clients.
WHY: the catalog's §5.3 freeze gate names this the unfreezing evidence; P7 IS the prototype.
Priority: MED · Confidence: MED · Guidance: compact — layout may adjust; consent rules may not (bc: catalog commits them).

**7. The off-flag parity contract** — project-space · epistemic · TEST
Movement: validate that backend=off renders content-equivalent to today's confirm summary across the enumerated fields (budget, slots×pay, audience+privacy-floor wording, deadline, mode, raw-statement warning).
WHY: T10-refined is the rollout's no-regression proof; the strongest de-risk found in the run.
Priority: MED · Confidence: HIGH · Guidance: none.

**8. The operator capability** — project-space · teleological · INVESTIGATE-FRONTIER
Movement: ship `OPERATOR_USER_IDS` + held-draft notification + resolve endpoint now; open the real admin/roles component when holds have traffic.
WHY: sensemaking's frame-exit catch — the hold path's operator did not exist anywhere; A6 invented the minimum.
Priority: MED · Confidence: MED · Guidance: compact — record the migration path (config list → roles table) in the BOM's open knobs (bc: throwaway-vs-seed ambiguity should be explicit).

**9. Draft data lifecycle** — project-space · epistemic · REFINE
Movement: sharpen retention policy: TTL knob (default off), cleanup script semantics, what hold/abandoned drafts may legally retain (PII posture).
WHY: critique's T7 prosecution landed (unbounded PII retention); the knob ships but the POLICY is unrefined.
Priority: MED · Confidence: MED · Guidance: none.

**10. Prompt-seed rendering** — project-space · teleological · INVESTIGATE-FRONTIER
Movement: turn the prompt-builder CONTRACT (this BOM) into the actual builder: registry + case files → system prompt, vendor-neutral.
WHY: recurring identity from the detections inquiry's route-map (its route 10); this inquiry deliberately bounded it to a contract (MQ4).
Priority: MED · Confidence: MED · Guidance: compact — needs case files first (the detections inquiry's route 9) (bc: few-shots are the prompt's substance).

**11. Detection-log → calibration loop** — project-space · teleological · INVESTIGATE-FRONTIER
Movement: wire log-derived per-entry miss/stet/abandon rates into the meta-definition's feedback register; revisit thresholds.
WHY: D8 existed as a dimension because the log is the calibration substrate; the loop is designed but unwired.
Priority: LOW-MED · Confidence: HIGH (that it's the path) · Guidance: none — blocked on real runs by nature.

**12. Replay/eval harness** — project-space · teleological · PURSUE-SEED
Movement: dev script replaying logged submissions against a new registry/prompt version, diffing results.
WHY: T13 deferred with gate "first registry/prompt change after ≥50 real runs"; the regression tool for canon evolution.
Priority: LOW-MED · Confidence: MED · Guidance: none.

**13. Real-vendor reference backend** — project-space · teleological · INVESTIGATE-FRONTIER
Movement: pick the reference vendor at implementation, build the structured-output adapter, run T15's manual smoke checklist.
WHY: A5's selector leaves the slot open; the BOM names protocol + one reference impl.
Priority: LOW-MED · Confidence: MED · Guidance: none.

**14. Async migration seam** — project-space · teleological · INVESTIGATE-FRONTIER
Movement: when volume demands, move the engine call to a background job behind the SAME endpoint contract (status polling already designed).
WHY: A4 committed sync-with-seam; T4's slow-sim test keeps the seam honest.
Priority: LOW · Confidence: HIGH · Guidance: none.

**15. Hold-path operations** — project-space · teleological · PURSUE-SEED
Movement: SLA wording, operator re-ping, hold-queue ergonomics — once holds have real traffic.
WHY: T14 deferred on operator practice data.
Priority: LOW · Confidence: MED · Guidance: none.

**16. Task-table draft merge** — project-space · teleological · PURSUE-SEED
Movement: at a future major migration, consider folding drafts into tasks once ALL consumers are status-aware by design.
WHY: K2's kill preserved this seed; the kill grounds (browse/my_tasks unguarded) are fixable design debts, not laws.
Priority: LOW · Confidence: LOW · Guidance: compact — revisit only with a consumer-audit in hand (bc: the kill was blast-radius, and the radius must be measured to be re-argued).

## Excluded

- **ToS-posture decision** — the prior inquiry's route 5; a product call that gates policy-floor WORDING, not this BOM's structure; engaging it here advances nothing the BOM needs (PROJECT.md → Open Decisions).
- **Case-file authoring / eval corpus content** — MQ4 exclusion; lives on the detections inquiry's route-map (routes 9/16).
- **Full admin/roles component design** — beyond the minimal gate; a future component with its own inquiry (route 8 records only the seam).
- **Vendor comparison shopping** — implementation-time choice behind a stable protocol; nothing structural turns on it now.
- **"Conclude the inquiry" / "implement now vs later"** — control-flow and disposition decisions, not concept-directions (NOT-list).

## Telemetry

- mode: root/project-space · entry: fresh
- identities: 16 · teleological 13 / epistemic 3 · high-priority 3
- individuations: 19 considered → 16 identities (3 lean-to-split kept separate: canon spine vs BOM document; parity contract vs client prototype; data lifecycle vs operator capability) · uncertain: 1 (canon spine could be read as a BOM manifestation — kept split per asymmetry; it has independent onward life at implementation) · stale: 0 (fresh)
- convergence: 2 sweep cycles; second yielded no new identities · frontier flags: none (territory compact, 7 artifacts)
- failure modes checked: LAYER 1 (Over-merge, Under-coverage, Wrong-grain, Goal-loss, Type-misassignment, Index-drift) + LAYER 2 (Selection-creep, Process-coupling, Description-collapse, Manifestation-dump) — none fired; disposition candidates routed to Excluded
- **Self-assessment: PROCEED**
