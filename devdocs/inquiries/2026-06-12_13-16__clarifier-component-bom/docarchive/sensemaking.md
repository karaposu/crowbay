# Sensemaking — Clarifier Component BOM

## User Input

/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/_branch.md

## SV1 — Baseline Understanding

A BOM document in the house pattern listing what to build for the clarifier: a service that runs the catalog's detections, some endpoints, and card rendering in the two clients. Mirror `matching/list.md`, fill in sections, done.

## Phase 1 — Cognitive Anchor Extraction

**Constraints**
- C1: Catalog v1.2 is canon. The BOM consumes §2 (framework/normative), §5 (card spec), §6 (output contract); it never re-opens detection semantics (MQ4).
- C2: Catalog §2.4 NAMES this BOM's deliverables: the concrete JSON wire schema, prompt assembly, invocation plumbing.
- C3: Single-pass discipline + idempotency (§2.5): one LLM call per submission revision; identical text+context ⇒ identical results; suppression (`not-evaluated`) is runner-set.
- C4: Both clients POST `/tasks` directly from their confirm step (bot `flows/launch.py` CONFIRM callback; fe `confirmLaunch()`); the card must land in both; chip ergonomics carry the catalog's two-client freeze gate.
- C5: Greenfield: zero LLM code in `src/` — this is the backend's first LLM dependency; must follow the pluggable-backend house pattern (`EMAIL_BACKEND`/`SMS_BACKEND`/`NOTIFY_BACKEND`: console/mock vs real, Settings-selected, fail-fast required config).
- C6: House conventions bind: plain-function services, thin routers, hand-written pydantic, Alembic migrations, ledger-style log tables (`notifications` precedent: dedupe_key, status enum, JSON payload), no DI.
- C7: Layer Commitment: structural — the BOM specifies; implementation is a later session working the sections in order.
- C8: `notifications.fan_out_task_matched` fires inside `POST /tasks` — clarifier approval must come BEFORE task creation/fan-out, not after.
- C9: No task-edit endpoint exists; binding-pair freeze is trivially satisfied today; the clarifier's revision loop is the first pre-launch mutation surface.
- C10: MQ4: no ToS resolution, no case-file authoring, no prompt text, no eval corpus (hooks only).

**Key Insights**
- KI1: **The invocation-seam decision is THE architecture decision** — everything else (schema, storage, client work) follows from whether the clarifier is a draft resource, a decorator on `POST /tasks`, or a stateless pre-check.
- KI2: Catalog §5.4 (approval record stores card-as-shown + every resolution) + §2.6 (log row carries `resolution`, which arrives AFTER the run) jointly force **persistence** — a run that must be updated later cannot be stateless.
- KI3: Normalized slots have **no column home**: the Task model mirrors TaskCreate; nothing holds `actions[]`/`end_state`/`bound`.
- KI4: The **mock backend is the product at MVP**, not a test stub: deterministic, catalog-shaped output lets the whole draft→card→approve flow ship and be exercised before any API key exists (MockTwilio precedent).
- KI5: Idempotency + revision loop imply run records keyed by submission content hash — identical re-runs return the cached run.
- KI6: The wire schema mirrors catalog §2.1's entry fields + slot model, and must carry **versions** (catalog version, per-entry versions) or the calibration log is uninterpretable later.
- KI7: Sync-in-request with a declared async seam is the established house posture (fan-out: "synchronous at MVP; the seam should allow moving to a background job without API changes").
- KI8: The K3 hold path needs an **operator surface that doesn't exist** — the backbone has no admin/operator concept at all.
- KI9: Prompt assembly is a module with a contract (catalog+cases in, prompt out), not authored text (route 10 stays open; MQ4).
- KI10: Degradation posture must be explicit: `off` must reproduce today's flow exactly; real-backend failure must not become a platform outage.

