---
status: active
model: claude-fable-5
effort: max
---
# Finding: Crowdjump Task Meta-Definition

## Question

From the inquiry's framing (`_branch.md`): **create a meta-definition of what a Crowdjump task is, using attributes** (the user's seed attributes: achievable, recordable via screen recording, digital, "and other attributes"). The motivating incident: a live task — "check my instagram page and like photos to give me a boost" — passed the launch wizard with zero challenge, because nothing in the system knows what a well-formed task is. The user explicitly deferred building the clarification pipeline itself ("but this later"); this inquiry's deliverable is the definitional foundation that pipeline will later be generated from.

The framing preserved four plausible readings of the ask — a human-readable ontology, a machine-consumable schema, a launch-time acceptance gate, and a definition-plus-derived-definedness-questions — and the pipeline was required to address the set, not pick one early.

## Finding Summary

- A Crowdjump task is defined by **eleven attributes on two axes**: four **kind** attributes that say whether this sort of work can be a Crowdjump task at all (digital, self-contained, policy-permissible, verifiable-in-principle), and seven **instance** attributes that say whether this particular submission is specified well enough to perform and verify (goal-clear, target-identified, actions-specified, completion-criterion-observable, performable, bounded, atomic).
- Every attribute is a **triple**: a definition, a satisfaction test (answerable by reading the submission alone), and a clarifying-question template. The triples are what make the future AI clarification pipeline *generatable from* the definition instead of designed from scratch — which was the user's stated reason for wanting the definition first.
- Each attribute carries an **enforcement flag** with axis-derived defaults: kind attributes **gate** (failing means the task is not admissible), instance attributes **clarify** (failing fires the attribute's question back to the Launcher — confirm or fix, never silent rejection).
- The definition includes a **task normal form** — "*[Do action(s)] on [target] until [observable end-state], by any matching Jumper, within [bound]*" — whose slots map to the instance attributes. Definedness is operationally slot-filling; the form is the canonical *rendering* of a defined task, not a required input format.
- Two product parameters are deliberately left **open**, not silently resolved: the target-platform Terms-of-Service posture (inside policy-permissible) and the verification capability envelope version (inside verifiable-in-principle).
- The four readings preserved by the framing all survive as **renderings of one artifact**: the registry's definitions serve the ontology reading, the tests serve the schema reading, the kind flags serve the gate reading, and the question templates serve the definedness reading.
- The definition answers the motivating incident precisely: the Instagram "boost" task **passes every kind attribute and fails four instance attributes** (goal, target, actions, completion criterion) — confirming the platform's live failure is under-specification, not inadmissible work.

## Finding

Crowdjump pays verified humans for verified digital work; payment releases only when screen-recording analysis can judge completion. The platform's central noun — "task" — had no definition: the data model constrains money math but accepts any free text as work content. The definition below is **normative** (it states what qualifies, because there is no healthy task population to describe yet) and lives at the **meaning layer** (no code, no pipeline — those are explicitly later layers).

### 1. The two axes

**Axis 1 — Admissible kind** (default enforcement: GATE — a failing task is not accepted; wording must say why). Asks: can this *sort* of work be a Crowdjump task?

**Axis 2 — Defined instance** (default enforcement: CLARIFY — a failing attribute fires its question back to the Launcher; never silent rejection). Asks: is *this* submission specified well enough that a stranger Jumper could perform it and prove it without asking anything? That stranger-Jumper test is the axis's summary criterion.

Enforcement is recorded per attribute (a gate/clarify flag with the axis defaults above), so future exceptions — say, escalating a policy concern from clarify to gate — are flag changes with a version note, not restructurings.

### 2. The kind attributes (gate)

| Attribute | Definition | Satisfaction test (reads the submission only) | Example violation |
|---|---|---|---|
| **digital** | The work happens entirely on internet-connected devices and services | Does the described work occur on-screen, on digital platforms? | "hand out flyers downtown" |
| **self-contained** | Performable by an ordinary verified Jumper using only their own accounts and devices, on public platform surfaces — no credential transfer, no access to the Launcher's accounts | Does the text require logging into someone else's account, or access beyond public surfaces? | "log into my account and clean my inbox" |
| **policy-permissible** | Lawful and non-harmful as a floor; the target-platform ToS posture is an explicit OPEN parameter pending the product decision recorded in PROJECT.md's Open Decisions | Does the work fall into a prohibited category (illegal activity, harassment, deception targeting individuals, …)? *ToS-posture slot applied here when decided* | "post a review claiming you bought it" (deception — also the posture's hardest case) |
| **verifiable-in-principle** | Work of this kind produces completion observable through the platform's approved evidence channel — currently screen recording, capability-versioned against the verification design (SemanticVideoInspector docs) | Could completion of this sort of work be visible within a recording session? | "make my song famous" (the outcome never appears on-screen) |

