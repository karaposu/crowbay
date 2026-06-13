# Decomposition — Clarifier Component BOM

## User Input

/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/_branch.md
(operating on sensemaking SV6: draft-lifecycle wrapper, six collapsed decisions A1–A6)

## Step 1 — Coupling Map

Elements: config knobs · draft/run/detection tables · task columns + migration · LLM output schema · card payload schema · catalog-as-code registry (entry codes, severities, executors, templates, versions) · backend protocol · mock backend · real backend reference · prompt-builder contract · code executors · single-pass orchestration · routing matrix · suppression · content-hash idempotency · detection-log writes · card composition (zones/diffs/chips) · archetype variants (green/transform/decline/hold) · draft endpoints · resolutions · approve→launch · hold-resolve · operator gate · audit events · capability flag · bot rendering · fe rendering · thinking state · off-flag fallback · acid fixtures · matrix test grid · round-trip tests.

**Clusters (high internal coupling):**
- K1 *persistence+config*: tables ↔ status machine ↔ config keys ↔ migration (change a status → schema + transitions move together)
- K2 *contracts*: LLM output schema ↔ card payload schema ↔ catalog registry ↔ versioning (a new entry field propagates through all three)
- K3 *backend*: protocol ↔ mock ↔ real ↔ retry/fail-open ↔ prompt-builder contract (all implement/feed one interface)
- K4 *engine*: executors ↔ orchestration ↔ routing ↔ suppression ↔ hash ↔ log writes (one pass, shared run state)
- K5 *composition*: zones ↔ diffs ↔ chips ↔ CTA lock ↔ archetype variants (all render one RunResult into one payload)
- K6 *lifecycle API*: endpoints ↔ transitions ↔ approve/fan-out ordering ↔ hold/operator ↔ audit ↔ capability flag
- K7 *clients*: bot ∥ fe rendering ↔ thinking state ↔ chips→resolutions ↔ fallback (two parallel consumers of one payload)
- K8 *verification*: fixtures ↔ grids ↔ round-trips (consume everything via public contracts only)

**Valleys (low coupling = boundaries):** K2↔K4 cross only via typed schemas; K4↔K5 cross only via RunResult; K5↔K7 cross only via the payload; K3↔K4 cross only via the protocol. K1 is contract-stable to everyone.

## Step 2 — Boundaries (Top-Down)

Cut at the valleys → 8 pieces: P1=K1, P2=K2, P3=K3, P4=K4, P5=K5, P6=K6, P7=K7, P8=K8. Card composition (P5) is deliberately cut FROM the engine (P4): the engine answers "what fired?", composition answers "what does the Launcher see?" — they share only RunResult, and catalog §2 governs P4 while §5 governs P5 (different canon sections = different change drivers).

## Step 3 — Bottom-Up Validation

Atoms: status enum → K1 ✓ · content-hash util → K4 ✓ · chip object → K2 ✓ · retry-once rule → K3 ✓ · `OPERATOR_USER_IDS` → K1 (config) with its consumer in K6 ✓ (config-vs-use split is normal, not a broken atom) · fan-out call site → K6 ✓ · diff-mark triple → K2 (shape) vs K5 (production) ✓ same pattern · acid fixture set → K8 ✓ · catalog version pin → K2 ✓. No atom is split against its cluster; no cluster holds independent atoms. **Confidence: HIGH (directions agree).**

## Step 4 — Question Tree

**P1 — Foundations.** *What persistent state and configuration does the clarifier need?*
- [ ] `CLARIFIER_*` config block: backend selector (off|mock|real), knobs mirroring catalog §4 constants w/ calibration-gate comments, `OPERATOR_USER_IDS`, fail-fast validation when backend=real
- [ ] `task_drafts` (owner, payload JSON, status enum, timestamps), `clarifier_runs` (draft FK, submission hash, catalog version, LLM output JSON, card payload JSON, status), `detection_records` (run FK, code, entry_version, result, severity_at_fire, response_shown, resolution) — ledger house style
- [ ] `tasks.normalized_slots` JSON + `tasks.clarifier_run_id` FK columns
- [ ] one Alembic migration; status machine documented on the model
- [ ] draft TTL/cleanup decision recorded (open knob acceptable)

