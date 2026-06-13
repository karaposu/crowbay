# filepath: devdocs/scoped/be/clarifier/bom.md

# Clarifier BOM — Draft Lifecycle + Detection Engine + Card

> **Status: IN PROGRESS** — §1–§4 implemented 2026-06-12 (foundations, contracts,
> backend abstraction incl. the deterministic mock, detection engine). ToS
> matrix v1 RATIFIED and propagated: catalog v1.3, entry CJ-C5, `tos_category`
> full-coverage logging, per-row kill-switches. 119 tests green (31 clarifier);
> ruff clean; migrations `a41c7e9d2b10` + `b7d31f8c4e22` applied. Note: the
> version-pin test caught real canon drift on its first run (catalog Status
> line lagged its own version notes — fixed). §5–§8 remaining. Derived in
> `devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/finding.md`
> (full reasoning, killed alternatives, open questions there).
> **Canon consumed:** `devdocs/task_consumer_catalog.md` v1.3 (detections,
> severities, card, output contract) + `devdocs/task_meta_definition.md`.
> This BOM implements canon; it never re-opens it. Update this header at
> implementation (pattern: backbone/matching BOMs).

The component that runs the task-consumer catalog inside the launch flow: a
**task-draft lifecycle** wrapped around the existing launch path. Clients
create a draft; one engine pass runs the 19 detections; a server-composed
card comes back; the Launcher resolves and approves; approval calls the
EXISTING `task_service.launch_task`. Estimated **4–5 days solo**; effort per
section.

**In scope:** config, draft/run/log tables, wire schemas + catalog registry,
LLM backend abstraction (mock first), detection engine, card composition,
lifecycle endpoints, bot+fe card integration, tests.
**Out of scope** (separate routes/components): prompt TEXT authoring,
case-file corpus, eval/replay harness, admin/roles component, ToS-posture
decision, verification evidence.

---

## 0. Decisions encoded here (veto before starting)

| Decision | Choice | Why |
|---|---|---|
| Seam | task-draft resource; `POST /tasks` untouched; approval → existing `launch_task` (fan-out ordering preserved) | catalog §5.4: card-as-shown + resolutions must persist across interactions — stateless/clientside variants can't hold the consent record |
| NOT drafts-on-tasks | new tables, not `status='draft'` on tasks | verified: `browse_tasks` (no default status filter) + `my_tasks` (no status filter) would leak drafts; "a Task row is launched" is load-bearing |
| Card | server-composed payload (zones, semantic marks, chips w/ entry codes, CTA lock); clients render layout only; payload persisted as-shown = approval record | consent content must not drift between two clients |
| Payload vocab | platform-neutral; zero client markup | clients map marks → their own widgets |
| Slots | JSON on run; copied to `tasks.normalized_slots` + `tasks.clarifier_run_id` at launch | catalog §6 realized; relational slot schema = calibration-era |
| Engine call | sync in-request; status field + polling shape from day one (async swap changes no contract) | house seam pattern (fan-out precedent) |
| Backend | `CLARIFIER_BACKEND = off \| mock \| <real>`; protocol `(submission, wizard_context, registry) → LLMOutput`; **no tools, no lookups** | pluggable-backend house pattern; definedness ≠ truth enforced structurally |
| Failure | retry once → **visible fail-open**: code-only card + "AI review unavailable" warn + audit `clarifier.skipped` + `not-evaluated` log rows | fail-closed = platform outage to protect a week-old gate; revisit at ToS decision |
| Holds (CJ-K3 uncertain) | draft `held`; `OPERATOR_USER_IDS` config; notify via existing notifier; one operator-gated resolve endpoint | canon forbids auto-decline on uncertainty; no admin concept exists — minimal invention, roles component later |
| Canon coupling | registry mirrors catalog §4 → feeds engine + prompt-builder + mock; version-pin test (hard) + literal scan (advisory) + unknown-code tolerance — **one unit** | drift becomes CI failure, not silent divergence |
| Retention | `CLARIFIER_DRAFT_TTL_DAYS: int \| None = None` + cleanup fn (default off) | PII retention prosecution hit; mechanism ships, policy open |
| Abuse | `CLARIFIER_RUNS_PER_USER_PER_HOUR` cap (429) | first token-spend guard |

## 1. Foundations (~0.5d)

