# Branch: clarifier-component-bom

## Source Input

```text
the clarifier component BOM (structural layer)    project-space    teleological    INVESTIGATE-FRONTIER    HIGH

lets do this
```

(Quotes route 4 of `devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/routelister.md`; that route record's Movement and Guidance are part of the statement's meaning: "open the structural layer — `devdocs/scoped/be/clarifier/` BOM consuming the catalog (placement, endpoints, invocation, revision loop)"; "mirror the matching component's BOM pattern".)

## Articulation Reference

- **File:** `devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/articulate_simple.md`
- **Itemize count:** 1
- **Per-item identifiers:** item-1
- **Verdict:** HIGH-PROCEED
- **Flagged conditions:** none

## Question

Literal statement: "the clarifier component BOM (structural layer) — project-space · teleological · INVESTIGATE-FRONTIER · HIGH — lets do this."

What kinds of ask this carries (MQ1, preserved as ambiguities):
- `bom-as-work-order` (ordered buildable checklist, matching-list pattern) vs `bom-as-architecture-record` (placement/endpoints/invocation/revision-loop decisions explicit) vs `both` (the project's BOM precedent combines decisions table + ordered sections)
- `bom-only` vs `bom-then-implement` ("lets do this" as spec consent vs build consent)
- `inquire-then-bom` (the /aMVLwr invocation makes the loop the mechanism: derive what the BOM should contain, then produce it)

What action-endpoints are plausible (MQ3):
- `produce-buildable-task-list` (so a later session implements one by one — the established rhythm)
- `fix-component-architecture` (placement, endpoints, invocation point, revision loop, data model — before code)
- `bridge-canon-to-code` (translate catalog semantics — entries, results, log rows, slots — into schema/service/router work items)
- `integrate-launch-flow` (land the card in the existing bot/fe confirm step without breaking the wizard)

## Goal

Deconstruct tuple: **deliverable** = a BOM document for the clarifier component under `devdocs/scoped/be/clarifier/`; **kinds** = markdown spec — decisions table + data model + service/module layout + endpoints + client integration + revision/approval mechanics + test plan, in implementable order; **bounds** = the clarifier component only, consuming `task_consumer_catalog.md` v1.2 + `task_meta_definition.md` as canon, structural layer.

WHY-axis motivations a good answer might serve (preserved as ambiguities):
- `enable-next-build-session` — the BOM as work-order making implementation mechanical
- `close-the-mvp-pipeline-gap` — the launch flow's missing clarification step (the original "missing hugely" motivation)
- `de-risk-integration` — settle placement/invocation/wire-schema before code lands in existing `src/`
- `sustain-route-map-momentum` — HIGH routes executed in declared order

Context downstream consumers need (MQ2):
- **verdict:** catalog v1.2 (esp. §2.4's explicit deferral of JSON schema / prompt assembly / invocation plumbing TO this BOM), the meta-definition, the BOM precedents (`devdocs/scoped/be/backbone/concept_bom.md`, `devdocs/scoped/be/matching/list.md`), current `src/` layout (routers/services/models/pluggable backends), the launch flow's confirm step (bot step-6, fe wizard)
- **kinds:** artifact kind (list-style vs concept-bom-style vs hybrid); location `devdocs/scoped/be/clarifier/`; one file or several
- **stance:** MVP vs production posture — real LLM API vs mocked backend (project precedent: pluggable console/mock backends; unfunded-escrow dev posture); sync-blocking vs async invocation; vendor-commitment depth

What would explicitly fail (MQ4 — negative spec):
- re-opening catalog process semantics (detections/severities/card rules are canon)
- writing the implementation itself (structural layer: spec, not code)
- deciding the ToS posture (route 5, user's call)
- authoring case files / eval corpus (routes 9/16; hooks may be named)
- authoring the prompt (route 10; the BOM places the prompt-builder, doesn't write prompt text)

## Considered Articulations

**Item item-1 — "produce the clarifier component BOM (structural layer)":**
1. **Work-order reading:** Produce `devdocs/scoped/be/clarifier/` BOM in the proven pattern — decisions table up front, then ordered buildable sections (data model → LLM backend abstraction → service → endpoints → bot/fe card integration → logging → tests) consuming the catalog as canon, so a later session can implement section by section.
2. **Architecture reading:** Fix the clarifier's structural decisions — placement in `src/`, invocation point in the launch flow, sync vs async posture, revision loop, LLM-backend abstraction, the JSON wire schema (§2.4's named deliverable) — recorded as a BOM with each decision explicit and alternatives noted.
3. **Inquiry reading:** Run the full /aMVLwr loop on "what should the clarifier component BOM contain," letting the BOM emerge as the finding's canonical artifact — the loop adjudicates the open structural choices (placement, posture, schema) rather than inheriting defaults.
4. **Extent-maximal reading:** Produce the BOM and begin implementing its first section(s) in `src/` in the same stretch ("lets do this" as build consent).

## Scope Check

Question covers goal. The Deconstruct bounds (clarifier component, canon-consuming, structural layer) cover everything the Goal asks; the MQ4 exclusions (no process re-opening, no implementation-as-deliverable, no ToS call, no case files, no prompt text) bound it from the other side. Extent note: articulation 4 (begin implementing) exceeds Deconstruct's bounds — the pipeline carries it as a variant; if it survives critique, beginning implementation is a follow-on consent the user has arguably already given ("lets do this"), to be confirmed at finding time rather than assumed.

Specific-vs-pattern check: the question targets ONE specific artifact (this component's BOM), not a pattern of BOMs — scoped to the specific deliverable by the route record itself.

## Layer Commitment

Primary layer: **Structural** — what the clarifier's spec LOOKS LIKE: sections, decisions, data model, endpoints, module placement, wire schema, integration points, ordered work items.

Out of scope for THIS run:
- **Meaning** — what the consumer IS (single-pass detect→propose→confirm normalizer) was settled by the two prior inquiries; canon in `task_consumer_catalog.md` §1.
- **Process** — what steps it runs (detections, severities, routing, card mechanics) is catalog §2–§5 canon; the BOM consumes, never re-adjudicates.

Sequential plan inherited from the detections inquiry's Layer Commitment: Process (done, catalog v1.2) → **Structural (this inquiry)** → implementation (next, on the BOM's order).
