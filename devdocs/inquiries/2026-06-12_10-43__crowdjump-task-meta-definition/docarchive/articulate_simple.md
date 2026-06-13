# Articulate-Simple — Crowdjump Task Meta-Definition

## User Input

```text
Step 1/6 · Description
What should Jumpers do? Describe the task in your own words.
✖️ Cancel
check my instagram page and like photos to give me a boost
Step 2/6 · Budget
Total budget for this task, in USDT (just a number, e.g. 50):
✖️ Cancel
50
Step 2/6 · Pay
How much does each Jumper earn? (e.g. 5)
✖️ Cancel
1
Step 2/6 · Jumpers
How many Jumpers do you need? (e.g. 10)
✖️ Cancel
20
Step 3/6 · Filters — location
Where should Jumpers be from? Type it freely (e.g. Germany, Istanbul, EMEA but not Russia) — or skip:
🌍 Anywhere (skip)
✖️ Cancel
not from india and china
Step 3/6 · Filters — age
Pick a range or type one like 21-30:
18–25
25–35
18+
Any age (skip)
✖️ Cancel
Step 3/6 · Filters — gender
Female
Male
Any (skip)
✖️ Cancel
Step 4/6 · Deadline
In how many days must submissions be done? Type a number of days, or skip:
No deadline (skip)
✖️ Cancel
Step 5/6 · Jumper approval
Auto-accept anyone who matches, or approve each Jumper yourself?
⚡ Auto-accept Jumpers
✅ I'll approve each Jumper
✖️ Cancel
Step 6/6 · Confirm your task

📝 check my instagram page and like photos to give me a boost

💰 Budget: 50 USDT
🐦 20 Jumper(s) × 1 USDT
🎯 Who: location: not from india and china, age 18–25, female
⏰ Deadline: none
✅ Mode: auto-accept

👥 Verified Jumpers matching right now: fewer than 10
⚠️ Location is free text only — it won't constrain matching until parsed

Launch it?
🚀 Launch it
↩️ Start over
✖️ Cancel
🚀 Task #2 launched!
It's now visible to Jumpers (20 slot(s)).

Escrow funding arrives with the payments component — for now tasks launch unfunded in this dev build.
Welcome to Crowdjump!

Launch a task — the crowd jumps on it.
Earn money by jumping on tasks that match you.

What would you like to do?
🚀 Launch a task
👀 Browse tasks
📋 My tasks
🐦 My jumps
👤 Profile
❓ Help
Your launched tasks
🟢 #2 check my instagram page and like photos to give me a boost — 20 slot(s) · open
👥 Jumpers of #2
Task #2 has no Jumpers yet.


okay we have this but do you see what this is missing hugely?

  Main issue, task clarification pipeline, and AI based data consumer which shows tasks relevant ambiguities and generate
  confirmation text which will be forwarded to user so he can confirm or clarify..


  and we have to have meta definition of what makes a task defined or not.

  for example goal is clear? etc but this later. but to generate these first we need to meta define what a crowdjump task is.

lets create a meta definition for it using attributes (it should be achievable, recordable via screen recording, it should be digital and other attributes  )
```

## Substrate Note