- [x] `CLARIFIER_*` config block in `Settings`: backend selector, knobs mirroring catalog §4 constants (w/ calibration-gate comments), `OPERATOR_USER_IDS`, TTL knob, rate cap; fail-fast validation when backend=real
- [x] `db/models/clarifier.py`: `task_drafts` (owner_id, payload JSON, status, timestamps; statuses: clarifying → awaiting_approval | held | declined | abandoned → launched), `clarifier_runs` (draft FK, submission_hash, catalog_version, llm_output JSON, card_payload JSON, status), `detection_records` (run FK, code, entry_version, result, severity_at_fire, response_shown, resolution) — ledger house style; records reference the run, never copy submission text
- [x] migration: the three tables + `tasks.normalized_slots` (JSON) + `tasks.clarifier_run_id` (FK)
- [x] status machine documented on the model; transitions enforced server-side (consumed by §6)

## 2. Contracts & catalog registry (~0.5d — parallel with §1)

- [x] `services/clarifier_registry.py`: entries mirroring catalog v1.2 §4 — code, class, severity, executor, escalation/override flags, response templates, version. THE only place entry codes/templates live
- [x] `schemas/clarifier.py`: LLM structured-output schema (per-entry results: clear|fired|uncertain, slots, drafts; catalog + per-entry versions) · RunResult (engine→composer) · card payload (ordered zones; diff marks replacement/addition/unchanged; chip objects kind+entry-code+value; rationale lines; preview line; CTA lock state) · consensus-snapshot→TaskCreate mapping
- [x] unknown-code tolerance: log readers/clients ignore codes they don't know (catalog extension ⇒ no migration)
- [x] canon-coupling tests: registry version == catalog version note (HARD fail) · no entry-code literals outside registry (advisory scan)

## 3. Backend abstraction (~0.5d)

- [x] protocol: `(submission, wizard_context, registry) -> LLMOutput`; no tool access; desc passed strictly as data
- [x] `MockClarifierBackend`: deterministic, rule-driven, catalog-shaped — full acid-case coverage (catalog §7). **The MVP product and the demo**, not a stub
- [x] real reference backend behind the selector — now a LangChain `with_structured_output(ConsumerReport)` call (Anthropic); ConsumerReport subclasses the 11-attribute `AttributeReport` and adds the 9 channel/composition judgments + tos_category + slots, ONE pass; config-gated latency injection for §8's slow-sim. Untested vs live API until §8 smoke
- [x] prompt-builder: explicit production prompts now live in `services/prompts/` — `clarification_prompts.SEMANTIC_ATTRIBUTE_CHECKER` (the 11) + `consumer_prompts.CHANNEL_COMPOSITION_ADDENDUM` (the rest). `build_system_prompt` kept as the registry-rendered CONTRACT/reference. (Partly advances detections route 10 — prompt-seed rendering; case-file few-shots still pending)
- [x] retry-once → typed failure the engine converts to a degraded run

## 4. Detection engine (~1d)

- [x] code executors: length guard (`MIN_TASK_CHARS`), pay/effort ratio (code half), field presence — field-backed data never re-asked
- [x] single-pass orchestration: channel → kind → instance+composition; suppression per catalog §2.5 (X1 gate stops all → `not-evaluated`; X3 fired → instance entries `not-evaluated`; kind-gate fired → evaluate+log, render decline only)
- [x] routing matrix (catalog §2.3) as data, not if-chains — incl. K3-uncertain → hold
- [x] content-hash idempotency: identical submission+context ⇒ cached run
- [x] detection-log writes (§2.6 row shape); resolutions updatable post-run; degraded mode (backend failure ⇒ code-only run + audit)
- [x] rate-cap enforcement (429 before any LLM call)

## 5. Card composition (~0.5d)

- [ ] RunResult + registry templates → card payload, zones in catalog §5.2 order
- [ ] diff discipline: every consumer change visible; Launcher's original reconstructible from the card alone
- [ ] chips: mandatory free-text escape; ≤4 per item; stet only on replacement proposals; CJ-I7's `[Keep as one]` declared override
- [ ] ≤3 blocking questions; thin-submission overflow swap; CTA lock until resolved
- [ ] archetype variants: green receipt · clarify card · transform-lead · decline 4a/4b · hold notice
- [ ] composition budget: Telegram 4096-char limit enforced server-side (trimming rules + maximal-card fixture)
- [ ] audience-preview line composed server-side (engine holds the filters; draft-flow clients stop calling the preview endpoint; legacy flow keeps it)
- [ ] payload persisted as-shown on the run

