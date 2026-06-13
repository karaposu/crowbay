---
status: active
model: claude-fable-5
effort: max
---
# Finding: Clarifier Component BOM (Structural Layer)

## Question

From `_branch.md`: **what should the clarifier component's BOM (bill of materials) be** — the structural spec under `devdocs/scoped/be/clarifier/` covering placement, endpoints, invocation, the revision loop, and the LLM wire schema — consuming `devdocs/task_consumer_catalog.md` v1.2 and `devdocs/task_meta_definition.md` as canon. This is route 4 of the task-consumer inquiry's route-map; the catalog's §2.4 explicitly assigns "the concrete JSON schema, prompt assembly, and invocation plumbing" to this BOM. Open readings preserved through the pipeline: work-order checklist vs architecture record vs both; spec-only vs spec-then-build. Excluded by the question itself: re-opening catalog semantics, writing the implementation, the ToS-posture decision, case-file/prompt-text authoring.

## Finding Summary

- **The clarifier is a draft-lifecycle wrapper around the existing launch path.** Clients create a **task draft**; the engine runs the catalog's 19 detections in one pass; the result renders as a server-composed card; the Launcher resolves and approves; approval calls the EXISTING `task_service.launch_task` — so `POST /tasks` and the fan-out ordering stay untouched.
- **Six architecture decisions were adjudicated with tested counters**: draft resource (not stateless clarify — the consent record must be written across interactions) · server-composed card payload (consent content can't drift between two clients) · normalized slots as JSON copied run→task (relational schema is calibration-era work) · synchronous engine with an async-ready status contract · backend selector `off | mock | real` with **visible fail-open** (one retry, then code-only card + audit event) · a **minimal operator gate** (`OPERATOR_USER_IDS`) for policy holds, because no admin concept exists anywhere in the backend yet.
- **The mock backend is the MVP product, not a test stub**: deterministic, catalog-shaped, covering the acid cases — the entire flow ships and demos before any LLM API key exists, and CI stays keyless.
- **A canon-as-code spine keeps the catalog and the code coupled**: one registry module mirrors the catalog's entries and feeds the engine, the prompt builder, AND the mock; a version-pin test fails CI when the catalog and registry drift; log readers tolerate unknown entry codes so future catalog extensions need no migration.
- **The rollout is provably non-breaking**: an off-flag parity test (the draft flow with clarifier off renders the same confirm content as today's `summary_text`), a slow-backend simulation, a server-side Telegram size budget, and a client idempotency key together form the ship-without-breaking-launch gate.
- The strongest challenger — **storing drafts as `status='draft'` rows on the existing tasks table instead of new tables — was killed on verified code anchors**: `browse_tasks` applies no status filter by default and `my_tasks` returns all owner rows, so drafts would leak into existing surfaces; the "a Task row is a launched thing" invariant is load-bearing across the codebase.
- Effort estimate: **~4–5 focused days** across 8 ordered sections; the build can start with the two contract-producing sections in one session.
- The deliverable BOM document is extracted to **`devdocs/scoped/be/clarifier/bom.md`** (the MUST below); the onward field (16 typed routes) lives in this inquiry's route-map.

## Finding

Crowdjump's launch flow currently sends free text straight to `POST /tasks`. The two prior inquiries defined what a well-formed task IS (the meta-definition) and what the consuming LLM DOES (the catalog: 19 detections, severity routing, the marked-up-draft card, the output contract). This inquiry designed the missing structural layer: the backend component that runs that catalog inside the real codebase. The answer is the BOM below — a decisions table plus eight ordered, checkbox-style build sections, in the same shape as the project's backbone and matching BOMs.

### 1. Decisions encoded (veto before building)

| Decision | Choice | Ground |
|---|---|---|
| Invocation seam | **Task-draft resource** (`task_drafts` + `clarifier_runs` + `detection_records`), approval funnels into existing `task_service.launch_task`; `POST /tasks` untouched | catalog §5.4 requires persisting the card-as-shown plus every resolution, and resolutions arrive across multiple interactions — stateless variants can't hold that record. Client-side variants are pinned out by the same persistence requirement plus two clients (the kill of "bot calls the LLM directly" named this: the consent record pins the clarifier server-side) |
| Why not drafts-on-tasks-table | new tables, NOT `status='draft'` on tasks | verified anchors: `browse_tasks` with `status_filter=None` applies no status filter; `my_tasks` has no status filter — drafts would leak into existing read paths; every future Task consumer would need draft-awareness forever |
| Card composition | server-composed **card payload** (ordered zones, semantic diff marks, chips with entry codes, CTA lock state); clients render layout only | diff visibility and stet scope are committed consent rules; two clients composing independently would drift on exactly the content that legally matters; the persisted payload IS the approval record |
| Payload vocabulary | platform-neutral semantic marks; zero client markup in the payload | two clients today, more later; HTML-in-JSON is dearer than semantic marks |
| Normalized slots | JSON on the run; copied to `tasks.normalized_slots` + `tasks.clarifier_run_id` at launch | slot consumers read per-task values at MVP; relational slot schema is calibration-era; ledger house style (JSON payload column) is the norm |
| Engine posture | synchronous in-request; status field + polling shape from day one so the async swap changes no API contract | house precedent (fan-out: "synchronous at MVP; the seam should allow moving to a background job without API changes") |
| Backend | `CLARIFIER_BACKEND = off \| mock \| <real>`; protocol `(submission, wizard_context, registry) → LLMOutput`, no tools, no lookups | the pluggable-backend house pattern (email/SMS/notify); definedness ≠ truth is enforced structurally by giving the LLM no tools |
| Failure posture | retry once, then **visible fail-open**: code-executor-only card + "AI review unavailable" warn + audit `clarifier.skipped` + LLM entries logged `not-evaluated` | fail-closed turns an LLM outage into a platform outage to protect a gate that didn't exist last week; visibility, not blockage, is the MVP requirement — revisit at the ToS-posture decision |
| Policy holds (CJ-K3 uncertain) | draft status `held`; operators = `OPERATOR_USER_IDS` config list; notified via existing notifier; one operator-gated resolve endpoint | the catalog forbids auto-decline on uncertainty; NO admin/operator concept exists in the backend — this is the minimal invention, with the real roles component deferred |
| Canon coupling | registry module mirrors catalog §4; version-pin test (hard) + code-literal scan (advisory) + unknown-code tolerance — one unit, never split | the registry is the single executable form of the catalog; the pin test turns silent drift into CI failure |
| Retention | `CLARIFIER_DRAFT_TTL_DAYS: int \| None = None` (knob ships, default off) + cleanup function | unbounded PII retention was a sustained prosecution hit; the policy stays open, the mechanism ships |
| Abuse guard | `CLARIFIER_RUNS_PER_USER_PER_HOUR` rate cap (code executor; 429) | the first real token-spend guard; submission text is already capped at 5000 chars |

### 2. The eight build sections (dependency order)

**§1 Foundations** *(~0.5d)* — `CLARIFIER_*` config block (selector, knobs mirroring the catalog's provisional constants with calibration-gate comments, operator list, TTL knob, rate cap; fail-fast validation when backend=real) · three tables in ledger house style: `task_drafts` (owner, payload JSON, status: clarifying → awaiting_approval | held | declined | abandoned → launched), `clarifier_runs` (draft FK, submission hash, catalog version, LLM output JSON, card payload JSON), `detection_records` (run FK, code, entry_version, result, severity_at_fire, response_shown, resolution — referencing the run, never copying submission text) · `tasks.normalized_slots` + `tasks.clarifier_run_id` columns · one Alembic migration.

**§2 Contracts & catalog registry** *(~0.5d, parallel with §1)* — the registry module (entries: code, class, severity, executor, escalation/override flags, response templates, version — mirroring catalog v1.2 §4) · LLM structured-output schema (per-entry results, slots, drafts, versions) · the internal RunResult shape · the card payload schema (zones, diff marks: replacement/addition/unchanged, chip objects, rationale lines, preview line, CTA lock) · consensus-snapshot→TaskCreate mapping · unknown-code tolerance · the canon-coupling tests (version pin = hard; literal scan = advisory).

**§3 Backend abstraction** *(~0.5d)* — the protocol; the **deterministic mock** (rule-driven, full acid-case coverage — the MVP product and the demo); the real reference implementation behind the selector (vendor named at implementation; structured output enforced; desc passed strictly as data); the prompt-builder CONTRACT only (`(registry, case files) → system prompt` — authoring the prompt text is its own later route); retry-once → typed failure the engine converts to a degraded run.

**§4 Detection engine** *(~1d)* — code executors (length guard, pay/effort ratio half, field presence — field-backed data never re-asked) · single-pass orchestration with the catalog's suppression rules (injection gate stops everything; degenerate input → instance entries `not-evaluated`; a fired kind-gate still logs instance results but renders only the decline) · the routing matrix as data, not if-chains, including the policy-hold path · content-hash idempotency (identical submission+context returns the cached run) · detection-log writes with post-run resolution updates · degraded mode.

**§5 Card composition** *(~0.5d)* — RunResult → card payload: zone assembly in the catalog's fixed order; diff discipline (every change visible; the Launcher's original reconstructible); chips with the mandatory free-text escape, stet only where legal, the atomic-split's `[Keep as one]` override; ≤3 blocking questions with the thin-submission overflow swap; CTA lock until resolved; archetype variants (green receipt / clarify card / transform-lead / decline-with-repair / decline-alone / hold notice); **server-side composition budget** for Telegram's 4096-char limit (trimming rules, never client truncation); **the audience-preview line composed server-side** (the engine already holds the filters; draft-flow clients stop calling the preview endpoint; it stays for the legacy flow); payload persisted as-shown.

**§6 Draft lifecycle endpoints** *(~0.5d)* — `POST /tasks/drafts` (create + run; **client idempotency key** honored) · `GET /tasks/drafts/{id}` (status + card) · `POST .../resolutions` (chip/typed/stet per entry) · `POST .../revise` (new text ⇒ new run; unchanged ⇒ cached; resolutions persist where inputs didn't change) · `POST .../approve` (consensus snapshot → existing launch service → fan-out unchanged) · `POST .../hold-resolution` (operator-gated) · server-side transition enforcement · audit rows per transition (existing audit service) + `clarifier.skipped` · capability exposure so clients know the flag state · `POST /tasks` remains for direct API launches.

**§7 Client integration** *(~1–1.5d)* — bot: confirm step branches to the draft flow when the capability is on; thinking state while the run executes; zones → message HTML + inline keyboards (callback = entry code + choice); typed answers via reply; flag off ⇒ exactly today's flow. Web client: same branch; zones → DOM; launch button disabled until CTA unlock. Both render from the payload only. This section IS the catalog's two-client prototype that can unfreeze the card layout (it may adjust layout, never the consent rules). DoD gate: the **off-flag parity test** — with the clarifier off, the draft flow's confirm content is equivalent to today's `summary_text` across the enumerated fields (budget, slots×pay, audience line with privacy-floor wording, deadline, mode, raw-statement warning).

**§8 Tests & definition of done** *(~1d)* — routing-matrix grid (every severity × result cell) · mock contract test (catalog-shaped output for every entry, same schema as real) · acid round-trips (catalog §7 → expected archetype, end-to-end through the endpoints) · idempotency, revision, degradation (slow-backend simulation with injected mock latency), hold-path, rate-cap tests · consent invariants as tests (no silent rewrite; CTA lock; decline renders alone) · canon-coupling tests from §2 · manual real-backend smoke checklist (non-CI; runs once a key exists) · DoD: all green via mock only, ruff clean, BOM status header updated.

### 3. What this realizes from the canon

The catalog's §2.4 deferred three deliverables to this BOM — all three land here: the **wire schema** is §2's structured-output contract; **prompt assembly** is §3's builder contract (text deliberately not authored — that is the prompt-seed route on the route-map); **invocation plumbing** is §6's lifecycle. The output contract (catalog §6) is realized by the normalized-slots copy at approval; the detection log (catalog §2.6) by §1's `detection_records`; the card spec (catalog §5) by §5's composition rules. Nothing in the catalog was re-opened.

## Next Actions

### MUST
- **What:** Extract the BOM to its canonical home `devdocs/scoped/be/clarifier/bom.md` (decisions table + 8 checkbox sections + in/out scope + effort + open knobs, without inquiry apparatus)
  **Who:** AI session (this one) · **Gate:** immediately after this finding is filed · **Why:** the build sessions need a stable, citable work-order — the established pattern (backbone, matching) the team already executes against

### COULD
- **What:** Begin implementation with §1 Foundations + §2 Contracts in one session (the contract producers everything else consumes)
  **Who:** AI session with user · **Gate:** user's go ("lets do this" arguably already consents; confirming at finding time per the extent ambiguity the articulation preserved) · **Why:** closes the MVP pipeline gap; the mock-first order means visible progress without any API key
  **Depends-on:** MUST item "Extract the BOM". This COULD is GATED — the sections cite the canonical doc.
- **What:** Decide the real-backend reference vendor when §3 is built
  **Who:** user (cost/key ownership) · **Gate:** §3 implementation start · **Why:** the protocol isolates the choice; only the reference adapter and smoke checklist depend on it

### DEFERRED
- **What:** Replay/eval harness (re-run logged submissions against a new registry/prompt version) — **Gate:** first registry or prompt change after ≥50 real runs — **Why (if revived):** regression safety for canon evolution
- **What:** Hold-path operations (SLA wording, operator re-ping) — **Gate:** operator practice data exists — **Why:** ergonomics without traffic is guesswork
- **What:** Async migration (engine call → background job) — **Gate:** observed p95 draft-creation latency exceeds clients' tolerable thinking-state duration — **Why:** the status contract already supports it; only volume justifies the infra
- **What:** Drafts-merge-into-tasks reconsideration — **Gate:** a future major migration WITH a full Task-consumer audit in hand — **Why:** the kill was blast-radius-based; a measured radius could re-open it

## Reasoning

- **Draft resource over stateless clarify**: the catalog requires the approval record to store the card-as-shown plus every resolution, and resolutions arrive after the run as the Launcher interacts. A stateless endpoint (or approval-token replay) re-implements persistence badly — size, audit, abandonment tracking all lost. This was the load-bearing collapse; four other decisions inherit from it.
- **The zero-new-tables challenger was killed twice, the second time with code anchors.** Innovation killed it on argued task-invariant grounds and flagged its own kill as the most uncomfortable one (survival-bias guard); critique re-prosecuted it independently and confirmed with verbatim evidence — `browse_tasks` filters status only when a filter is passed, and `my_tasks` has no status filter at all, so drafts would surface in existing lists labeled as launched tasks. The seed survives: with a consumer audit, a future migration could merge the tables.
- **Client-side clarifier killed at system level**: iterating the inversion produced the structural pin — the consent record's persistence requirement plus two clients leaves no client-side variant. The kill's value is the pin itself, now named in the decisions table.
- **Fail-open over fail-closed** (with the counter taken seriously: "a policy gate that opens on outage isn't a gate"): the platform today has NO gate; failing closed converts an LLM outage into a total launch outage to protect a week-old control, while the operator-review backstop is unchanged. The commitment is visibility — warn line, audit event, honest `not-evaluated` logging — and the posture is explicitly revisit-gated on the ToS decision.
- **Skip-holds-at-MVP killed**: mapping policy-uncertainty to decline is exactly what the catalog forbids (auto-decline on uncertainty was critique-tested in the prior inquiry); building against canon on day one would also corrupt the calibration log's semantics. Hence the minimal operator gate — the inquiry's frame-exit catch (no operator concept existed anywhere).
- **Runtime catalog-doc parsing killed** (the registry's piece-level inversion): parsing prose canon at runtime is untestable and inverts the canon/build relationship. The registry is the single executable mirror, and the version-pin test makes its one risk — drift — a CI failure instead of a silent divergence.
- **Two refinements from prosecution hits**: unbounded retention → the TTL knob ships now (default off, policy open); "content-equivalence" in the parity test was hand-waving → the parity fields are enumerated.
- **Incremental per-step clarification killed** by the single-pass canon and the interrogation pattern killed one inquiry earlier; preserved as a production-era seed alongside inline-as-you-type.
- Inheritance note: this finding operates the catalog v1.2 and the meta-definition as given canon and re-tests none of their commitments by design (both are days-old, critique-tested, with their own monitoring questions). What this inquiry added is the structural layer beneath them; the frame-premise "the catalog's semantics are right" is mitigated independently by the canon-coupling spine plus the calibration log.

## Open Questions

### Monitoring
- Does the mock-first order hold through implementation (does any section secretly need the real backend before §8)?
- Fail-open rate once backend=real: a non-trivial `clarifier.skipped` rate means the retry policy or vendor choice needs revisiting.

### Blocked
- Policy-floor wording and the fail-open posture's production stance: blocked on the ToS-posture decision (PROJECT.md → Open Decisions).
- All numeric knobs (question cap, rate cap, effort heuristics): blocked on real submissions.

### Research Frontiers
- Sub-second/near-free LLM calls would make inline-as-you-type clarification plausible; the draft seam is unaffected, but the interaction model would re-open.

### Refinement Triggers
- If p95 draft-creation latency exceeds what the thinking state can hold, the async seam activates (contract already in place).
- If the operator hold queue sees real traffic, the minimal gate graduates to the roles/admin component.
- If chip-resolution data shows high stet rates on specific entries, the proposal templates (registry) re-open — a registry change, not a schema change.

## Source Input

<details>
<summary>Raw user input for this finding</summary>

```text
the clarifier component BOM (structural layer)    project-space    teleological    INVESTIGATE-FRONTIER    HIGH

lets do this
```

</details>
