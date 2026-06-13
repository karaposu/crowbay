# Articulate-Simple — clarifier component BOM

## User Input

```text
the clarifier component BOM (structural layer)    project-space    teleological    INVESTIGATE-FRONTIER    HIGH

lets do this

---
SAVE OUTPUT TO: /Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/articulate_simple.md
```

## Substrate

Warm (Edge 1: relevance signals strong). The statement quotes **route 4** of `devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/routelister.md` verbatim — its route record supplies Movement ("open the structural layer — `devdocs/scoped/be/clarifier/` BOM consuming the catalog (placement, endpoints, invocation, revision loop)") and Guidance ("mirror the matching component's BOM pattern"). Session canon: `devdocs/task_consumer_catalog.md` v1.2, `devdocs/task_meta_definition.md`, BOM precedents (`devdocs/scoped/be/backbone/concept_bom.md`, `devdocs/scoped/be/matching/list.md`), existing `src/` layout, bot + fe clients.

## Itemize

- **count:** 1
- **items:** `[item-1: "produce the clarifier component BOM (structural layer)"]`
- Keep-together: the route-type metadata (project-space · teleological · INVESTIGATE-FRONTIER · HIGH) qualifies the one item; "lets do this" is execution consent, not a second item.

## Item 1 — "produce the clarifier component BOM (structural layer)"

### MQ1 (verdict-axis) — What is the user asking for?

identified-ambiguities-list:
- `bom-as-work-order` (an ordered buildable checklist in the matching-list pattern) vs `bom-as-architecture-record` (placement/endpoints/invocation/revision-loop decisions made explicit) vs `both` (the project's BOM precedent combines a decisions table with ordered sections)
- `bom-only` vs `bom-then-implement` (prior BOMs were produced first, then implemented section-by-section on a separate user request; "lets do this" could extend to starting implementation)
- `inquire-then-bom` (the /aMVLwr invocation makes the loop itself the asked-for mechanism: derive what the BOM should contain, then produce it as the finding's artifact)

### MQ2 (context-need axis) — What context does the response need that isn't in the statement?

identified-ambiguities-list:
- **verdict:** the canon pair being consumed (`task_consumer_catalog.md` v1.2 — esp. §2.4's explicit deferral: "the concrete JSON schema, prompt assembly, and invocation plumbing are the clarifier component BOM's deliverable" — and `task_meta_definition.md`); the BOM precedents' structure; the current `src/` module layout (routers / services / models / pluggable backends); the launch flow's confirm step (bot step-6, fe wizard) where the card must land
- **kinds:** which artifact kind — `list.md`-style vs `concept_bom.md`-style vs hybrid; file location (route Movement says `devdocs/scoped/be/clarifier/`); one file or several
- **stance:** MVP vs production posture — real LLM API vs mocked backend at dev-build (project precedent: pluggable backends with console/mock implementations — email, SMS, notifications; escrow launched unfunded); sync-blocking call vs async job in the launch flow; how hard to commit to a vendor

### MQ3 (intent-axis, WHAT) — What is the user trying to accomplish?

identified-ambiguities-list:
- `produce-buildable-task-list` (so a later session can "implement one by one" — the established working rhythm)
- `fix-component-architecture` (decide placement, endpoints, invocation point, revision loop, data model before any code)
- `bridge-canon-to-code` (translate catalog semantics — entries, results, log rows, slots — into schema/service/router work items)
- `integrate-launch-flow` (wire the card into the existing bot/fe confirm step without breaking the wizard)

### MQ4 (boundary-axis) — What is the user explicitly excluding?

identified-ambiguities-list (intrinsic "(structural layer)" + extrinsic route/canon context; Edge 2 routed to both where unclear):
- `not-process-redesign` — the catalog's detections/severities/card semantics are canon (v1.2); the BOM consumes, never re-opens them
- `not-implementation` — structural layer: what the spec looks like and what gets built, not the code itself (implementation follows on separate request, per precedent)
- `not-tos-posture` — route 5, the user's product call
- `not-case-files-or-eval-corpus` — routes 9/16, separate (the BOM may name hooks)
- `not-prompt-authoring` — route 10 (prompt-seed rendering) is its own route; the BOM places the prompt-builder module but does not write the prompt

### MQA

**reconcile:** MQ1's `bom-only vs bom-then-implement` and MQ3's `produce-buildable-task-list` span one joint axis — **deliverable-extent** (framing document ↔ document + begun implementation). Folded into Considered Articulations as the extent dimension. Remaining identifications carry through unchanged; no other overlap (MQ3's architecture/bridge/integrate endpoints are facets of one BOM, not competing extents).

### Deconstruct

- **deliverable:** a BOM document (component bill-of-materials) for the clarifier, under `devdocs/scoped/be/clarifier/`
- **kinds:** markdown spec — decisions table + data model + service/module layout + endpoints + client integration + revision/approval mechanics + test plan, in implementable order
- **bounds:** the clarifier component only; consumes catalog v1.2 + meta-definition as canon; structural layer; excludes the MQ4 list
- Late-split check: one coherent artifact — no split signal.

### MultiDepth

- **literal-statement:** "the clarifier component BOM (structural layer) — project-space · teleological · INVESTIGATE-FRONTIER · HIGH — lets do this."
- **purpose-motivation-ambiguities (WHY-axis):** identified-ambiguities-list:
  - `enable-next-build-session` (the BOM as the work-order that makes implementation a mechanical follow-on)
  - `close-the-mvp-pipeline-gap` (the launch flow's missing clarification step — the original "do you see what this is missing hugely?" motivation)
  - `de-risk-integration` (settle placement/invocation/wire-schema before code so the consumer lands cleanly in existing `src/`)
  - `sustain-route-map-momentum` (executing the HIGH routes in declared order)

### Considered Articulations

1. **Work-order reading:** Produce `devdocs/scoped/be/clarifier/` BOM in the proven pattern — decisions table up front, then ordered buildable sections (data model → LLM backend abstraction → service → endpoints → bot/fe card integration → logging → tests) consuming `task_consumer_catalog.md` as canon, so a later session can implement section by section.
2. **Architecture reading:** Fix the clarifier's structural decisions — where it sits in `src/`, its invocation point in the launch flow, sync vs async posture, the revision loop, the LLM-backend abstraction, the JSON wire schema (§2.4's named deliverable) — recorded as a BOM with each decision explicit and alternatives noted.
3. **Inquiry reading:** Run the full /aMVLwr loop on "what should the clarifier component BOM contain," letting the BOM emerge as the finding's canonical artifact — the loop adjudicates the open structural choices (placement, posture, schema) rather than inheriting defaults.
4. **Extent-maximal reading:** Produce the BOM and begin implementing its first section(s) in `src/` in the same stretch ("lets do this" as build consent, not just spec consent).

## Self-Assessment

LAYER 1 self-check (single LIGHT pass): Modes 1–9 — no fires. Itemize count stable across Deconstruct (no late-split); MQ2 carries verdict/kinds/stance; 2-shape held at every position; WHAT/WHY separated; all four variants pass the composition bounds (BOM deliverable-shape preserved; extent/architecture/mechanism dimensions spanned; MQ4 vocab excluded; warm substrate only). Friction: low — the route record + BOM precedents make the framing well-anchored.

**Verdict: HIGH-PROCEED**