**P2 — Contracts & catalog registry.** *What exact shapes cross every boundary, and where does canon live as code?*
- [ ] catalog registry module: entries (code, class, severity, executor, escalation/override flags, response templates, version) mirroring catalog v1.2 §4 — the single in-code canon mirror
- [ ] LLM structured-output schema (per-entry results, slots, drafts) + versions (catalog + per-entry)
- [ ] RunResult internal shape (engine→composition)
- [ ] card payload schema: ordered zones, diff marks (replacement/addition/unchanged), chip objects (kind, entry code, value), rationale lines, preview line, CTA lock state
- [ ] consensus-snapshot→TaskCreate mapping defined
- [ ] schema-version policy: log rows uninterpretable without versions = test-enforced

**P3 — Backend abstraction.** *How does the engine talk to an LLM without caring which one?*
- [ ] protocol: `(submission, wizard_context, registry) -> LLMOutput` — no tools, no lookups (FP2 structural)
- [ ] deterministic mock: catalog-shaped, rule-driven (substring/heuristic), covers every entry + acid cases — the MVP product
- [ ] real reference impl behind the selector (vendor named at implementation; structured-output enforced; desc passed as data)
- [ ] prompt-builder CONTRACT only: `(registry, case files) -> system prompt` (route 10 executes later; no prompt text here)
- [ ] retry-once → visible fail-open signal (typed error the engine converts to degraded run)

**P4 — Detection engine.** *How does one submission revision become a recorded run?*
- [ ] code executors (length guard, pay/effort ratio code half, field-presence) — never re-ask field-backed
- [ ] single-pass orchestration: channel → kind → instance+composition; suppression rules (X1 gate stop; X3 → not-evaluated; kind-gate fired → evaluate+log, render-decline)
- [ ] routing matrix (§2.3) implemented as data, not ifs — incl. K3-uncertain → hold
- [ ] content-hash idempotency: identical submission+context ⇒ cached run
- [ ] detection-log writes per §2.6 row shape; resolutions updatable post-run
- [ ] degraded mode: backend failure ⇒ code-only run, LLM entries not-evaluated, audit `clarifier.skipped`

**P5 — Card composition.** *How does a RunResult become the consent-bearing card?*
- [ ] zone assembly in fixed order (§5.2 table) from RunResult + registry templates
- [ ] diff discipline: every change visible (replacement/addition/unchanged marks); Launcher's original reconstructible
- [ ] chips per item incl. mandatory free-text escape; ≤4/row; stet only where legal; I7 `[Keep as one]` override
- [ ] ≤3 blocking questions + thin-submission overflow swap; CTA lock until resolved
- [ ] archetype variants: green receipt · clarify card · transform-lead · decline 4a/4b · hold notice
- [ ] payload persisted as-shown on the run (the §5.4 approval record)

**P6 — Draft lifecycle endpoints.** *How do clients drive a draft from submission to launch?*
- [ ] `POST /tasks/drafts` (create+run) · `GET /tasks/drafts/{id}` (status+card) · `POST .../resolutions` (chip/typed/stet per entry) · `POST .../revise` (new text ⇒ new run; unchanged ⇒ cached) · `POST .../approve` (consensus snapshot → existing `task_service.launch_task` → fan-out unchanged) · `POST .../hold-resolution` (operator-gated)
- [ ] status transitions enforced server-side; held drafts notify operators via existing notifier
- [ ] audit events: draft.created/approved/declined/held/abandoned + clarifier.skipped
- [ ] capability exposure so clients know flag state (config endpoint or draft-create response)
- [ ] `POST /tasks` untouched (direct API launch remains legal)

**P7 — Client integration.** *How do both clients render the card and drive the loop?*
- [ ] bot: confirm step branches to draft flow when capability on; thinking state; zones → message HTML + inline keyboards (callback = entry code + choice); typed answers via reply; off ⇒ exactly today's flow
- [ ] fe: same branch; zones → DOM; chips = buttons; launch button disabled until CTA unlock
- [ ] both render from payload only (zero composition logic client-side)
- [ ] freeze-gate honored: this piece IS the two-client prototype that can adjust §5.3 layout (not consent rules)