Gate questions still get phrased helpfully (e.g., "Crowdjump tasks must be doable entirely on a screen — can yours be?") because even a gate should teach, but a kind failure ends the launch.

### 3. The instance attributes (clarify), in clarification order

The first four are dependency-ordered — actions can't be specified without a target; a completion criterion presupposes actions — and that order is the future clarifier's question order:

| # | Attribute | Definition | Clarifying-question template |
|---|---|---|---|
| 1 | **goal-clear** | The underlying intent is stated well enough to disambiguate everything below | "What outcome do you want from this task?" |
| 2 | **target-identified** | The exact object of work is named (URL, handle, app screen) | "Which exact page/profile/app should Jumpers open? Paste the link or handle." |
| 3 | **actions-specified** | The per-Jumper actions are enumerated | "What exactly should each Jumper do, step by step?" |
| 4 | **completion-criterion-observable** | An on-screen end state is named — "done" is visible | "What will be visible on the Jumper's screen when the task is complete?" |
| 5 | **performable** | An ordinary verified Jumper can do it with their own accounts and skills | "Does this need any special account, skill, or access beyond your audience filters?" |
| 6 | **bounded** | Finite; completable within one recording session | "Can one Jumper finish this in a single sitting? Roughly how long?" |
| 7 | **atomic** | Exactly one uniform unit of work per Jumper, identical across slots | "Is this the same single job for every Jumper? If different people do different things, split it into separate tasks." |

Two structural notes ride on these:

- **The binding pair.** Actions-specified + completion-criterion-observable are simultaneously what *binds* (a Jumper's obligation and a dispute's adjudication basis are these two, not the goal text) and what *freezes* (once the first Jumper is active, the completion criterion is immutable; changing it is a new task version). Ask-order is goal-first for good conversation; bindingness belongs to the pair.
- **Definedness ≠ truth.** Every satisfaction test reads the submission text and fields only — "does the text name a target URL?" — never the world. Whether the URL exists, whether the profile is real: that is the verification component's job at submission time. The definition must state this handoff explicitly so Launchers aren't surprised later.

### 4. The task normal form

> **"[Do action(s)] on [target] until [observable end-state], by any matching Jumper, within [bound]."**

The slots map to instance attributes 3, 2, 4, the audience filters (already structured), and attribute 6. A task is defined exactly when its submission can be rendered into this sentence with no empty slots. The form is the canonical **rendering** — Launchers keep writing free text; the clarifier's future job is mapping that text into the form and asking for whatever stays empty. It expresses every task type in the verification design's taxonomy: engagement ("like the 3 most recent photos on instagram.com/X until all 3 hearts show filled"), duration ("watch video V until the player shows ≥30s elapsed"), form-fill ("complete fields A–C on form F and submit, until the confirmation page is visible").

### 5. Aggregation, sufficiency, and field-backed attributes

- **The normative statement is the checklist**: defined = all seven instance attributes satisfied. A graded definedness score may exist *internally* (clarifier UX, analytics) but thresholds are deliberately unset until real task data exists.
- **Sufficiency, not maximization**: beyond all-satisfied, MORE constraint is worse — over-specified paths violate the platform's path-tolerance principle (Jumpers may take alternative valid routes; the verification design explicitly tolerates this). The clarifier should warn against over-constraining.
- **Field-backed attributes**: economics (budget, per-Jumper pay, slot count — including the budget-covers-payouts rule), audience (filters), and timing (deadlines) are definitionally part of every task but already structurally collected and enforced by the wizard and schema. They are listed in the definition for completeness and excluded from the clarifier's question set.

