# Critique — Clarifier Component BOM

## User Input

/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/_branch.md — candidates from `innovation.md` (T1–T15, K1–K3, two emergent assemblies, plus the BOM assembly itself) against `sensemaking.md` SV6 and the branch Goal.

## Phase 0 — Dimensions (extracted; purpose-fitness weighted)

| # | Dimension | Weight | Extracted from | Success criterion |
|---|---|---|---|---|
| D1 | Canon faithfulness (catalog v1.2 + meta-def consumed, never re-opened) | CRITICAL .20 | C1/C10, MQ4 | no candidate alters detection semantics, severities, card consent rules — **external anchor: `devdocs/task_consumer_catalog.md`** |
| D2 | House-pattern coherence | CRITICAL .175 | C5/C6 | plain-function services, thin routers, pluggable backend, Alembic, ledger style — **external anchors: `src/config.py`, `services/sms.py`, `db/models/notification.py`, backbone BOM §0** |
| D3 | Launch-flow safety (blast radius; project-specific risk axis) | HIGH .15 | C4/C8/C9 | existing `POST /tasks`, bot, fe keep working; flag-off = today exactly; fan-out fires only post-approval — **external anchors: `routers/tasks.py`, `services/tasks.py`, `flows/launch.py`, `fe/app.js`** |
| D4 | Work-order implementability (the BOM's purpose) | HIGH .125 | WHY: enable-next-build-session | ordered sections, checkable criteria, each ~a focused pass |
| D5 | MVP parsimony | MED .10 | Resource anchor, A4/A5 | no premature infra; mock-first; ~4–5 days holds |
| D6 | Consent/audit integrity | MED .10 | catalog §5.4, A1/A2 | card-as-shown + resolutions persist; approval = consensus snapshot |
| D7 | Cost/abuse robustness | MED .075 | Risk perspective | token spend bounded; degradation visible |
| D8 | Calibration-data integrity (project-specific risk axis) | MED .075 | SP3, §2.6 | versioned rows; `not-evaluated` honesty; no PII duplication |

**Frame-premise test** (candidate-space rests on inherited commitments): (i) *catalog v1.2 semantics are right* — what-if-wrong: the BOM builds a faithful machine for wrong rules; independent mitigation exists (registry+drift-guard make canon changes one-file; detection log feeds the feedback register) — inheritance NAMED, accepted. (ii) *draft-resource architecture (A1)* — prosecuted independently below via the K2 re-prosecution with fresh external anchors. (iii) *the wizard remains the collection mechanism* — standing kill from the catalog inquiry (K2 there); unchanged here. Premises named; none invisible.

## Phase 1 — Landscape

- **Viable:** cheap tests/knobs raising D3/D6/D7/D8 (most of the survivor set); contract-level work raising D1/D2.
- **Dead:** anything re-opening canon (D1); client-side business logic (D2/D6); silent degradation (D7); schema-less log rows (D8).
- **Boundary:** storage-shape choices (K2's region — viability depends on D3 blast radius); DoD strictness (mock-only vs real-API).
- **Unexplored (deliberate):** prompt wording, vendor choice, eval corpus content — excluded by MQ4/Layer Commitment.

## Phase 2/3 — Adversarial Evaluation + Verdicts

**K2 re-prosecution — zero-new-tables (drafts as `status='draft'` tasks)** *(innovation's uncomfortable kill, re-tried with anchors)*
- Defense of K2 (strongest): one less model; `jump_on_task` ALREADY guards (`task.status != OPEN → 409` — verified verbatim); drafts appearing in "my tasks" could be a feature.
- Prosecution (external-anchor sub-axis): `browse_tasks` with `status_filter=None` applies **no status filter** (`if status_filter is not None: q = q.filter(...)`) — both the internal path and the eligible-feed scan would include drafts today; `my_tasks` has **no status filter** — drafts would surface in the bot's "Your launched tasks" labeled as launched. Making K2 safe means auditing/patching every Task read path now and every future one forever (escrow, verification, disputes all bind to tasks) — the invariant "a Task row is a launched thing" is load-bearing across the codebase.
- Collision: defense's guard exists in exactly ONE consumer; two other consumers verified unguarded. **KILL CONFIRMED** (D3 critical). Seed preserved: the draft table may merge INTO tasks at a future major migration once consumers are status-aware by design.

**T1 — platform-neutral payload vocabulary** — Prosecution: abstraction tax for 2 clients. Defense: semantic marks are cheaper than HTML-in-JSON; catalog §5.3 already notes per-client ergonomics. **SURVIVE** (D1/D2).

**T2 — registry-driven triple (canon-as-code spine)**
- Prosecution (strongest): the registry is a hand-maintained COPY of the catalog — dual-maintenance is the very drift it claims to prevent, one layer down.
- Defense: the executable form must exist somewhere; alternatives are worse (runtime doc-parsing killed in innovation; scattered literals = N copies instead of 1); T5's version-pin test turns silent drift into CI failure.
- Collision: defense holds CONDITIONAL on T5 shipping in the same section. **SURVIVE** with binding caveat: registry and drift-guard are one unit, never split across sections.

**T3 — server-side preview composition** — Prosecution: duplicates an endpoint clients already call; adds a query to draft creation. Defense: the preview line becomes part of the persisted consent record (D6) — a card without its preview is not card-as-shown; endpoint stays for the legacy flow. **SURVIVE.**

**T4 — slow-backend simulation test** — survives trivially (mock latency flag); D3/D5. **SURVIVE.**

**T5 — drift-guard tests** — prosecution: grep-tests are brittle theater. Defense: pin test (registry version == catalog version note) is exact, not grep; code-literal scan is advisory. **SURVIVE** (refine wording: version-pin = hard, literal-scan = advisory).

**T6 — composition budget (Telegram 4096)** — hard platform constant; server-side trimming protects D6 (truncated card ≠ card-as-shown — trimming RULES, not client truncation). **SURVIVE.**

**T7 — no-TTL-at-MVP** — Prosecution: unbounded PII retention (drafts hold submission text; X4's own concern), GDPR-ish exposure; "abandoned drafts are calibration data" justifies hoarding. Collision: prosecution lands a real hit. **REFINE →** ship the knob now, default off: `CLARIFIER_DRAFT_TTL_DAYS: int | None = None` + cleanup function (callable as script); enabling is an ops decision. Refinement absorbed into P1.

**T8 — run rate cap** — first real token-abuse guard; code executor; D7 core. **SURVIVE.**

**T9 — log normalization (no text copies)** — supports D8 + privacy; join cost trivial at MVP. **SURVIVE.**

**T10 — off-flag parity test** — Prosecution: "content-equivalence" is unverifiable hand-waving. Collision: hit lands. **REFINE →** enumerate the parity fields: budget line, slots×pay line, audience line (incl. privacy-floor wording), deadline, mode, raw-statement warning. Parity test asserts field presence + semantic equality, not bytes. Absorbed into P7.

**T11 — client idempotency key on draft create** — Telegram double-taps are real; header + unique constraint is cheap (ledger dedupe_key precedent — D2 anchor). **SURVIVE.**

**T12 — unknown-code tolerance** — forward-compat for the extension trigger; one guard clause. **SURVIVE.**

**T15 — manual real-backend smoke checklist** — keeps CI keyless while closing the "mock-only self-deception" hole at the right cost. **SURVIVE.**

**T13 — replay harness / T14 — hold-SLA re-ping** — screened: both blocked on data that doesn't exist (real runs; operator practice). **DEFER** with innovation's revival gates unchanged.

**ASSEMBLY — the BOM document itself (§0 decisions + 9 sections + survivors folded in)**
- Prosecution (user-perspective, strongest): the ask was a BOM to build from; 15 survivors risk bloating it into an architecture treatise — past BOMs succeeded BECAUSE they were checkbox work-orders (~120 lines).
- Defense: the survivors are mostly tests and config knobs (cheap line-items, not sections); the decisions table absorbs the architecture; the precedent pattern (backbone §0 + checkbox sections) is exactly what sensemaking committed.
- Collision: prosecution lands a PRESENTATION requirement, not a content hit: survivors fold INTO their owning sections as checkbox items; the decisions table stays ≤ a screen; no separate "innovations" section. Extent note: articulation 4 (BOM-then-implement) is the user's call at finding time — the BOM must stand alone either way (D4). **SURVIVE with the presentation requirement. Ranked #1.**

**Specification-gap probe:** who invokes hold-resolution auth (operator list — specified, P1/P6); how clients detect the flag (capability exposure — specified, P6); how parity is judged (T10 refinement — now specified). No presupposed-but-unspecified determinations remain.

## Phase 3.5 — Assembly Check

T7-refined + T8 + T9 compose into a **data-hygiene block** inside P1 (retention knob, rate cap, normalized rows) — folded as P1 line-items, no new candidate. The rollout-safety cluster (T4+T6+T10+T11) becomes P7/P8's DoD gate, per innovation's assembly — confirmed against D3.

## Phase 4 — Coverage + Convergence

- **Accumulator:** 17 evaluations (15 survivors-or-refines, K2 re-kill, BOM assembly); kills: K1 (persistence pin named in decisions table), K2 (anchored), K3 (production-era seed); refinements: T7, T10 (both absorbed); mechanism-independence: **validated** (external anchors quoted verbatim this pass: `browse_tasks` filter conditional, `jump_on_task` guard, `my_tasks` query; cited: config backend selectors, notification dedupe_key, catalog §5.3/§5.4/§2.6).
- **Coverage:** all 8 dimensions discriminated (every candidate faced D1+D2; D3 killed K2; D6/D7/D8 each shaped at least one verdict). Unexplored regions are MQ4-deliberate.
- **Convergence:** landscape STABLE; clean SURVIVEs exist.
- **Signal: TERMINATE.** Ranked: 1) BOM assembly (presentation-constrained) · 2) T2+T5 canon spine (one unit) · 3) T10-refined parity test · 4) rollout cluster T4/T6/T11 · 5) T8 rate cap · 6) T3 server-side preview · 7) T9 log normalization · 8) T1 neutral vocabulary · 9) T7-refined TTL knob · 10) T12 tolerance · 11) T15 smoke checklist. Deferred: T13, T14.

## Convergence Telemetry

- Dimension coverage: 8/8 applied; project-specific risk axes present (D3, D8)
- Adversarial strength: STRONG — K2's re-prosecution flipped from argued-kill to anchored-kill; T7 and T10 prosecutions both forced refinements; the assembly prosecution forced a presentation constraint
- Landscape stability: STABLE
- Clean SURVIVE exists: YES (assembly, post-constraint)
- Failure modes observed: none (defense mandatory throughout; external anchors quoted verbatim; no quarantine)
- **Overall: PROCEED**
