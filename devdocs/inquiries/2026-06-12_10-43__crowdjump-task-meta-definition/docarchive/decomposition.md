# Decomposition — Crowdjump Task Meta-Definition

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_10-43__crowdjump-task-meta-definition/_branch.md` — decomposing the whole as stabilized by `sensemaking.md` SV6: a normative, two-axis (kind gates / instance clarifies), triple-form (definition / test / question) meta-definition of a Crowdjump task, with two open parameters (ToS posture; capability envelope) and a dependency-ordered instance axis.

## Step 1 — Coupling Map

Elements: kind-axis attribute content (4 attributes) · instance-axis attribute content (7 attributes) · triple-form template · enforcement-posture semantics (gate/clarify) · definedness aggregation shape · instance-attribute ordering · open-parameter handling (ToS, capability envelope) · acid-test examples · consumer readings · extension/versioning convention.

**Clusters (high internal coupling):**
- **A — Form contract:** triple template + posture semantics + aggregation shape. Change any and every attribute entry changes → they move together.
- **B — Kind-axis content:** the 4 admissibility attributes; the two open parameters live INSIDE two of its entries (policy-permissible carries the ToS parameter; verifiable-in-principle carries the envelope reference).
- **C — Instance-axis content + ordering:** the 7 definedness attributes and their check order — ordering is meaningless apart from the attributes it orders.
- **D — Acid tests:** worked examples (task #2; per-SVI-type passes; kind-rejections). Consumes everything, constrains nothing upstream at build time.
- **E — Consumption & evolution:** per-consumer reading notes + extension convention. Pure consumer of A–C.

**Valleys (low coupling, natural boundaries):** A|B and A|C — once the template is fixed, content pieces consume it as a contract with no back-traffic. B|C — different postures, different anchor sources; ONE moderate crossing: the observability bridge (kind's verifiable-in-principle defines the envelope the instance's completion-criterion test cites). D and E sit behind one-way boundaries.

## Step 2 — Boundaries (Top-Down)

Five pieces: P1 form contract · P2 kind axis · P3 instance axis (+ ordering) · P4 acid tests · P5 consumption & evolution. The B|C crossing is single-point (envelope citation) — boundary holds with an explicit interface rather than a merge.

## Step 3 — Bottom-Up Validation

Atoms: 11 attribute entries; 3 template fields; 2 posture rules; 1 aggregation choice; 1 ordering; 2 open parameters; ~7 examples; 4 consumer notes; 1 extension rule. Grouping check: attributes split 4/7 along the axes exactly as Step 2 drew them ✓; template fields + postures + aggregation cohere in P1 ✓; open-parameter VALUES sit inside P2 entries while the versioning CONVENTION generalizes into P5 — overlap resolved by that split ✓; examples → P4 ✓. No atom is split by a boundary; no independent atoms are forced together. **Confidence: HIGH on all five boundaries** (top-down and bottom-up agree; B|C noted as the only moderate-traffic edge).

## Step 4 — Question Tree

- **Q1 (P1): What is the canonical form of a task attribute, and what do satisfaction and failure mean on each axis?**
  - [ ] Triple template defined: per attribute — definition, satisfaction test (LLM-judgment predicate over the submission alone), clarifying-question template
  - [ ] Kind-axis semantics: failure GATES (task not admissible), wording for rejection
  - [ ] Instance-axis semantics: failure CLARIFIES (question fired, confirm-or-fix), never silent rejection
  - [ ] Aggregation shape chosen: checklist vs graded score for definedness
  - [ ] Template applies identically to both axes (one form, two postures)

- **Q2 (P2): Which attributes make a KIND of work admissible as a Crowdjump task?**
  - [ ] `digital` triple
  - [ ] `self-contained` triple (public surface; no credential transfer)
  - [ ] `policy-permissible` triple — lawful/non-harmful floor; target-platform-ToS posture marked OPEN with parameter slot
  - [ ] `verifiable-in-principle` triple — cites the capability envelope by reference (capability-versioned)
  - [ ] Every test evaluable from the submission text + structured fields alone (no external fetches)

- **Q3 (P3): Which attributes make a task INSTANCE defined, and in what order are they checked?**
  - [ ] Triples for: `goal-clear`, `target-identified`, `actions-specified`, `completion-criterion-observable`, `performable`, `bounded`, `atomic`
  - [ ] Dependency order stated: goal → target → actions → completion-criterion (then performable/bounded/atomic)
  - [ ] Jumper-comprehensibility test stated as the axis's summary criterion
  - [ ] Each question template written as Launcher-facing text (plain language, no jargon)

- **Q4 (P4): Does the definition discriminate correctly on real cases?**
  - [ ] Task #2 ("check my instagram page and like photos to give me a boost") passes ALL kind attributes and fails exactly: goal-clear, target-identified, actions-specified, completion-criterion-observable
  - [ ] A repaired rewrite of task #2 passes both axes
  - [ ] One passing example per SVI task type (form-fill, navigation, content creation, engagement-with-duration)
  - [ ] ≥2 kind-rejections fail at the intended attribute (credential-transfer case → self-contained; off-screen-outcome case → verifiable-in-principle)

- **Q5 (P5): How do the four consumers read the definition, and how does it evolve?**
  - [ ] Reading note per consumer: clarifier (instance triples → question inventory), launch gate (kind triples), product vocabulary (definitions), verification component (completion-criterion contract)
  - [ ] Extension convention: adding an attribute = adding a triple + version note
  - [ ] Open-parameter register: ToS posture; capability envelope version

Independence check: each question is answerable without reading sibling pieces, given the interfaces below. ✓

## Step 5 — Interface Map

| From | To | What flows | Direction |
|---|---|---|---|
| P1 | P2 | triple template + gate semantics (contract) | one-way |
| P1 | P3 | triple template + clarify semantics + aggregation (contract) | one-way |
| P2 | P3 | observability bridge: the capability-envelope reference that `completion-criterion-observable`'s test cites | one-way |
| P2, P3 | P4 | the 11 attribute triples (data) | one-way |
| P4 | P2/P3 | DV2 trigger only — an acid-test failure reopens the failing attribute | feedback, not build-order |
| P1, P2, P3 | P5 | template + attribute inventory + parameter slots | one-way |

**Assumptions-not-data check:** P3 assumes P1's clarify semantics fire PER attribute (stated in Q1 criterion 3, not left implicit). P4 assumes satisfaction tests yield stable pass/fail on examples — made explicit: Q1's test field defines tests as LLM-judgment predicates WITH stated expected outcomes. P5 assumes attribute names are final — ordering puts P5 last. No unstated timing/state coupling found.

## Step 6 — Dependency Order

```
P1 (form contract)
 ├─→ P2 (kind axis) ──────────────┐
 ├─→ P3 (instance axis) ←─ envelope ref from P2 (single late-join citation)
 │        (P3 may start in parallel after P1; completes after P2's envelope ref exists)
 └────────────────────────────────┴─→ P4 (acid tests) ─→ P5 (consumption & evolution)
```

No circular dependencies (P4→P2/P3 is a revision trigger, not a build input).

## Step 7 — Self-Evaluation (full, 7 dimensions)

| Dimension | Verdict | Note |
|---|---|---|
| Independence | PASS | each Q answerable alone via the contracts |
| Completeness | PASS | every SV6 commitment lands in a piece: axes (P2/P3), triples+postures+aggregation (P1), ordering+Jumper-test (P3), open params (P2/P5), examples (P4), consumers+versioning (P5) |
| Reassembly | PASS | P1 form + P2/P3 content + P4 validation + P5 consumption = the complete meta-definition document; determination-mechanism check: the two runtime-ish determinations (envelope citation; aggregation shape) each have a home (Q2 / Q1) |
| Tractability | PASS | each piece is a single focused pass |
| Interface clarity | PASS | all flows explicit incl. the one moderate B|C bridge |
| Balance | PASS (noted) | P3 is the largest (7 triples + ordering) at roughly 2–3× P1 — within tolerance, flagged for Innovation to keep P3's entries lean |
| Confidence | HIGH | top-down and bottom-up agreed on all five boundaries |

**Stopping criterion met:** all five pieces are tractable; no recursive decomposition needed.