**Structural Points**
- SP1: Candidate homes: `services/clarifier.py` (engine+card composer), `services/clarifier_backend.py` (protocol+mock+real), `schemas/clarifier.py` (wire), `db/models/clarifier.py` (draft/run/detection rows), `routers/clarifier.py`.
- SP2: Flow: client submits draft payload (TaskCreate shape) → code executors + single LLM pass → run + card persisted → client renders card → resolutions accumulate → approve → task created from consensus snapshot (existing `task_service.launch_task`) → fan-out.
- SP3: Detection log = the calibration dataset feeding the meta-definition's feedback register (§2.6 row shape is given).
- SP4: Acid cases (catalog §7) are the integration fixtures; routing matrix (§2.3) is the unit-test grid.

**Foundational Principles**
- FP1: The bot owns zero business logic — card CONTENT must be API-side; clients render layout only.
- FP2: Definedness ≠ truth — no lookups (inherited; shapes the backend protocol: text+context in, judgments out, no tools).
- FP3: Code authoritative over LLM; field-backed data never re-asked (executor split is config, not prompt).
- FP4: Config-overridable knobs; fail fast at startup on missing required config for the selected backend.

**Meaning-Nodes:** draft lifecycle · the run · card payload (server-composed JSON) · consensus snapshot · executor split · backend selector.

## SV2 — Anchor-Informed Understanding

Not "a list of things to build" — the BOM is **six open structural decisions plus a mostly-determined build plan**. Canon (catalog) + house precedent determine ~80% of the component; the BOM's real content is adjudicating: (1) invocation seam, (2) card-composition home, (3) slot storage, (4) sync/async, (5) degradation/failure posture, (6) hold operator surface — then ordering the determined work into implementable sections.

*Meta-inspection (H4/H5): "draft" is a loop-introduced term — validated against user language ("task clarification pipeline", "AI based data consumer… forwarded to user so he can confirm or clarify" — a confirm-or-clarify holding state is exactly a draft). "Clarifier" is the user's own established component name (prior finding's "clarifier-startup", route 4 title).*

## Phase 2 — Perspective Checking

- **Technical/Logical:** KI2's persistence forcing + KI5's content-hash caching both land naturally on a draft resource with run rows. Decorating `POST /tasks` (inline block-and-return-card) stuffs a state machine into a creation endpoint and leaves resolutions homeless; stateless pre-check loses the approval record outright. New anchor: **draft status machine** (clarifying → awaiting_approval | held | declined → approved/launched | abandoned).
- **Human/User (Launcher):** LLM latency (2–10s) sits between "Launch it?" and the card — clients need a thinking state; green channel must stay one tap (card arrives pre-confirmed-shape, single CTA). Two clients must show IDENTICAL consent content — diff visibility is a committed consent rule; duplicated composition logic would drift. New anchor: **server-composed card payload** (zones as structured JSON; clients render).
- **Strategic/Long-term:** the draft resource is the future home of task versioning (freeze: edits = new version, catalog §5.4) and the approval record is dispute evidence; the run/log table is the calibration substrate the meta-definition's evolution depends on. Choosing draft-resource now buys those for free.
- **Risk/Failure:** LLM outage with backend=real: fail-closed turns an API outage into a platform outage; fail-open matches today's status quo (the platform currently has NO gate at all) — but must be visible (card notice + audit event + `not-evaluated` logging). Injection: X1's hard rule is enforced structurally — structured output schema, no tool access, desc passed as data field. Token cost bounded by desc ≤ 5000 chars.
- **Resource/Feasibility:** ~4–5 days solo (tables+schemas 0.5 · engine+mock 1 · endpoints 0.5 · bot+fe card 1–1.5 · real backend 0.5 · tests 1). Comparable to the backbone BOM; mock-first means no API-key dependency for the bulk.
- **Definitional/Internal Consistency:** draft-resource vs catalog's "consumer enriches the existing confirm step" — no contradiction: the wizard is unchanged through its steps; only the confirm step becomes draft-backed. Server-composed content vs the two-client freeze gate — no contradiction: the gate governs LAYOUT/ergonomics (client-side), not content.
- **Frame-exit Completeness** (gating fires: "backend" inherited across 4 values; "operator" inherited from catalog hold path): Existence Enumeration on "operator" → the catalog assumes an operator queue ("at MVP the operator IS the queue") but project-wide NO operator/admin role, auth gate, or surface exists anywhere in `src/`. Role assessment: load-bearing for K3 holds. Corrective: not force into frame as a full admin system — re-locate as a minimal config-gated capability (`OPERATOR_USER_IDS`) with the real admin component out of scope. **This is the inquiry's biggest frame-exit catch.**
- **Phase/Calibration-State:** all numeric knobs provisional (catalog §8); the BOM must ship them as config with calibration gates noted, not hardcode. Default backend at MVP: `mock` in dev; flag-off rollout posture until the card prototype passes the freeze gate.

