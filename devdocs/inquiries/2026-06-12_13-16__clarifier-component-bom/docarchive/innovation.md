# Innovation — Clarifier Component BOM

## User Input

/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/_branch.md
(operating on sensemaking SV6 + decomposition P1–P8)

## Seed & Methodology Mode

**Seed (gap):** the clarifier's structural spec doesn't exist; SV6 committed the architecture (A1–A6), P1–P8 staked the pieces — what design content should fill them, and is anything structurally missing or wrong?

**Mode consideration:** (a) inherited mode: **Standard default** (branch says produce the BOM; no weighting signals). (b) Alternative: **Contrarian-rethink (Framer-weighted)**. (c) Under it, mechanisms would re-litigate A1–A6 — ground sensemaking already adjudicated with tested counters, and critique re-prosecutes next; the run would predictably duplicate. (d) **Decision: default** (4G+3F), with the Inherited Frame Audit still forcing explicit challenges to the central commitments (below).

**Production-task classification:** P2 (registry-as-canon framing), P6 (lifecycle REST framing), P8 (DoD evaluation criteria) are meta-decision pieces → piece-level Inversion mandatory. P1/P3/P4/P5/P7 are content-production within A1–A6.

## Phase 2 — Generate (7 mechanisms × 3)

### Lens Shifting (Framer)
- *Generic — multi-platform future lens:* with web + future mobile clients, the card payload must carry **zero client markup** — semantic marks only (`replacement`, `addition`, `chip`, kinds), each client maps to its own widgets. → **V-L1 platform-neutral payload vocabulary**.
- *Focused — demo lens:* the mock backend is the demo: it must produce convincing full-card behavior on the acid set, not stub strings. → **V-L2 mock-as-demo quality bar** (acid coverage mandatory in mock rules).
- *Contrarian — high-volume lens:* at volume, sync-in-request dies; the async seam must be PROVEN, not declared. → **V-L3 slow-backend simulation test** (inject 10s mock latency; assert thinking-state contract + no client timeout assumptions).

### Combination (Generator)
- *Generic:* registry + prompt-builder + mock rules → **V-C1 registry-driven triple**: one in-code canon mirror feeds engine routing, prompt rendering, AND mock behavior. Three consumers, one source — catalog drift becomes one-file drift.
- *Focused:* draft lifecycle + existing `services/audit.py` → **V-C2 transition auditing** (every status transition = audit row; reuses existing service verbatim).
- *Contrarian:* clarifier run + existing audience preview → **V-C3 server-side preview composition**: the engine already holds wizard context; compose the preview line INTO the card server-side; draft-flow clients stop calling `/tasks/audience-preview` themselves.

### Inversion (Framer)
- *Generic (system-level, audit-serving):* "clarifier is a backend component" → "clarifier is client-side; the bot calls the LLM directly." Depth-iterate: L1 "bot owns the call" violates bot-owns-zero-logic; L2 system-level: **the consent record's persistence requirement pins the clarifier server-side** — two clients + a card that must be stored as-shown leave no client-side variant. KILLED; fertile (names the structural pin for the BOM's decisions table).
- *Focused:* "draft created at confirm" → "draft created at wizard start; clarify incrementally per step." KILLED: violates single-pass canon + reintroduces the interrogation pattern the catalog inquiry killed. Preserved as production-era seed (pre-warming).
- *Contrarian (existence-axis per multi-axis check):* "new tables must exist" → **ZERO new tables**: tasks gain `status='draft'` + run/card JSON columns; drafts ARE pre-launch tasks. Tested seriously: browse already filters status; fan-out fires only on launch path. FAILS on task invariants: every existing query/contract ("a task is a launched thing" — my_tasks, audit targets, id space, capacity math) gains a draft guard; abandoned drafts pollute the task table; freeze semantics blur. KILLED on blast-radius grounds — flagged to Critique for independent re-prosecution (the most uncomfortable kill).

### Constraint Manipulation (Framer — both directions)
- *ADD (generic):* "entry codes may appear ONLY in the registry" → **V-CM1 drift-guard tests**: grep-style test asserting no code literals outside registry; catalog version pin asserted against `task_consumer_catalog.md` version note.
- *ADD (focused):* "card payload must render within Telegram's 4096-char message limit" → **V-CM2 server-side composition budget** (zone trimming rules + maximal-card fixture).
- *REMOVE (contrarian):* remove "drafts expire": **V-CM3 no TTL at MVP** — drafts persist; cleanup is a future ops script; resolves P1's open TTL knob at zero cost. (Also explored removing "one LLM call per revision" — non-removable: canon §2.5; MQ4 forbids re-opening.)