**P8 — Tests & definition of done.** *How do we know it's correct and complete?*
- [ ] routing-matrix grid test (every severity × result cell)
- [ ] mock-backend contract test (catalog-shaped output for every entry)
- [ ] acid round-trips (catalog §7 → expected archetype end-to-end through endpoints)
- [ ] idempotency + revision + degradation + hold-path integration tests
- [ ] consent invariants as tests: no silent rewrite (diff completeness), CTA lock, decline-renders-alone
- [ ] DoD: all green via mock backend only (no API key in CI); ruff clean; BOM status header updated

## Step 5 — Interface Map

| From → To | What flows | Direction | Assumption check (hidden-coupling probe) |
|---|---|---|---|
| P1 → P2..P8 | table/model names, status enum, config keys | one-way contract | P6 assumes transitions live server-side with the models (stated in P1) |
| P2 → P3 | LLMOutput schema + registry | one-way | mock must validate against the SAME schema as real (test in P8) |
| P2 → P4 | registry (executors, severities), RunResult shape | one-way | engine assumes registry is the ONLY canon source (no literals) — drift guard |
| P2 → P5 | payload schema + response templates | one-way | composition assumes templates carry rationale text keyed by entry code |
| P2 → P6 | snapshot→TaskCreate mapping | one-way | approve assumes existing `launch_task` signature unchanged — verified, no edit needed |
| P3 → P4 | LLMOutput or typed failure | one-way | engine assumes retry already happened inside backend (exactly-once retry ownership: P3) |
| P4 → P5 | RunResult (results + slots + drafts + worst-severity) | one-way | composition assumes suppression already applied (not-evaluated never renders) |
| P5 → P6 | persisted card payload | one-way | endpoint serves stored payload verbatim (consent record = served bytes) |
| P6 → P7 | REST contract + capability flag | one-way | bot assumes zone content fits Telegram message limits — flagged to P7 verification (freeze gate) |
| P6 → P4 | resolution updates to detection rows | one-way | resolution writes are append/update on existing rows, never re-run |
| P1+P2+P4+P6 → P8 | fixtures, contracts, routes | one-way | P8 tests via public surfaces only (no engine internals) |

## Step 6 — Dependency Order

1. **P1 ∥ P2** (no mutual dependency; both are contract producers)
2. **P3 ∥ P4** after P2 (P4 also after P1 for tables; P4's tests use P3's mock — build mock before engine wiring completes)
3. **P5** after P2 + P4 (can begin against P2's payload schema with fixture RunResults while P4 finishes)
4. **P6** after P1 + P4 + P5
5. **P7** after P6 (two client sub-tracks internally parallel)
6. **P8** integration tier last (unit tests live inside each piece as built)

No circular dependencies; P2 is the contract hub by design (matches A2/KI6).

## Step 7 — Self-Evaluation (full, 7 dimensions)

| Dimension | Verdict | Note |
|---|---|---|
| Independence | PASS | each question answerable through stated contracts; P5 buildable on fixtures |
| Completeness | PASS | all SV6 commitments land in a piece: A1→P1/P6, A2→P2/P5, A3→P1/P2, A4→P4/P6, A5→P1/P3/P4/P7, A6→P1/P6; OPEN knobs recorded in P1/P3 |
| Reassembly | PASS | acid walk: submission → P6 create → P4 run (P3 mock) → P5 card → P7 render → resolutions → approve → existing launch+fan-out; every catalog §2/§5/§6 obligation traced |
| Tractability | PASS | each piece ≈ 0.5–1 day focused |
| Interface clarity | PASS | assumptions column populated; two flagged items routed to verifications (Telegram size → P7; same-schema mock → P8) |
| Balance | PASS (tolerated skew) | P4 ≈ 1d vs P1 ≈ 0.5d — ≤2× spread |
| Confidence | HIGH | Step 2/3 agree; no boundary disputed |

**Determination-mechanism check:** runtime determinations all have owning pieces — backend selection (P1 config + P3 factory), green-channel/archetype routing (P4 matrix), CTA lock (P5), capability/off behavior (P6 exposure + P7 branch), hold gating (P1 list + P6 enforcement). No presupposed-but-unowned determination found.

**Verdict: 7/7 PASS — decomposition committed. The 8 pieces are the BOM's section skeleton.**