## 6. Draft lifecycle endpoints (~0.5d)

- [ ] `POST /tasks/drafts` (create + run; client idempotency key honored — unique-constraint dedupe, ledger pattern)
- [ ] `GET /tasks/drafts/{id}` (status + card payload)
- [ ] `POST /tasks/drafts/{id}/resolutions` (chip / typed / stet / override per entry code)
- [ ] `POST /tasks/drafts/{id}/revise` (new text ⇒ new run; unchanged ⇒ cached; resolutions persist where inputs unchanged)
- [ ] `POST /tasks/drafts/{id}/approve` (consensus snapshot → `task_service.launch_task` → existing audit + fan-out)
- [ ] `POST /tasks/drafts/{id}/hold-resolution` (gated on `OPERATOR_USER_IDS`)
- [ ] held drafts notify operators via existing notifier; transitions audited via existing audit service + `clarifier.skipped`
- [ ] capability exposure (flag state) so clients can branch; `POST /tasks` untouched

## 7. Client integration (~1–1.5d)

- [ ] bot: confirm step branches to draft flow when capability on; thinking state during the run; zones → message HTML + inline keyboards (callback = entry code + choice); typed answers via reply; off ⇒ exactly today's flow
- [ ] fe: same branch; zones → DOM; chips = buttons; launch disabled until CTA unlock
- [ ] both render from payload only — zero composition logic client-side
- [ ] **off-flag parity test** (DoD gate): backend=off draft flow renders content-equivalent to today's `summary_text` across: budget, slots×pay, audience line (privacy-floor wording), deadline, mode, raw-statement warning
- [ ] this section IS the catalog §5.3 two-client prototype — may adjust LAYOUT, never consent rules (diff visibility, stet scope, question budget)

## 8. Tests & definition of done (~1d)

- [ ] routing-matrix grid: every severity × result cell
- [ ] mock contract test: catalog-shaped output for every entry; mock validates against the SAME schema as real
- [ ] acid round-trips: catalog §7 cases → expected archetype, end-to-end through endpoints
- [ ] idempotency · revision · degradation (slow-backend sim via injected mock latency) · hold path · rate cap
- [ ] consent invariants as tests: no silent rewrite (diff completeness) · CTA lock · decline renders alone
- [ ] canon-coupling tests green (§2)
- [ ] manual real-backend smoke checklist (non-CI; once a key exists)
- [ ] DoD: all green via mock only · ruff clean · this header updated to IMPLEMENTED w/ deviations noted

## Sequencing & dependencies

§1 ∥ §2 (contract producers) → §3 ∥ §4 (§4 tests use §3's mock) → §5 → §6 → §7 → §8 integration tier (unit tests live inside each section as built). Depends on: backbone (done), matching (done — preview, notifier, audit), catalog v1.2 (done).

## Incident playbook (ToS matrix v1 — one paragraph, drilled before needed)

On a purge wave, platform contact, or C&D touching a task category:
**1)** flip the row into `CLARIFIER_TOS_KILLED_ROWS` (config; gates the row
instantly, no deploy); **2)** notify affected Launchers (open tasks in the
row) and Jumpers (active jumps) via the existing notifier; **3)** refund
stance per the payments component's published rule (until that exists: the
operator decides case-by-case and records it in audit); **4)** the matching
revisit gate fires — the row's disposition is re-decided, in the open
(TASK_POLICY.md is updated and versioned). A C&D additionally means: preserve
the contacted row's detection log unmodified and seek counsel before
replying.

## Open knobs (config now, decide later)

- **fail-open coupling rule (from the ratified ToS posture):** any GATED ToS
  row must be acceptable-to-miss during fail-open at current scale, else
  fail-open degrades to fail-hold. At MVP: acceptable (gated rows are
  law-floor categories whose fail-open miss risk equals the pre-existing K3
  residual; operator eyeballs cover dev volume). Re-assess at the production
  revisit gates.
- `CLARIFIER_TOS_KILLED_ROWS` — per-row kill-switch (config flip = instant
  gate for a matrix row; incident playbook step 1)
- TTL value (knob ships default-off; retention policy open — PII posture)
- real-backend vendor (protocol isolates; pick at §3)
- operator list → roles component (migration path; graduates when holds have traffic)
- async swap (status contract ready; activates on p95 latency evidence)
- all numeric knobs carry calibration gates (≥100 real submissions / fill-rate data)
