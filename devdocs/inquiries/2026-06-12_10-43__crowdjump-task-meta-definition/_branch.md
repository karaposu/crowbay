# Branch: crowdjump-task-meta-definition

## Source Input
[The user's raw request, preserved verbatim in `articulate_simple.md`'s `## User Input` section — both copies authoritative for transcription audit. Abbreviated here to the operative ask; the full wizard transcript precedes it in the articulation file.]

```text
okay we have this but do you see what this is missing hugely?

  Main issue, task clarification pipeline, and AI based data consumer which shows tasks relevant ambiguities and generate
  confirmation text which will be forwarded to user so he can confirm or clarify..

  and we have to have meta definition of what makes a task defined or not.

  for example goal is clear? etc but this later. but to generate these first we need to meta define what a crowdjump task is.

lets create a meta definition for it using attributes (it should be achievable, recordable via screen recording, it should be digital and other attributes  )
```

(Preceded by the full launch-wizard transcript of task #2 — "check my instagram page and like photos to give me a boost" — which serves as the live example of an under-defined task passing launch unchallenged.)

## Articulation Reference

- **File:** `devdocs/inquiries/2026-06-12_10-43__crowdjump-task-meta-definition/articulate_simple.md`
- **Itemize count:** 1
- **Per-item identifiers:** item-1
- **Verdict:** HIGH-PROCEED
- **Flagged conditions:** none

## Question

**Literal statement (MultiDepth):** "lets create a meta definition for it [what a crowdjump task is] using attributes (it should be achievable, recordable via screen recording, it should be digital and other attributes)"

**What is being asked (MQ1 verdict-axis ambiguities, preserved):**
- `artifact-kind` — a human-readable conceptual definition document vs a machine-consumable attribute schema (per-attribute checks for the future AI clarifier) vs both in one artifact.
- `attribute-set-completeness` — three seeds given (achievable; recordable via screen recording; digital) plus "other attributes": exhaustive enumeration vs a workable core set with extension room.
- `normative-vs-descriptive` — define what a task SHOULD be allowed to be (acceptance/policy gate) vs what a task IS (ontology of the concept).
- `definedness-inclusion` — whether the deliverable includes the derived "is this task defined?" criteria ("goal is clear?") or strictly the meta-definition those criteria will later be generated from.

**What the user is trying to accomplish (MQ3 intent-axis ambiguities, preserved):**
- `endpoint-shape` — foundation document (devdocs vocabulary artifact) vs input contract for the AI clarification pipeline vs launch-time acceptance gate.
- `definition-function` — definition-as-validation (reject failing tasks) vs definition-as-elicitation (drive clarifying questions until attributes are satisfied).

**MQA joint axis (reconciled):** the artifact-kind and endpoint ambiguities fold into one axis — *which consumer the meta-definition serves first* (human readers / the AI clarifier / the launch gate).

## Goal

**Deliverable shape (Deconstruct tuple):** (deliverable: an attribute-based meta-definition of "Crowdjump task"; kinds: definitional documentation with attribute entries structured enough to be individually testable; bounds: Crowdjump tasks specifically — not generic crowdsourcing; meta-level — about the task concept, not any specific task; attribute-based form as prescribed).

**Why a good answer might be wanted (MultiDepth WHY-axis ambiguities, preserved):**
- `enable-the-clarifier` — make the deferred AI clarification pipeline generatable ("to generate these first we need to meta define").
- `marketplace-quality` — keep under-defined tasks (like "give me a boost") from reaching Jumpers.
- `verifiability-economics` — only admit tasks the screen-recording verification can judge, since payment release depends on it.
- `policy-risk-control` — definitionally exclude illegal/abusive/ToS-explosive tasks.
- `product-identity` — pin the platform's central noun so all components share one contract.

**Context the answer needs (MQ2 context-need ambiguities, preserved):**
- verdict: PROJECT.md's task concept and loop; the wizard's current field set; the verification component's capability envelope (SemanticVideoInspector docs); the open ToS/task-category decision.
- kinds: product scope (MVP categories undecided), technical feasibility (what is checkable), legal/policy posture, economic verifiability.
- stance: prototype-stance (lean MVP gate enforceable soon) vs production-stance (complete policy framework).

**What would explicitly fail (MQ4 exclusions):**
- Building the clarification pipeline / AI data-consumer / confirmation-text generation now — explicitly deferred ("but this later").
- Treating this as an implementation task — the ask is a definitional artifact, not wizard/backend code changes.
- Defining the specific Instagram task instance — it is the motivating example only.

## Considered Articulations

**Item item-1 — "Create a meta-definition of what a Crowdjump task is, using attributes":**

1. **Conceptual-ontology reading:** Write a devdocs meta-definition document enumerating the defining attributes of a Crowdjump task (digital, achievable, recordable, and peers), each with definition and rationale — a human-readable foundation for what the platform means by "task."
2. **Machine-consumable schema reading:** Define the attribute set as a structured, individually-testable schema — per attribute: name, definition, satisfaction condition, example pass/fail — explicitly designed as the input contract the future AI clarification pipeline evaluates task descriptions against.
3. **Launch-gate policy reading:** Define the attributes as normative acceptance criteria — the gate distinguishing tasks Crowdjump admits from tasks it rejects (including the legality/ToS dimension), intended for enforcement at task-creation time.
4. **Definedness-foundation reading:** Produce the meta-definition AND derive from each attribute its definedness question (goal-attribute → "is the goal clear?"), yielding both the ontology and the seed question-inventory the deferred clarifier will use.

## Scope Check

**IN scope (Deconstruct bounds):** the attribute-based meta-definition of the Crowdjump task concept — meta-level, Crowdjump-specific, attribute-formed; structured enough that each attribute is individually testable (which keeps variants 2–4 reachable).

**OUT of scope (MQ4 exclusions):** implementing the clarification pipeline, the AI data-consumer, or confirmation-text generation; code changes to the wizard/backend; adjudicating the single Instagram example.

Question covers goal — with one watch-point: the Goal's `enable-the-clarifier` motivation requires the definition to be *generative* (definedness questions must be derivable from it), so a purely prose ontology (variant 1 alone) would cover the question but under-serve the goal. The pipeline should keep variants 2 and 4 alive through critique.

**Specific-vs-pattern check:** the wizard transcript is a specific example ("check my instagram page..."). This inquiry addresses the BROADER PATTERN — what makes ANY submission a well-formed Crowdjump task — not the repair of task #2. The example serves as a test instance for whatever definition emerges.

## Layer Commitment

This inquiry defines a concept (what a Crowdjump task IS) from scratch — a definitional target, so the layer is declared:

- **Primary layer: Meaning** — what a Crowdjump task IS; adjudicates the concept's essence and its defining attributes.
- Out of scope this run:
  - **Structural** (what the task schema/spec looks like in code or DB) — one line: schema follows meaning; deferred until the meaning layer stabilizes.
  - **Process** (what steps the clarification pipeline runs) — one line: explicitly deferred by the user ("but this later").
- Sequential plan: Meaning now → a later inquiry/BOM takes the Structural layer (task schema + definedness checks) → the Process layer (clarification pipeline) builds on both.
