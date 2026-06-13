# Decomposition — Task-Consumer LLM Detections & Scenarios

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/_branch.md` — decomposing the whole stabilized by `sensemaking.md` SV6: a three-part operational catalog (three-class detection inventory · four scenario archetypes under the one-card rule · output contract with normalizer role), with provisional thresholds and calibration-by-design.

## Step 1 — Coupling Map

Elements: detection entry schema · severity/uncertainty semantics · class execution order + short-circuit rule · channel-class content · kind-class content · instance-class content · composition checks · archetype definitions + worst-severity keying · one-card rendering (diff restatement, question cap) · thin-submission variant · revision loop · normalized-slot output · detection-log schema · declined-output shape · acid/eval cases · calibration + extension conventions.

**Clusters:**
- **A — Detection framework:** entry schema + severity/uncertainty semantics + ordering/short-circuit. Change any → every entry changes; they move together.
- **B1 — Channel class** (submission-as-input hygiene) · **B2 — Kind class** (gate attributes) · **B3 — Instance + composition class** (clarify attributes + cross-attribute checks). Strong coupling WITHIN each class (shared source authority); weak BETWEEN classes (order only). Composition checks consume instance results → they live with B3.
- **C — Scenario layer:** archetypes + keying + one-card rules + thin-submission + revision loop. Consumes severities (from A) and result LISTS (from B*), not entry internals.
- **D — Output contract:** normalized slots + detection log + declined shape. Consumes B3's slot proposals and A's schema.
- **E — Validation & evolution:** acid/eval cases + calibration/extension conventions. Pure consumer.

**Valleys:** A|B\* (schema as contract, one-way once fixed) · B\*|C (uniform result-object lists — the single biggest flow, but uniform) · B3|D (slot values) · everything|E (one-way).

## Step 2 — Boundaries (Top-Down)

Seven pieces: P1 framework · P2 channel class · P3 kind class · P4 instance+composition class · P5 scenario layer · P6 output contract · P7 validation & evolution.

## Step 3 — Bottom-Up Validation

Atoms: ~15 detection entries (channel ~4, kind ~4, instance 7 + composition ~4), schema fields, 3 severities + uncertainty routing, ordering/short-circuit decision, 4 archetypes, card rules + question cap, thin-submission variant, revision loop, 2+1 contract shapes, log schema, acid set, 2 conventions. All group exactly into the seven pieces; the worst-severity-keying atom sits in the scenario layer consuming the framework's severity definitions; the short-circuit atom sits in the framework. No atom split by a boundary. **Confidence: HIGH on all boundaries** (the B\*→C edge carries the most traffic but over a uniform interface).

## Step 4 — Question Tree

- **Q1 (P1): What is a detection, formally — schema, severities, uncertainty, ordering?**
  - [ ] Entry schema fixed: {name, version, class, source-attribute(s), trigger, severity gate|clarify|warn, result clear|fired|uncertain, proposal (typed per slot, required for slot-bearing detections), question, transform}
  - [ ] Severity semantics defined incl. response obligations (gate→decline path; clarify→question/proposal; warn→card notice, non-blocking)
  - [ ] Uncertainty routing: policy-floor uncertain → conservative hold; all other uncertain → ask
  - [ ] Class order channel → kind → instance/composition + the short-circuit decision (does a fired gate suppress instance findings or annotate them?)
  - [ ] Naming/versioning convention (ties to meta-definition extension convention)

- **Q2 (P2): Which channel-class detections run on the raw submission, first?**
  - [ ] Injection/instruction-content detection (desc tries to steer the LLM)
  - [ ] Language detection + handling stance
  - [ ] Degenerate-input detection (too short / paste-dump / non-task text)
  - [ ] Each: trigger + severity + response; runs-first justification per entry

- **Q3 (P3): Which kind-class detections enforce the four gate attributes?**
  - [ ] non-digital · credential-transfer/non-self-contained · policy-floor (with ToS-posture parameter slot) · unverifiable-in-principle
  - [ ] Decline-with-named-reason wording per entry + repair suggestion where repairable (e.g., descope the credential part)
  - [ ] Conservative-uncertainty bias applied to the policy floor specifically

- **Q4 (P4): Which instance + composition detections produce the rewrite proposal?**
  - [ ] Seven attribute-derived detections (goal/target/actions/completion/performable/bounded/atomic), each with slot-proposal behavior
  - [ ] Composition: non-unit/splitability (the user's anchor example, with split-transform), contradiction (desc vs structured fields), over-specification (path-tolerance warn), thin-submission aggregate trigger
  - [ ] Each entry names its slot(s) and transform template where repairable

- **Q5 (P5): How do fired detections compose into ONE interaction?**
  - [ ] Four archetypes (confirm / clarify-propose / suggest-transform / decline-with-reason) keyed by worst fired severity
  - [ ] One-card layout: diff-style normal-form restatement + inline proposals + ≤3 blocking questions (provisional) + warnings
  - [ ] Thin-submission variant (one re-description ask, clarify-shaped)
  - [ ] Revision loop semantics (Launcher edits → re-run; convergence expectation)
  - [ ] Approval semantics: what exactly approval commits (the structured reading; the binding pair freeze notice)

- **Q6 (P6): What does the consumer output?**
  - [ ] Approved shape: original desc + normalized slots (structured location, actions list, completion criterion, bound) + approval record
  - [ ] Detection log schema (per run: results, resolutions)
  - [ ] Declined shape: named rule + suggestion
  - [ ] Consumer mapping: matching (location), verification (criterion), Jumper display (clean text), feedback register (log)

- **Q7 (P7): How is the catalog validated and evolved?**
  - [ ] Acid set: task #2 (clarify-propose), repaired #2 (confirm), non-unit example (suggest-transform), credential case + off-screen case (decline), injection case (channel)
  - [ ] Eval = archetype × case matrix
  - [ ] Calibration convention: every numeric knob provisional, log-driven revision
  - [ ] Extension convention: new detection = full entry + version note

Independence check: each question answerable alone given the interfaces. ✓

## Step 5 — Interface Map

| From | To | What flows | Direction |
|---|---|---|---|
| P1 | P2, P3, P4 | entry schema + severity/uncertainty semantics (contract) | one-way |
| P1 | P5 | severity definitions + ordering/short-circuit (keying basis) | one-way |
| P2 | P5 | channel results (may preempt the card entirely — injection path) | one-way |
| P3, P4 | P5 | uniform detection-result lists | one-way |
| P4 | P6 | slot proposals/normalizations | one-way |
| P1 | P6 | log schema base | one-way |
| P3, P4 | P6 | named rules for the declined shape | one-way |
| P1–P6 | P7 | test subjects | one-way |
| P7 | P2–P6 | DV2 trigger only (acid failure reopens the entry) | feedback |

**Assumptions-not-data check:** P5 assumes uniform result objects across classes — stated in Q1's schema criterion, not implicit. P6 assumes slot-bearing detections return VALUES, not just verdicts — made explicit via Q1's typed `proposal` field. P5 assumes the short-circuit decision exists — parked in Q1 deliberately. P7 assumes the archetype set is closed — Q5 commits it. No unstated timing/state coupling found.

## Step 6 — Dependency Order

```
P1 (framework)
 ├─→ P2 (channel) ─┐
 ├─→ P3 (kind) ────┼─→ P5 (scenario layer) ─→ P7 (validation & evolution)
 ├─→ P4 (instance+composition) ─→ P6 (output contract) ─┘
 │        (P2–P4 parallel after P1; P5 completes after all three;
 └─        P6 after P4+P1; P7 last)
```

No circular dependencies (P7's arrows are revision triggers, not build inputs).

## Step 7 — Self-Evaluation (full, 7 dimensions)

| Dimension | Verdict | Note |
|---|---|---|
| Independence | PASS | contracts carry all cross-piece needs |
| Completeness | PASS | every SV6 commitment has a home: schema/severities/uncertainty/order (P1), three classes (P2–P4), archetypes/card/thin/revision (P5), normalizer contract + log (P6), acid/calibration/extension (P7), provisional thresholds (P1+P7), policy bias (P1 routing + P3), diff restatement (P5) |
| Reassembly | PASS | framework + inventory + interaction + contract + validation = the catalog; determination mechanisms placed (worst-severity keying in P5 over P1 semantics; uncertainty routing in P1) |
| Tractability | PASS | each piece is one focused pass |
| Interface clarity | PASS | uniform result-object interface explicit; typed proposal field explicit |
| Balance | PASS (noted) | P4 ≈ 2.5× P2 (eleven entries vs three-four) — within tolerance; Innovation keeps entries lean |
| Confidence | HIGH | top-down and bottom-up agree on all seven boundaries |

**Stopping criterion met:** all pieces tractable; no recursive decomposition needed.