### Absence Recognition (Generator — patch + redesign, bidirectional)
- *Patch:* nothing guards LLM spend — **V-A1 run rate cap** (`CLARIFIER_RUNS_PER_USER_PER_HOUR`; 429 on excess; code executor, free). Also absent: hold-SLA re-ping (knob, deferred); ops metrics (log-derived at MVP, note only).
- *Patch (privacy):* detection rows copying submission text duplicates PII — **V-A2 log normalization**: rows reference the run FK; text lives once on the draft.
- *Redesign (what's missing):* a from-scratch design would include a **clarifier replay harness** — re-run logged submissions against a new registry/prompt version and diff results; the regression tool for canon changes. → **V-A3 replay hook** (dev script over detection log).
- *Redesign (already-present-in-different-form):* the project ALREADY HAS a code-only clarifier v0 — the bot's `summary_text(data, audience, warnings)` + preview + budget validator. The rollout should be framed as **payload replaces summary_text's inputs**, provable by **V-A4 off-flag parity test**: with backend=off, the draft flow's card renders content-equivalent to today's confirm summary. The single biggest rollout de-risk found this run.

### Domain Transfer (Generator — native source included)
- *Native (computing — payment-intent pattern, Stripe):* create intent → confirm → capture maps onto draft → resolve → approve. Import the missing piece: **V-D1 client idempotency key** on `POST /tasks/drafts` (dedupes double-taps/retries — Telegram users double-tap). Status-enum naming discipline comes along free.
- *Different field (publishing):* galley-proof framing — the persisted card payload IS the galley; approval signs the galley. Naming color for the BOM's approval section; no new structure (stet/diff already imported by the catalog).
- *Different field (code review / PR flow):* "conversations must resolve before merge" ≈ CTA lock (already committed); the transferable residue is **resolution persistence across revisions** (re-request-review pattern) — already a P6 criterion; transfer confirms, adds nothing new. Flagged honestly as convergent-confirmation, not novelty.

### Extrapolation (Generator)
- *Generic (catalog grows):* extension trigger will add entries post-launch → **V-E1 unknown-code tolerance**: log readers and clients ignore codes they don't know; registry additions need no migration (codes are strings on rows).
- *Focused (corpus accumulates):* the detection log becomes the eval corpus (routes 16/17) — V-A2's normalization + V-A3's replay are the prerequisites; convergence noted.
- *Contrarian (LLM cost→0, latency→sub-second):* inline-as-you-type clarification becomes plausible; the draft seam is unaffected (same engine, different invocation cadence). RESEARCH FRONTIER; no BOM change.

## Inherited Frame Audit

- **Seed central assumption:** "the clarifier is a backend draft-lifecycle component wrapped around the existing launch path" (SV6/A1). **Challenged?** YES — Inversion-generic (client-side clarifier; killed at system level, naming the persistence pin) and Inversion-contrarian (zero-new-tables; killed on task invariants, flagged to Critique). Audit satisfied for the seed.
- **P2 registry commitment** (framing-semantic): challenged via piece-level Inversion — "parse the catalog DOC at runtime instead of maintaining a code registry." KILLED: doc-parsing is untestable, fragile against prose edits, and inverts the canon/build relationship (§ the catalog is canon; the prompt/code are build artifacts). Registry survives strengthened.
- **P6 lifecycle commitment** (framing-semantic): challenged twice (zero-table inversion above; payment-intent transfer independently CONFIRMS the lifecycle shape from a different ground). Satisfied.
- **P8 DoD commitment** (evaluation-criterion): challenged via Inversion — "mock-only DoD is self-deception; demand a real-API gate." Partial survivor: real-API in CI killed (no key in CI; vendor coupling), but **V-T1 manual real-backend smoke checklist** (pre-"done" once a key exists) survives as an ADD.
- **Audit verdict:** no unchallenged load-bearing commitment remains; no override needed.

## Phase 3 — Test (5-test cycle on candidates)

| # | Candidate | Novel | Scrutiny | Fertile | Actionable | Mech-indep | Disposition → piece |
|---|---|---|---|---|---|---|---|
| T1 | platform-neutral payload vocabulary (V-L1) | ✓ (catalog §5.3 implied per-client markup) | strongest objection: over-abstraction for 2 clients — survives: semantic marks are CHEAPER than HTML-in-JSON | ✓ mobile later | ✓ | lens + extrapolation | **ACTIONABLE → P2** |
| T2 | registry-driven triple (V-C1) | ✓ | objection: registry becomes god-module — survives: it's data, not logic; consumers stay separate | ✓ (canon-coupling spine) | ✓ | combination + constraint-ADD + extrapolation (shared-input check: convergent content EXCEEDS the inherited P2 framing — drift guards and triple-sourcing are additive from different grounds; independence accepted) | **ACTIONABLE → P2/P3** |
| T3 | server-side preview composition (V-C3) | ✓ | objection: duplicates an endpoint clients already call — survives: removes a client roundtrip + preview becomes part of consent record | ✓ | ✓ | combination + card-zone spec | **ACTIONABLE → P5/P6** |
| T4 | slow-backend simulation test (V-L3) | ✓ | survives (cheap, mock-latency flag) | ✓ async era | ✓ | lens + payment-intent polling | **ACTIONABLE → P8 (+P7 thinking-state contract)** |
| T5 | drift-guard tests (V-CM1) | ✓ | survives | ✓ | ✓ | constraint + combination | **ACTIONABLE → P8** |
| T6 | composition budget / Telegram limit (V-CM2) | ✓ | objection: premature — survives: 4096 is a hard platform constant, not a tunable | ✓ | ✓ | constraint + P7 freeze-gate assumption | **ACTIONABLE → P5** |
| T7 | no-TTL-at-MVP (V-CM3) | ✓ resolves open knob | survives (cleanup deferrable; abandoned drafts are calibration data, not waste) | – | ✓ | constraint-REMOVE | **ACTIONABLE → P1** |
| T8 | run rate cap (V-A1) | ✓ | survives (first real token-abuse guard) | ✓ | ✓ | absence + economics lens | **ACTIONABLE → P1/P6** |
| T9 | log normalization / no text copies (V-A2) | ✓ | survives (PII + size) | ✓ eval corpus | ✓ | absence + extrapolation | **ACTIONABLE → P1** |
| T10 | off-flag parity test / summary_text continuity (V-A4) | ✓ | objection: byte-parity too strict — REFINED to content-equivalence (fields present, same semantics) | ✓ | ✓ | absence-redesign (already-present direction) | **ACTIONABLE → P7** |
| T11 | client idempotency key (V-D1) | ✓ | survives (double-tap is real on Telegram) | – | ✓ | domain transfer + Telegram UX | **ACTIONABLE → P6** |
| T12 | unknown-code tolerance (V-E1) | ✓ | survives | ✓ | ✓ | extrapolation + registry spine | **ACTIONABLE → P2/P8** |
| T13 | replay harness hook (V-A3) | ✓ | survives but exceeds MVP need | ✓✓ (routes 16/17 prerequisite) | partial | absence-redesign | **DEFERRED — revival: first registry/prompt change after ≥50 real runs** |
| T14 | hold-SLA re-ping | ✓ | thin | – | ✓ | absence-patch only | **DEFERRED — revival: operator practice data** |
| T15 | manual real-backend smoke checklist | ✓ | survives | – | ✓ | inversion at P8 | **ACTIONABLE (small) → P8** |
| K1 | client-side clarifier | killed at system level — names the persistence pin (record in decisions table) | | | | | seed |
| K2 | zero-new-tables (draft-status-on-task) | killed on task invariants + blast radius — **flagged to Critique for independent re-prosecution** | | | | | seed |
| K3 | incremental per-step clarification | killed by single-pass canon — production-era seed | | | | | seed |

**RE-TEST TRIGGER scan:** T3 (server-side preview) recasts a P7 assumption ("clients call preview as today") — P7's criteria re-checked: draft-flow clients render the preview zone instead of calling the endpoint; legacy wizard (flag off) keeps calling it. No contradiction remains. T10's refinement (content-equivalence) updates V-A4's wording only.

**Artifact-grounding (conditional 6th test):** claims checked against code — `summary_text(data, audience, warnings)` exists (`src/bot/flows/launch.py:130`) ✓; `/tasks/audience-preview` exists ✓; browse filters by status param ✓ (K2's kill ground verified); audit service exists ✓.

## Assembly Check

- **Canon-coupling spine (emergent):** T2 + T5 + T12 compose into one subsystem — registry feeds engine/prompt/mock; drift guards pin registry↔catalog; tolerance rules absorb future entries. The BOM should present these as ONE "canon coupling" block inside P2, not three scattered items. This materializes route 15 (canon coupling) in code form.
- **Rollout-safety cluster (emergent):** T10 (parity) + T4 (slow-sim) + T6 (size budget) + T11 (idempotency) form the "ship without breaking launch" checklist — the BOM should gate P7's DoD on all four, since they jointly guarantee the flag can turn on without UX regression.
- **Axis coverage:** persistence (challenged via K2) · contracts (T1/T2/T12) · composition (T3/T6) · rollout/ops (T4/T10/T11/T15) · economics (T8) · privacy (T9) — no axis without a variant.
- **Per-piece trace:** P1: T7/T8/T9 · P2: T1/T2/T12 (+registry inversion) · P3: T2/V-L2 · P4: T4-degrade + killed partial-rerun · P5: T3/T6 · P6: T3/T8/T11 (+K1/K2 challenges) · P7: T4/T6/T10 · P8: T4/T5/T12/T15 (+DoD inversion). All pieces show mechanism trace.

## Telemetry

- Generators: 4/4 · Framers: 3/3
- Convergence: YES — 3+ mechanisms converge on the registry/canon-coupling spine; 2 independent grounds confirm the draft-lifecycle shape (payment-intent transfer; persistence-pin inversion)
- Survivors tested: 15/15 (+3 kills documented with grounds, 1 frontier)
- Piece classification: P2/P6/P8 meta-decision (Inversion compliance: **satisfied** ×3); P1/P3/P4/P5/P7 content-production
- Per-piece mechanism log: see Assembly per-piece trace
- Failure modes: none observed (uncomfortable kill K2 explicitly re-flagged to Critique against survival bias)
- **Overall: PROCEED**