Warm context: this session built the Crowdjump backend, bot, matching component, and dev web client. The wizard transcript above is a live run of that system (task #2: "check my instagram page and like photos to give me a boost"). It functions as illustrative substrate — a concrete instance of an under-defined task slipping through launch with zero clarification — not as the deliverable target.

## Itemize

- **count:** 1
- **items:**
  - **item-1:** "Create a meta-definition of what a Crowdjump task is, using attributes (e.g. achievable, recordable via screen recording, digital, and other attributes)."

Keep-together reasoning: the statement names a larger missing system (clarification pipeline, AI ambiguity-consumer, confirmation-text generation, definedness criteria) but explicitly defers it ("but this later") and orders the dependency ("to generate these first we need to meta define what a crowdjump task is"). The final imperative is a single work item: the attribute-based meta-definition. The definedness-criteria question ("goal is clear?") is held as an identified ambiguity about deliverable scope rather than split into a second item — the user frames it as a derivative of this item, not a parallel one.

## Item 1 — "Create a meta-definition of what a Crowdjump task is, using attributes"

### MQ1 (verdict-axis)

**Q:** What is the user asking for?

**A — identified-ambiguities-list:**
- `artifact-kind`: a human-readable conceptual definition document vs a machine-consumable attribute schema (named attributes with per-attribute checks, designed for the future AI clarifier to evaluate) vs both in one artifact.
- `attribute-set-completeness`: three seed attributes are given (achievable; recordable via screen recording; digital) plus "and other attributes" — exhaustive enumeration vs a workable core set with extension room.
- `normative-vs-descriptive`: define what a Crowdjump task SHOULD be allowed to be (an acceptance/policy gate) vs describe what a Crowdjump task IS (an ontology of the concept).
- `definedness-inclusion`: whether the deliverable includes the derived "is this task defined?" criteria (e.g. "goal is clear?") or strictly the meta-definition from which those criteria will later be generated.

### MQ2 (context-need axis)

**Q:** What context does the response need that isn't in the statement?

**A — identified-ambiguities-list:**
- `verdict`: which existing artifacts constrain the definition — PROJECT.md's task concept and loop; the launch wizard's current field set (desc/budget/pay/slots/filters/deadline/approval); the verification component's actual capability envelope (what screen-recording analysis can and cannot judge, per SemanticVideoInspector docs); the open ToS/task-category decision in PROJECT.md's Open Decisions.
- `kinds`: which kinds of context matter — product scope (MVP task categories undecided), technical feasibility (what is checkable), legal/policy posture (prohibited tasks), economic (is the task verifiable cheaply enough to release money on).
- `stance`: prototype-stance (a lean MVP gate the current codebase can enforce soon) vs production-stance (a complete policy framework with edge-case taxonomy).

### MQ3 (intent-axis, WHAT)

**Q:** What is the user trying to accomplish?

**A — identified-ambiguities-list:**
- `endpoint-shape`: produce a foundation document (vocabulary artifact in devdocs) vs produce the input contract for the AI clarification pipeline (the thing the "AI based data consumer" reads to find a task's relevant ambiguities) vs produce a launch-time acceptance gate (criteria that admit/reject tasks at creation).
- `definition-function`: definition-as-validation (reject tasks that fail attributes) vs definition-as-elicitation (drive clarifying questions back to the Launcher until attributes are satisfied) — the transcript's confirmation-text mention suggests elicitation, but the ask itself doesn't commit.

### MQ4 (boundary-axis)

**Q:** What is the user explicitly excluding?

**A — identified-ambiguities-list (explicit exclusions):**
- The clarification pipeline implementation itself — "Main issue, task clarification pipeline, and AI based data consumer ... generate confirmation text" is named as the missing system but deferred: "for example goal is clear? etc **but this later**."
- Building/changing the wizard or backend code as part of this ask — the imperative is "create a meta definition," a definitional artifact, not an implementation.
- The specific Instagram task instance — it is the motivating example, not the object to be defined.

### MQA

**reconcile** — MQ1's `artifact-kind` and MQ3's `endpoint-shape` span one joint axis: **consumer-of-the-definition** (human readers building shared vocabulary / the future AI clarifier / the launch-time gate). The choice of primary consumer determines artifact kind. Folded as: "which consumer the meta-definition serves first."

Remaining identifications flow through unreconciled: MQ1's `normative-vs-descriptive` and `definedness-inclusion`, MQ3's `definition-function`, and all MQ2 axes are distinct dimensions — no further joint axis perceivable with confidence.

### Deconstruct

**tuple:** (deliverable: an attribute-based meta-definition of "Crowdjump task"; kinds: definitional documentation, with attribute entries structured enough to be individually testable; bounds: Crowdjump tasks specifically — not generic crowdsourcing; meta-level — about the task concept, not any specific task; attribute-based form as prescribed by the user)

Late-split check: single-deliverable tuple; no late-split signal. (The definedness-criteria derivative was held as ambiguity, consistent with keep-together.)

### MultiDepth

**literal-statement:** "lets create a meta definition for it [what a crowdjump task is] using attributes (it should be achievable, recordable via screen recording, it should be digital and other attributes)"

**identified-purpose-motivation-ambiguities (WHY-axis):**
- `enable-the-clarifier`: the definition exists to make the deferred AI clarification pipeline generatable ("to generate these first we need to meta define").
- `marketplace-quality`: keep under-defined junk tasks (like the transcript's "give me a boost") from reaching Jumpers, protecting completion rates and trust.
- `verifiability-economics`: only admit tasks the screen-recording verification can actually judge, since payment release depends on it.
- `policy-risk-control`: a definitional layer that excludes illegal/abusive/ToS-explosive tasks before they exist.
- `product-identity`: pin the platform's central noun — "task" — so all components (wizard, matching, verification, disputes) share one contract.

### Considered Articulations

1. **Conceptual-ontology reading:** Write a devdocs meta-definition document that enumerates the defining attributes of a Crowdjump task (digital, achievable, recordable, and peers), each with a definition and rationale — a human-readable foundation establishing what the platform means by "task."
2. **Machine-consumable schema reading:** Define the attribute set as a structured, individually-testable schema — per attribute: name, definition, satisfaction condition, example pass/fail — explicitly designed as the input contract the future AI clarification pipeline evaluates task descriptions against.
3. **Launch-gate policy reading:** Define the attributes as normative acceptance criteria — the gate that distinguishes tasks Crowdjump admits from tasks it rejects (including the legality/ToS dimension), intended for enforcement at task-creation time.
4. **Definedness-foundation reading:** Produce the meta-definition AND derive from each attribute its definedness question (e.g. goal-attribute → "is the goal clear?"), yielding both the ontology and the seed question-inventory the deferred clarifier will use — definition plus check-generation in one artifact.

Composition check: all four preserve the deliverable shape (attribute-based meta-definition artifact), each spans an identified ambiguity dimension (artifact-kind / consumer / normative-vs-descriptive / definedness-inclusion), none includes the excluded pipeline implementation, all stay within warm-session substrate (Crowdjump vocabulary: Launcher, Jumper, verification, launch gate).

## Self-Assessment

LAYER 1 self-check (single LIGHT pass): Modes 1–9 scanned — zero fires. One boundary noted without firing: Mode 2 (late-detected multi-item) was approached by the definedness-criteria question, resolved by keep-together since the user explicitly ordered the dependency ("first we need to meta define"); the openness is preserved as MQ1's `definedness-inclusion` ambiguity and articulation variant 4. Friction: low.

**Verdict: HIGH-PROCEED**
