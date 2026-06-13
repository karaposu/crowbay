# Branch: task-consumer-llm-detections

## Source Input

```text
based on devdocs/inquiries/2026-06-12_10-43__crowdjump-task-meta-definition/finding.md 

how should task consumer LLM should work? 
it should clarify the request with it's own non ambigious understanding and ask for approval
it should enforce the rules, again with suggestions , for example user asked for  non-unit task (this is a term then our LLM detect this, and suggest singular part back to the launcher)

so the thing we should start is , what are main detections and scenarios our LLM should do when consuming  a task.
```

## Articulation Reference

- **File:** `devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/articulate_simple.md`
- **Itemize count:** 1
- **Per-item identifiers:** item-1
- **Verdict:** HIGH-PROCEED
- **Flagged conditions:** none

## Question

**Literal statement (MultiDepth):** "what are main detections and scenarios our LLM should do when consuming a task — it should clarify the request with its own non-ambiguous understanding and ask for approval; it should enforce the rules with suggestions (e.g., user asked for a non-unit task → detect this and suggest the singular part back to the launcher)."

**What is being asked (MQ1 ambiguities, preserved):**
- `enumeration-vs-design` — a list of detections/scenarios vs the consumer's working design (detect → suggest → confirm flow).
- `granularity` — attribute-level detections vs scenario-level interaction patterns vs both layers.
- `scenario-meaning` — input categories vs conversation outcomes (confirm / clarify / suggest-fix / reject) vs future test cases.
- `completeness` — "main" = core working set vs exhaustive taxonomy.

**What the user is trying to accomplish (MQ3 ambiguities, preserved):**
- `endpoint-shape` — design document vs clarifier-BOM seed inventory vs prompt-ready instruction-set spec.
- `behavior-extent` — detect-and-ask vs detect-and-REWRITE-for-approval (the stated "its own non-ambiguous understanding" + "ask for approval") vs auto-apply (argued against by "ask for approval", still open in extent).

**MQA joint axis (reconciled):** `enumeration-vs-design` + `endpoint-shape` fold into **deliverable-altitude** — where between plain enumeration and executable prompt-spec the answer should land.

## Goal

**Deliverable shape (Deconstruct tuple):** (deliverable: a catalog of detections + interaction scenarios for the task-consumer LLM, grounded in the meta-definition's attributes, each detection carrying trigger and suggestion/response shape; kinds: design documentation — detection entries + scenario flows; bounds: task-consumption time only; Crowdjump submissions; LLM-as-consumer perspective; meta-definition as given base).

**Why a good answer might be wanted (WHY-axis, preserved):**
- `start-the-deferred-clarifier` — begin the design layer of the pipeline the prior inquiry deferred.
- `launch-quality` — keep under-defined / rule-violating tasks from reaching Jumpers.
- `launcher-UX` — confirm-and-suggest experience that teaches rather than rejects.
- `prompt-seed` — the catalog may become the LLM's instruction set directly.
- `test-coverage` — scenarios double as the consumer's future eval cases.

**Context the answer needs (MQ2, preserved):**
- verdict: the meta-definition finding + canonical `devdocs/task_meta_definition.md`; the consumer's seat in the existing launch flow (bot wizard collects desc verbatim today); the existing proto-detection (audience-preview raw-location warning); the matching evaluator as downstream consumer.
- kinds: behavioral contract (confirm vs auto-apply), pipeline placement (desc-step vs post-wizard vs pre-launch), interaction budget (questions per task before abandonment).
- stance: MVP-stance (single-pass LLM + short confirm loop) vs production-stance (multi-turn agent, learned thresholds).

**What would explicitly fail (MQ4 exclusions):**
- Implementing the consumer (code, API integration, prompt-engineering mechanics) — this ask is the detections/scenarios layer ("the thing we should start is").
- Re-deriving the task meta-definition — it is the given base.
- Downstream stages (verification, payouts) — consumption-time only.

## Considered Articulations

**Item item-1 — "Main detections and scenarios for the task-consumer LLM":**

1. **Detection-catalog reading:** enumerate the main detections — one per meta-definition attribute plus cross-cutting ones (e.g., non-atomic/non-unit) — each with trigger condition and suggested-response shape, as a design document.
2. **Interaction-scenario reading:** define the consumer's scenario space — the main conversation flows (clean → restate-and-confirm; under-specified → clarify; rule-violating → suggest repair; inadmissible kind → reject with reason) with detections as entry conditions.
3. **Behavioral-contract reading:** specify the end-to-end working contract — input, detection pass, rewrite proposal, approval gate, structured output — the clarifier's functional specification.
4. **Prompt-seed reading:** produce the catalog structured for direct consumption as the LLM's instruction set, scenarios as few-shot cases.

## Scope Check

**IN scope (Deconstruct bounds):** the detections + scenarios catalog for consumption-time behavior, grounded in the existing meta-definition, from the LLM-consumer's perspective — at whatever deliverable-altitude survives the pipeline.

**OUT of scope (MQ4):** consumer implementation; meta-definition re-derivation; verification/payout stages.

Question covers goal — with one watch-point: the `prompt-seed` and `test-coverage` motivations require detections phrased OPERATIONALLY (trigger + response, not just names), so a bare-list answer (thin end of the altitude axis) would cover the question but under-serve the goal. The pipeline should keep the operational phrasings alive.

**Specific-vs-pattern check:** the user's example (non-unit task → suggest singular part) is one detection instance. The inquiry addresses the BROADER PATTERN — the full detection/scenario space for task consumption — with the example as one anchor case.

## Layer Commitment

This inquiry designs how a component WORKS (steps, triggers, responses):

- **Primary layer: Process** — what detections fire, in what order, with what responses; adjudicates the consumer's behavioral mechanism.
- Out of scope this run:
  - **Meaning** (what a task IS) — one line: settled by the prior inquiry's meta-definition; inherited, not re-adjudicated.
  - **Structural** (code schema, API shape, prompt file layout) — one line: follows once the process layer stabilizes; belongs to the clarifier BOM.
- Sequential plan: Process now (this inquiry) → Structural next (clarifier BOM consuming this catalog) → implementation.