## SV3 — Multi-Perspective Understanding

The component is a **draft-lifecycle service wrapped around the existing launch path**, with the LLM behind a backend selector and the card composed server-side. The six decisions have leanings now (draft-resource; server composition; JSON slots; sync+seam; visible fail-open; minimal config-gated operator). One genuinely new requirement surfaced: the operator gate must be invented minimally because nothing exists. The BOM's sections are already enumerable.

## Phase 3 — Ambiguity Collapse

#### A1: Invocation seam — draft resource vs decorate POST /tasks vs stateless pre-check
**Counter:** stateless `POST /tasks/clarify` is radically simpler — no new tables, no status machine; clients call it, render the card, then POST /tasks as today.
**Why it fails (structural):** catalog §5.4 requires the approval record to store the card-as-shown + every item's resolution; §2.6's log row carries `resolution`, which arrives AFTER the LLM run as the Launcher taps chips. A record that must be written to across multiple client interactions cannot be stateless; and approval-by-token-replay (signing the card into a JWT the client returns) re-implements persistence badly (size, audit, abandonment tracking all lost).
**Confidence:** HIGH. **Resolution:** a **task-draft resource** with status machine; approval creates the task via existing `task_service.launch_task`. **Fixed:** draft/run/detection tables exist; `POST /tasks` remains untouched (direct API launch stays legal — it's also the escape hatch while flag is off). **Excluded:** inline blocking decoration of task creation; approval tokens. **Depends:** endpoints, client flows, log, tests.

#### A2: Card-content composition — server vs clients
**Counter:** ship raw detection results; each client composes its own card (max client flexibility, thinner API).
**Why it fails:** diff visibility and stet scope are committed CONSENT rules (catalog §5.2); duplicating their composition across bot HTML and web DOM guarantees drift on exactly the content that legally matters (consensus snapshot = what was SHOWN); and FP1 (bot owns zero business logic) already prohibits it.
**Confidence:** HIGH. **Resolution:** the API composes a **card payload** — ordered zones with typed items (diff marks, chips with entry codes, rationales, preview line, CTA lock state); clients map zones to layout only. The persisted card-as-shown IS this payload.
**Fixed:** one composition implementation; payload schema in `schemas/clarifier.py`. **Excluded:** client-side card logic beyond rendering.

#### A3: Normalized-slot storage — relational columns vs JSON
**Counter:** proper columns/table for slots (queryable, typed, "right" long-term).
**Why it fails (for now):** the slot consumers at MVP (matching's location handover, verification's criterion, Jumper display) read per-task values — no cross-task slot queries exist; the slot model may still evolve with calibration; a relational schema now is speculative structure. The ledger precedent (JSON payload column) is the house norm for exactly this.
**Confidence:** HIGH (with revisit gate). **Resolution:** slots live on the run as JSON; on approval they copy to `tasks.normalized_slots` (JSON) + `tasks.clarifier_run_id` FK. Revisit at calibration era or when a consumer needs slot-level SQL.
**Fixed:** Task gains two columns by migration. **Excluded:** slot tables now.

#### A4: Sync vs async LLM call
**Counter:** background job + polling from day one (LLM calls are slow; never block a request).
**Why it fails (for now):** MVP scale + house precedent (fan-out synchronous with a declared seam); the draft resource ALREADY gives the async-ready shape — `POST .../runs` could return `running` and clients poll draft status; committing queue infra now buys nothing the seam doesn't.
**Confidence:** HIGH. **Resolution:** synchronous in-request; endpoint + payload shapes designed so async swap changes no API contract (status field exists from day one; clients handle a `running` status defensively).
**Fixed:** no new infra. **Excluded:** celery/queue dependencies at MVP.

#### A5: Degradation & failure posture
**Counter (to fail-open):** fail-closed — a policy gate that silently opens on outage isn't a gate.
**Why the counter fails (at MVP):** today the platform has NO gate; fail-closed converts an LLM outage into a total launch outage to protect a control that didn't exist last week; the operator-review backstop is unchanged. Visibility is the real requirement.
**Confidence:** HIGH for MVP, explicitly revisit-gated on the ToS-posture decision / production hardening.
**Resolution:** `CLARIFIER_BACKEND = off | mock | <real>`. `off` ⇒ clients use today's direct flow (capability-flagged); `real` failure ⇒ one retry, then **visible fail-open**: code-executor-only card with "AI review unavailable" warn line, audit event `clarifier.skipped`, LLM entries logged `not-evaluated`.
**Fixed:** flag semantics; failure UX. **Excluded:** silent fail-open; fail-closed at MVP.

#### A6: K3 hold operator surface (the frame-exit catch)
**Counter:** skip holds at MVP — map K3-uncertain to decline (no operator exists anyway).
**Why it fails:** catalog §2.3 makes the hold the SOLE exception precisely because auto-declining on uncertainty is canon-forbidden (chilling-effect rationale, critique-tested); building the component against canon on day one corrupts the calibration log's semantics too.
**Confidence:** HIGH. **Resolution:** minimal operator capability: `OPERATOR_USER_IDS` config list; held drafts notify operators via the existing notifier; `POST /tasks/drafts/{id}/hold-resolution` gated on that list; full admin tooling explicitly out of scope (future component).
**Fixed:** hold path exists end-to-end. **Excluded:** building an admin system; auto-decline.

*(Load-bearing concept test — "draft": domain-property vs external default — validated against user language ("confirm or clarify" holding state) and against C9 (no other pre-launch mutable state exists; the concept is forced, not imported). "Run": proxy check — a run is a real structural unit (one LLM pass over one submission revision), not an incidental label; its determination mechanism is specified (content hash). Specific-vs-pattern: the acid cases are fixtures of the pattern, not the pattern — the BOM tests the MATRIX (§2.3) as the general object, acid cases as instances.)*

## SV4 — Clarified Understanding

The clarifier is a **draft-lifecycle component**: new tables (task_drafts, clarifier_runs, detection_records), a server-composed card payload, a backend selector with the mock as the MVP product, synchronous engine with an async-ready contract, visible fail-open, and a minimal config-gated operator path for holds. `POST /tasks` survives untouched; approval funnels into the existing launch service, which keeps fan-out ordering correct (C8). No longer viable: stateless clarify, client-composed cards, slot tables, queue infra, canon-violating hold shortcuts.

## Phase 4 — Degrees-of-Freedom Reduction

**Fixed:** the six resolutions above; module homes (SP1, house-flat); wire schema mirrors catalog §2.1 + versions (KI6); log rows per §2.6 in ledger house style; prompt-builder as contract-only module; acid cases as fixtures; config block `CLARIFIER_*` with catalog §4-constants as knobs + calibration gates.
**Eliminated:** LLM-everything (executor split is canon); re-asking field-backed data; lookups/tools in the LLM call; ToS/case-file/prompt-text content (MQ4); admin component.
**Remaining viable (open at BOM grain, named in the BOM):** real-vendor reference choice (protocol + one reference impl; vendor swap is config); draft TTL/cleanup policy; operator list → real roles migration path; exact thinking-state UX per client (freeze-gated prototype).

## SV5 — Constrained Understanding

The solution space is now one document away: a BOM = §0 decisions table (A1–A6 + inherited canon bindings) + ordered sections: (1) config & flags, (2) data model + migration, (3) wire schemas (LLM structured output; card payload), (4) backend abstraction (protocol, deterministic mock, real reference), (5) engine (executors, single pass, routing matrix, suppression, idempotency, card composition), (6) endpoints (draft lifecycle + resolutions + approve + hold), (7) client integration (bot + fe), (8) logging/audit, (9) tests & DoD. Effort ~4–5 days. In/out scope per MQ4.

## Phase 5 — Conceptual Stabilization / SV6 — Stabilized Model

**The clarifier component = a draft-lifecycle wrapper around the existing launch path, with the catalog as its rulebook and the LLM behind a house-pattern backend selector.**

1. **Draft resource** (A1): `task_drafts` + `clarifier_runs` + `detection_records`; status machine clarifying → awaiting_approval | held | declined | abandoned → launched. Approval calls the EXISTING `task_service.launch_task` (fan-out ordering preserved); `POST /tasks` untouched.
2. **Server-composed card payload** (A2): the consent-bearing artifact; persisted as-shown; clients render zones.
3. **JSON slots** (A3): on the run; copied to `tasks.normalized_slots` + `clarifier_run_id` at launch — the §6 output contract realized.
4. **Sync engine, async-ready contract** (A4): status field from day one.
5. **Backend selector + visible fail-open** (A5): off | mock | real; mock is deterministic and catalog-shaped (the MVP product); real failure degrades to code-only card with notice + audit.
6. **Minimal operator path** (A6): `OPERATOR_USER_IDS` + notifier + one resolve endpoint; admin tooling deferred.
7. The BOM document carries: decisions table (these six + canon bindings), the 9 ordered sections, in/out scope, effort, open knobs with calibration gates.

**Delta from SV1:** SV1 was "list the build steps." SV6 knows the BOM's real content is six adjudicated architecture decisions (each with a tested counter), one invented-minimal capability (operator gate) surfaced by frame-exit checking, and a build order whose first deliverable (mock backend) makes the component shippable before any LLM key exists.

**Ambiguity ledger:** 6 collapsed HIGH · 0 LOW · OPEN (named, carried to BOM): vendor reference choice, draft TTL, operator→roles path, thinking-state UX (freeze-gated).

## Saturation Telemetry

- Perspective saturation: reached — Definitional + Phase/Calibration confirmed rather than added new anchor TYPES; Risk and Frame-exit were the last to add new anchors (fail-open posture; operator gap).
- Ambiguity resolution: 6/6 collapsed; 4 OPEN explicitly carried (none silently dropped).
- SV delta: SV1→SV6 substantial (checklist → adjudicated architecture + invented capability).
- Anchor diversity: all five anchor types, seven perspectives, both inherited-canon and codebase-evidence sources.
- Failure modes scanned: Status Quo (draft-resource defended on §5.4 persistence forcing, not precedent comfort), Premature Stabilization (3 perspectives produced surprises: server-composition, fail-open, operator gap), Anchor Dominance (catalog dominates BY DESIGN as canon; A4/A5/A6 resolved from non-catalog anchors — house precedent, risk, frame-exit), Clean Resolution Trap (counters stated + structurally dismissed per collapse), Perspective Blindness (uncomfortable perspective WAS checked: fail-closed argument), Self-Reference (n/a — target is a code component, not a discipline).
