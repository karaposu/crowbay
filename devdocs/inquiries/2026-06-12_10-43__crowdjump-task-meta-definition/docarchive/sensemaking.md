# Sensemaking — Crowdjump Task Meta-Definition

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_10-43__crowdjump-task-meta-definition/_branch.md` — the articulated framing (4 considered articulations preserved; ambiguities at artifact-kind / normative-vs-descriptive / definedness-inclusion / consumer axes; MQ4 exclusions: no pipeline implementation, no code changes, broader pattern not the single Instagram instance). Operating over the Surfacing workspace (26 items, R1–R6).

---

## SV1 — Baseline Understanding

The ask reads as: produce a list of attributes (digital, achievable, recordable-via-screen-recording, plus others) that characterize a valid Crowdjump task, so that a future AI clarification pipeline can check submissions against the list and ask Launchers to fix what's missing.

---

## Phase 1 — Cognitive Anchor Extraction

**Constraints**
- C1 (economic): payment releases only on verified completion, and verification is screen-recording analysis — whatever a task is, its completion must be JUDGEABLE FROM A RECORDING (PROJECT.md loop; verification component design).
- C2 (structural): one task = `num_jumpers` identical slots × `you_earn` — the data model presumes a uniform, per-Jumper-repeatable unit of work (src/schemas/task.py).
- C3 (gap): the live contract constrains nothing about work content — `desc` is free text 1–5000 chars; task #2 ("...give me a boost") passed every existing check (wizard transcript).
- C4 (consumer): the deferred clarifier must be GENERATABLE from the definition — attributes must be individually testable, else no "is X clear?" questions can derive from them (user's stated dependency).
- C5 (policy): the ToS/task-category posture is an OPEN product decision (PROJECT.md Open Decisions) — the definition may name the dimension but cannot silently resolve it.
- C6 (capability): "verifiable" is bounded by the verification design envelope — visible UI actions, navigation, text entry, durations (SVI capability taxonomy); off-screen outcomes are outside it.

**Key Insights**
- KI1 (the central one): the user's seed attributes live at TWO DIFFERENT LOGICAL LEVELS. "Digital" and "recordable" are about a task's KIND — can this sort of thing be a Crowdjump task at all? "Achievable" and the example check "goal is clear?" are about an INSTANCE's specification quality — is THIS submission well-formed? The raw ask fuses two axes: **admissibility** (kind) and **definedness** (instance). A definition that conflates them produces a confused clarifier.
- KI2: in-project prior art exists — SVI's Task Specification Language already declares "without clear, unambiguous task definitions, the system cannot reliably determine if a task was completed" and sketches structured actions. The meta-definition is that document's MISSING UPSTREAM: TSL assumed a structured task arrives; nothing defines what makes one valid.
- KI3: task #2 PASSES the kind axis (liking photos is digital, recordable, performable) and FAILS the instance axis (goal vague — "a boost"; no target URL; no per-Jumper action spec; no completion criterion). The live failure is concentrated in definedness — evidence the definition must carry both axes to be useful.
- KI4: attributes are dependency-ordered: completion can't be observable unless actions are specified; actions can't be specified without a target; a target presupposes a goal. Attribute order = the clarifier's future question order.
- KI5: "achievable" is doing double duty — performable-by-an-ordinary-Jumper (skills/access) and bounded (finite, completable within one recording session).

**Structural Points**
- SP1: a task instance decomposes into (goal, target, per-Jumper actions, completion criterion, operational constraints, economics, audience, timing). The wizard already collects economics/audience/timing competently — the under-defined quadrant is exactly goal/target/actions/completion (SP3).
- SP2: four consumers — AI clarifier (instance checks), launch gate (kind checks), product vocabulary (humans), verification component (consumes completion criterion downstream).

**Foundational Principles**
- FP1: the three-verifications identity (verified humans / attributes / work) — the task definition serves "verified work."
- FP2: marketplace trust requires a Jumper to know exactly what to do BEFORE jumping.
- FP3: path tolerance (SVI philosophy) — define outcomes and observables, not pixel-exact paths.

**Meaning-Nodes:** task-ness · admissibility · definedness · verifiability · observability · atomicity.

### SV2 — Anchor-Informed Understanding

Not a flat attribute list: a **two-axis attribute system** — KIND-admissibility attributes (is this sort of work allowed to be a Crowdjump task?) and INSTANCE-definedness attributes (is this submission specified well enough to perform and verify?) — with dependency ordering that will later drive clarification order.

*(H4/H5 check after SV2: "admissibility"/"definedness" — definedness matches the user's own words ("what makes a task defined or not"); admissibility is loop-coined, kept with a plain-language alias ("allowed kind"). Motivating example = task #2; pattern-widening handled at A7.)*

---

## Phase 2 — Perspective Checking

- **Technical/Logical:** an attribute is only useful to the clarifier if it carries a satisfaction condition evaluable against the submission (free text + structured fields). The gate wants binary; the clarifier wants graded-plus-question. → New anchor: **every attribute is a triple (definition, satisfaction test, clarifying-question template)**.
- **Human/User:** Launchers think in outcomes ("give me a boost"), not specs — the definition must not demand spec-writing skill; the clarifier translates. Jumper side yields an operationalization: **a task is defined iff a stranger Jumper could perform it and prove it without asking a single question**. (New anchor — the Jumper-comprehensibility test.)
- **Strategic/Long-term:** the definition is the quality moat, but an over-strict gate kills task supply at MVP. → Posture anchor: **hard gate on the kind axis, soft clarify-and-confirm on the instance axis** — which matches the user's pipeline vision (confirm or clarify, not reject).
- **Risk/Failure:** (a) silently resolving the ToS posture inside the definition would smuggle a product decision — the policy attribute must carry an explicit OPEN parameter; (b) over-formalization risks Launcher abandonment; (c) **discovered attribute**: tasks demanding the Launcher's credentials or private-surface access ("log into my account and...") are unverifiable AND a safety hazard — self-containment / no-credential-transfer belongs on the kind axis.
- **Resource/Feasibility:** satisfaction tests must run as cheap LLM judgments on the submission alone at launch time — no external crawling at MVP.
- **Ethical/Systemic:** the legal/policy dimension is namable now even though its VALUE is open (C5): lawful + non-harmful are floor; target-platform-ToS posture is the open parameter.
- **Definitional/Internal Consistency:** PROJECT.md's loop already implicitly defines task-as-performable-verifiable-payable; the two-axis definition refines rather than contradicts. The seeds distribute cleanly across the axes (digital/recordable → kind; achievable/goal-clear → instance) — supporting KI1.
- **Definitional/Frame-exit Completeness** (gating fires — "task" is used at two levels inside this inquiry's own structure): project-wide referents of "task": (a) the Task DB row / lifecycle object; (b) task-as-work-content (what a Jumper does); (c) task-as-submission (what a Launcher writes); (d) incidental uses (asyncio/pytest "tasks") — irrelevant. The definition targets (b)+(c). Role assessment: (a) is the downstream CONTAINER — coherence preserved by relocating it to the Structural layer per `_branch.md`'s Layer Commitment, not by forcing it in. Verdict rigor on surfacing's confirmed-absent regions: counter — "payments matter to task-ness because tasks must be fundable"; tested: economics already enters via SP1/C2 (priced, per-Jumper uniform); the wallet PLUMBING adds nothing definitional. Holds.
- **Phase/Calibration-State** (required — phase-dependent rules present): "verifiable" depends on a verification capability that is DESIGNED but not BUILT. Early-stage default: define verifiability against the design envelope (SVI taxonomy) and mark the attribute **capability-versioned** — the envelope will widen; the attribute's test cites the envelope rather than hard-coding today's list. (New anchor.)

### SV3 — Multi-Perspective Understanding

Three structural expansions over SV2: (1) attributes are triples — definition + test + question — making the clarifier derivable by construction; (2) two attributes the seeds missed: **self-containment** (no credential transfer / public-surface work) and **capability-versioned verifiability**; (3) posture split — kind axis gates hard, instance axis clarifies softly. Plus the Jumper-comprehensibility test as the definedness axis's unifying operationalization.

---

## Phase 3 — Ambiguity Collapse

#### Ambiguity A1: artifact-kind / consumer (human ontology vs machine-consumable schema vs launch gate — variants 1/2/3/4)
**Strongest counter-interpretation:** write the prose ontology only (variant 1); schemas and gates are implementation, deferred with the pipeline.
**Why the counter fails (structural):** the user's stated dependency — "to generate these first we need to meta define" — makes the definition the GENERATOR of definedness checks. Prose without per-attribute satisfaction tests cannot mechanically generate anything; the deferred pipeline would have to re-derive structure, recreating this inquiry. The triple form costs one extra field per attribute and serves all four consumers (SP2) simultaneously.
**Confidence:** HIGH.
**Resolution:** the meta-definition is consumer-neutral content in **triple form** — per attribute: definition, satisfaction test, clarifying-question template — rendered as a devdocs document (Meaning layer; no code).
**Now fixed:** attribute = (name, definition, test, question). **No longer allowed:** prose-only ontology; writing code/schema now. **Depends on this:** Innovation's attribute design; the future clarifier BOM. **Model change:** variants 2 and 4 merge into the committed shape; variants 1 and 3 survive as RENDERINGS (doc view; gate view) of the same content.

#### Ambiguity A2: normative vs descriptive
**Strongest counter-interpretation:** a descriptive ontology of what tasks ARE is the safer "meaning-layer" artifact; norms belong to policy.
**Why the counter fails (structural):** there is no existing task population to describe — the platform is pre-launch; the only described instance would be task #2, the failure case. Every consumer (gate, clarifier, vocabulary) needs criteria, not census. A description would canonize the gap.
**Confidence:** HIGH.
**Resolution:** **normative** — the definition states what qualifies as a valid Crowdjump task.
**Now fixed:** "is a Crowdjump task" = satisfies the admissibility attributes; "is defined" = satisfies the definedness attributes. **Excluded:** descriptive census framing. **Depends:** gate semantics; clarifier semantics. **Model change:** the definition becomes testable membership, not observation.

#### Ambiguity A3: definedness-inclusion ("but this later")
**Strongest counter-interpretation:** the user explicitly deferred definedness ("goal is clear? etc but this later") — deliver only the kind-level definition.
**Why the counter fails (structural):** read against its own sentence, "this later" defers GENERATING the checks/pipeline (the AI consumer + confirmation text), while "we have to have meta definition of what makes a task defined or not" names definedness as part of the needed meta-layer. Structurally: KI3 shows the live failure is ENTIRELY on the instance axis — a kind-only definition would judge task #2 valid and the inquiry would answer the question while missing its goal (the `_branch.md` Scope Check watch-point). The triple form includes question templates WITHOUT building the pipeline, honoring the deferral.
**Confidence:** HIGH (textual counter acknowledged; structural ground decisive).
**Resolution:** include BOTH axes; per-attribute question templates included; pipeline implementation excluded.
**Now fixed:** two-axis scope. **Excluded:** kind-only definition; any pipeline/code work. **Depends:** the clarifier BOM consumes the question templates as its seed inventory. **Model change:** "definedness" becomes a first-class half of the definition, not a later appendix.

#### Ambiguity A4 (load-bearing seed test): "achievable"
**Strongest counter-interpretation:** keep "achievable" as one attribute — it's the user's own word.
**Why the counter fails (structural):** as a single predicate it is untestable — achievable BY WHOM and WITHIN WHAT? Two independent failure modes hide inside it: requires-special-position (skills/assets/access an ordinary verified Jumper lacks) and unbounded-effort (no finite completion within a recording session). One question template can't repair both.
**Confidence:** HIGH.
**Resolution:** split into **performable** (by an ordinary verified Jumper, with only their own accounts/devices) and **bounded** (finite unit completable within one recording session).
**Now fixed:** the split. **Excluded:** monolithic "achievable." **Depends:** clarifier question design. **Model change:** seed attributes are inputs to be DECOMPOSED, not copied.

#### Ambiguity A5 (load-bearing seed test; proxy-vs-structural): "recordable via screen recording"
**Strongest counter-interpretation:** keep literal recordability — the user's words; a Jumper can always record their screen.
**Why the counter fails (structural):** literal recordability is trivially true of any on-screen activity and therefore discriminates nothing — task #2 is perfectly recordable yet unverifiable, because "a boost" never APPEARS on screen. Recordability is a proxy; the structural requirement is that the task's COMPLETION CRITERION be observable within the recording (C1) and inside the capability envelope (C6).
**Confidence:** HIGH.
**Resolution:** the kind-axis attribute is **verifiability-in-principle** (this sort of work produces on-screen observable completion); the instance-axis attribute is **completion-criterion-observability** (THIS task names an observable end state). "Recordable" survives as the plain-language gloss.
**Now fixed:** observable-completion as the real test. **Excluded:** recordability-as-attribute. **Depends:** verification component contract. **Model change:** the definition's center of gravity moves from recording (medium) to observability (evidence).

#### Ambiguity A6 (hidden assumption): task heterogeneity
**Strongest counter-interpretation:** a task could be a heterogeneous bundle ("3 people like + 1 person writes a review").
**Why the counter fails (structural):** the entire data model (uniform `you_earn` × `num_jumpers`), matching, and the planned differential-pay extension (rate groups over the SAME unit) presume one uniform per-Jumper unit; verification verifies one unit-shape per task. Bundles are expressible as multiple tasks.
**Confidence:** HIGH.
**Resolution:** **atomicity** — a task specifies exactly one per-Jumper unit of work, identical across slots.
**Now fixed:** one unit per task. **Excluded:** bundle-tasks. **Depends:** clarifier ("this looks like two tasks — split?"). **Model change:** adds the eighth-ish attribute the seeds never hinted at.

#### Ambiguity A7 (specific-vs-pattern cue): is the definition shaped by task #2?
**Strongest counter-interpretation:** the attribute set fits engagement tasks (the example) but misses the wider task universe.
**Why the counter fails (structural):** the attributes derive from platform invariants (C1, C2, C6, economics) — not from the example's content; cross-checking against SVI's task taxonomy (forms, navigation, content creation, engagement-with-duration, transactions) each type maps onto goal/target/actions/observable-completion without new attribute-kinds. The example is the test instance, not the source.
**Confidence:** HIGH.
**Resolution:** attribute set sourced from invariants; task #2 retained only as acid test.

*(H8 self-reference check: this inquiry uses an articulation discipline to define task-definedness — shared conceptual language. External grounding applied: every attribute is anchored in platform mechanics (schema fields, verification design, escrow economics), not in articulation vocabulary.)*

### SV4 — Clarified Understanding

A normative, two-axis, triple-form definition. KIND axis (gate-hard): digital; performable-on-public-surface without credential transfer (self-contained); policy-permissible (lawful/non-harmful floor; platform-ToS posture an explicit OPEN parameter); verifiable-in-principle (capability-versioned). INSTANCE axis (clarify-soft): goal-clear; target-identified; actions-specified; completion-criterion-observable; performable; bounded; atomic. No longer viable: flat single-axis lists; prose-only; descriptive framing; literal-recordability; monolithic achievability; bundle-tasks; resolving ToS inside the definition.

---

## Phase 4 — Degrees-of-Freedom Reduction

**Fixed variables:** two axes with distinct enforcement postures (gate vs clarify); triple form per attribute; dependency order goal → target → actions → completion-criterion on the instance axis; capability-versioned verifiability; ToS posture as named-but-open parameter; the Jumper-comprehensibility test as the instance axis's summary criterion; attribute count lands ~11 (4 kind + 7 instance) subject to Innovation's shaping.

**Eliminated:** building any pipeline/code; per-attribute external data fetches at test time; treating the wizard's existing fields (economics/audience/timing) as missing — they are already collected and join the definition as the well-specified region (SP3).

**Remaining freedom (Innovation's space):** attribute naming and grouping; the question-template pattern per attribute; whether instance-definedness aggregates to a score or a checklist; how the definition document is organized for its four consumers; extension/versioning convention for future attributes.

### SV5 — Constrained Understanding

The solution space is now: design ~11 attribute triples across two fixed axes with fixed posture semantics and fixed dependency order, organized for four consumers, with two parameters explicitly left open (ToS posture value; capability envelope version). Innovation explores within that frame only.

---

## Phase 5 — Conceptual Stabilization

*(Accommodation check: perspectives stopped destabilizing after Risk and Phase/Calibration added their anchors — later perspectives confirmed; no patch-loop; stabilization is earned, not forced.)*

### SV6 — Stabilized Model

**A Crowdjump task is a normative, two-axis concept:**

1. **Admissible KIND** — the work is digital; performable on a public platform surface by an ordinary verified Jumper using only their own accounts and devices (self-contained — no credential transfer); policy-permissible (lawful and non-harmful as floor; target-platform-ToS posture an explicitly open product parameter); and verifiable-in-principle — work of this sort produces on-screen observable completion within the platform's (capability-versioned) verification envelope. The kind axis GATES.

2. **Defined INSTANCE** — the submission specifies: a clear goal; an identified target; the per-Jumper actions; an observable completion criterion; and the unit is performable, bounded (one recording session), and atomic (one uniform unit per Jumper). The instance axis CLARIFIES — its summary criterion is the Jumper-comprehensibility test: a stranger Jumper could perform and prove the task without asking anything. Each attribute is a triple (definition, satisfaction test, clarifying-question template), which is what makes the deferred clarification pipeline generatable from the definition rather than designed from scratch.

**Difference from SV1:** SV1 imagined one flat attribute list. SV6 commits to two axes with opposite enforcement postures; replaces two seed attributes with their structural cores (recordable → observable-completion; achievable → performable + bounded); adds two attributes the seeds missed (self-containment, atomicity); orders the instance attributes into the clarifier's future question order; and keeps two parameters explicitly open instead of silently resolved (ToS posture; capability envelope).

**OPEN (flagged, not dropped):** ToS posture value (product decision); final attribute names/grouping (Innovation); checklist-vs-score aggregation (Innovation/Critique); capability envelope versioning convention (Structural layer, later).

**Saturation telemetry:** perspectives 9 (3 produced NEW anchor types — Risk, Phase/Calibration, Human/User); ambiguities: 7 collapsed (all HIGH), 4 explicitly OPEN; SV6-vs-SV1 delta: structural (axes, postures, triple form — not cosmetic); anchor diversity: all five anchor types from ≥4 perspectives.