### 6. Per-attribute extras and evolution

- Each attribute may carry an optional **example-violation** (used above) — few-shot anchors for the future LLM checker.
- **Extension convention**: adding an attribute = adding a full triple plus a version note; changing an enforcement flag = a version note. The attribute set is expected to grow from evidence.
- **Feedback register (stub)**: the canonical definition document reserves a per-attribute "known misses" section — populated later from clarifier failures and dispute outcomes, so the definition is a calibration artifact, not a constitution.

### 7. Consumers

Five consumers read the one artifact: the **AI clarifier** (instance triples → its question inventory — the deferred pipeline's seed), the **launch gate** (kind triples), **product vocabulary** (definitions), the **verification component** (the completion criterion is its contract input), and **dispute resolution** (the binding pair is the adjudication basis). A sixth structural note for implementers: the definedness check's natural shape is `undefined_requirements(task) -> list[str]` — the same unmet-list shape the matching component already uses for eligibility (`services/matching.py`), keeping one mental model across gates.

### 8. Seed mapping (the user's words → where they landed)

| User's seed | Landed as | Why |
|---|---|---|
| "digital" | kind attribute **digital**, unchanged | already structural |
| "recordable via screen recording" | kind **verifiable-in-principle** + instance **completion-criterion-observable** | literal recordability discriminates nothing (any screen activity is recordable — including the unverifiable "boost" task); the structural requirement is that *completion* be observable in the evidence channel |
| "achievable" | instance **performable** + **bounded** | one word hid two independent failure modes — needs-special-position and unbounded-effort — which need different clarifying questions |
| "goal is clear?" (example check) | instance **goal-clear**'s question template | exactly as envisioned; plus six siblings derived the same way |

### 9. The acid test

Task #2 — "check my instagram page and like photos to give me a boost" — under the definition: **passes all four kind attributes** (digital, self-contained, permissible-floor, verifiable-in-principle) and **fails instance attributes 1–4** (goal: "a boost" is not an outcome; target: no handle/URL; actions: "like photos" — which, how many; completion: nothing observable named). The clarifier this definition generates would ask exactly four questions, and a repaired version passes: *"Open instagram.com/⟨handle⟩, like the 3 most recent photos, until all 3 show a filled heart, in one session."*

## Next Actions

### MUST
- **What:** Promote this definition into a canonical standalone document at `devdocs/task_meta_definition.md` (registry + normal form + rules + stubs, without the inquiry apparatus)
  **Who:** AI session (this one)
  **Gate:** immediately after this finding is filed
  **Why:** five consumers need a stable, citable path; an inquiry finding is the wrong long-term home for canon
- **What:** Decide the target-platform ToS posture (the open parameter in policy-permissible)
  **Who:** user (product decision, already listed in PROJECT.md Open Decisions)
  **Gate:** before any launch gate enforces the policy-permissible attribute, and no later than choosing MVP task categories
  **Why:** until decided, the kind gate can only enforce the lawful/non-harmful floor

### COULD
- **What:** Write the clarifier BOM (`devdocs/scoped/be/clarifier/`) — the AI data-consumer that evaluates submissions against the registry and generates the confirm-or-clarify text
  **Who:** AI session with user
  **Gate:** when the user schedules the next backend component
  **Why:** this is the deferred pipeline the definition exists to generate
  **Depends-on:** MUST item "Promote to canonical document". This COULD is GATED — the BOM should cite the canonical path, not an inquiry folder.
- **What:** Adopt the instance-attribute question templates as wizard microcopy now (human-Launcher-facing, no AI needed)
  **Who:** bot/web-client launch flows
  **Gate:** next wizard text revision
  **Why:** ships definitional value before the clarifier exists

### DEFERRED
- **What:** Launcher-spec vs verifier-expectation information separation (anti-gaming: don't publish exact evidence expectations) — **Gate:** verification component BOM start — **Why (if revived):** reduces fabricated-evidence risk
- **What:** Populate the feedback register mechanism — **Gate:** clarifier v1 ships — **Why:** turns clarifier misses and disputes into attribute calibration
- **What:** Continuous admissibility (Jumper flagging of non-doable/non-allowed tasks) — **Gate:** moderation/abuse work begins — **Why:** admissibility shouldn't be a launch-time-only stamp
- **What:** Numeric definedness-score thresholds — **Gate:** ≥100 real launched tasks to calibrate against — **Why:** thresholds without data are false precision

## Reasoning

Why this shape and not the alternatives the pipeline generated and tested:

- **Prose-only ontology (killed at sensemaking).** The user's stated dependency — "to generate these first we need to meta define" — makes the definition the *generator* of definedness checks. Prose without per-attribute tests can't generate anything mechanically; the deferred pipeline would re-derive structure from scratch.
- **Descriptive framing (killed at sensemaking).** There is no task population to describe; the only existing instance is the failure case. Description would canonize the gap. The definition is normative.
- **Kind-only definition (killed at sensemaking, despite textual support).** "But this later" reads as deferring the *pipeline*; the live failure is entirely on the instance axis, so a kind-only definition would have judged the motivating task valid — answering the question while missing its goal.
- **Literal "recordable" and monolithic "achievable" (killed as attributes).** Recordability is trivially true of all on-screen activity and discriminates nothing; achievability conflates two failure modes. Both seeds were decomposed rather than copied — the seed-mapping table preserves traceability, a requirement added when critique's user-perspective prosecution landed the objection "the user's words vanished."
- **Two axes as deep structure (killed by Innovation's Inherited Frame Audit, survives as presentation).** The audit forced a challenge to the unexamined two-axis commitment; the deeper structure is per-attribute enforcement flags, with the axes as default groupings. This was the loop catching its own inherited frame.
- **Attribute-count cap (killed in innovation testing).** Forcing ≤6 per axis merged attributes that need distinct clarifying questions; salvaged as presentation grouping only.
- **Revision/redo policy as an attribute (killed).** Lifecycle policy, not task-ness; noted for the verification BOM.
- **Bundle tasks (killed at sensemaking).** Heterogeneous per-Jumper work contradicts the uniform `you_earn × num_jumpers` data model and the planned differential-pay extension; bundles are expressible as multiple tasks — hence the atomicity attribute.
- **Survivors held because** each passed adversarial collision on the critical dimensions extracted from the stabilized understanding: generativity (the clarifier must be derivable — substance-probed by actually deriving questions on the live task) and verifiability alignment (payment-release must stay judgeable), with external anchors verified against the codebase (the schema's fields, the launch flow's steps, the matching component's unmet-list shape).
- **Three candidates were deferred, not killed** — information separation, the feedback-register mechanism, continuous admissibility — each with a concrete revival trigger, because their value is real but their actionability depends on components that don't exist yet.

## Open Questions

### Monitoring
- Do the seven instance attributes cover real submissions? Watch the first ~50 launched tasks for clarification needs that map to NO attribute — each is evidence for the extension convention.
- Does the atomicity question trigger often (>20% of tasks needing splits)? If so, the launch UX needs a first-class "split task" affordance.

### Blocked
- Final wording of policy-permissible's test: blocked on the ToS posture decision (PROJECT.md Open Decisions).
- Capability-envelope versioning convention: blocked on the verification component BOM (which owns the envelope).

### Research Frontiers
- Anti-gaming of definedness: how much evidence expectation can be public before fabrication gets easy (the deferred information-separation candidate).

### Refinement Triggers
- If the verification evidence channel changes (e.g., API-based evidence joins screen recording), re-test the wording of verifiable-in-principle and completion-criterion-observable against the new envelope.
- If the clarifier's miss-rate on any single attribute exceeds its siblings by a wide margin across 50 tasks, that attribute's triple re-opens.

## Source Input

<details>
<summary>Raw user input for this finding (operative ask; full wizard transcript preserved in articulate_simple.md)</summary>

```text
okay we have this but do you see what this is missing hugely?

  Main issue, task clarification pipeline, and AI based data consumer which shows tasks relevant ambiguities and generate
  confirmation text which will be forwarded to user so he can confirm or clarify..

  and we have to have meta definition of what makes a task defined or not.

  for example goal is clear? etc but this later. but to generate these first we need to meta define what a crowdjump task is.

lets create a meta definition for it using attributes (it should be achievable, recordable via screen recording, it should be digital and other attributes  )
```

</details>
