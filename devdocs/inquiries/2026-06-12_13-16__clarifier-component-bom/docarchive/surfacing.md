# Surfacing — Clarifier Component BOM

## User Input

/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_13-16__clarifier-component-bom/_branch.md

## Mode

- **Territory-type-mode:** artifact (concrete pre-existing items: canon docs, BOM precedents, `src/` codebase, two clients)
- **Entry point:** signal-first (purpose from `_branch.md` Goal: a structural BOM for the clarifier under `devdocs/scoped/be/clarifier/`, consuming catalog v1.2 + meta-definition as canon)
- **Territory specification:** explicit-bounded — 8 regions: R1 canon pair · R2 BOM precedents · R3 `src/` backbone surfaces · R4 bot launch flow · R5 fe web client · R6 matching/output-contract consumers · R7 ledger/log precedent · R8 config/backend-pattern
- **Boundary-discovery:** skipped (explicit-bounded)
- **Prior-workspace:** present (same session; catalog v1.2 + meta-definition + prior findings warm) — runner-supplied

## Traversal Trace

| # | Region | Item identifier(s) | Verdict | Conf | Recency `{fs}` | Note |
|---|---|---|---|---|---|---|
| 1 | R1 | `devdocs/task_consumer_catalog.md` §2.4 (LLM output shape — "concrete JSON schema… are the clarifier component BOM's deliverable"), §2.5 (single-pass, idempotency, suppression), §2.6 (log row shape), §5 (card zones, launch-CTA lock, revision loop), §6 (output contract/normalizer), §4 constants table | **core** | HIGH | 2026-06-12T13:11:23Z | warm; the canon this BOM operates — §2.4 NAMES this BOM as owner of wire schema + prompt assembly + invocation plumbing |
| 2 | R1 | `devdocs/task_meta_definition.md` implementation note (`undefined_requirements(task) -> list[str]`; "gates return unmet lists" mental model) | **core** | HIGH | 2026-06-12T11:16:19Z | warm; the check-shape convention the clarifier service should rhyme with |
| 3 | R2 | `devdocs/scoped/be/matching/list.md` — structure: status header updated at implementation; concept sections; "Decisions to make before the BOM"; sequencing/dependencies; config-overridable decisions recorded in header | **core** | HIGH | 2026-06-12T10:05:16Z | the pattern route-guidance says to mirror; read in full |
| 4 | R2 | `devdocs/scoped/be/backbone/concept_bom.md` — structure: §0 decisions table ("veto before starting"), checkbox sections w/ effort, in/out-scope block, deviations recorded in status header | **core** | HIGH | 2026-06-12T08:09:47Z | the decisions-table discipline; skimmed header + §0 + §1 + heading map |
| 5 | R2 | `devdocs/scoped/tg_bot_bom.md` | sub | MED | 2026-06-12T08:39:18Z | third precedent; not re-read (pattern already established by #3/#4) |
| 6 | R8 | `src/config.py` Settings — grouped sections per component (email/SMS/matching), backend-selector convention (`EMAIL_BACKEND`/`SMS_BACKEND`/`NOTIFY_BACKEND` = console/mock vs real), fail-fast SECRET_KEY, config-overridable knobs (`MATCH_*`, `AUDIENCE_PRIVACY_FLOOR`) | **core** | HIGH | 2026-06-12T09:43:20Z | the clarifier needs the same: `CLARIFIER_BACKEND` mock/real + knob block |
| 7 | R3 | `src/routers/tasks.py` — `POST /tasks` = launch (auth'd, audit.record, `notifications.fan_out_task_matched` inline); `POST /tasks/audience-preview` exists | **core** | HIGH | 2026-06-12T10:03:34Z | the invocation seam: today clients POST /tasks directly from confirm; no draft/clarify step exists |
| 8 | R3 | `src/services/tasks.py` — plain-function service (`launch_task(db, owner, data)`), `jump_on_task`, approve/reject/forfeit; no task-edit function | **core** | HIGH | 2026-06-12T09:54:04Z | no edit endpoint ⇒ binding-pair freeze is currently trivially satisfied; clarifier adds the only pre-launch mutation loop |
| 9 | R3 | `src/schemas/task.py` `TaskCreate` — desc ≤5000, budget/you_earn/num_jumpers + `_budget_covers_payouts` validator, filters, deadlines, `accept_jumpers_manually` | **core** | HIGH | 2026-06-12T09:55:11Z | the code-executor checks already live here (catalog executor=code claims); the clarifier's normalized slots have NO column home yet |
| 10 | R3 | `src/db/models/task.py` Task model | sub | MED | 2026-06-12T07:49:13Z | not fully read; columns mirror TaskCreate per session knowledge — slot-storage decision will need it at implementation |
| 11 | R4 | `src/bot/flows/launch.py` — FSM states incl. `confirm`; `build_payload`, `summary_text(data, audience, warnings)` already composes preview + warnings into the confirm card; `🚀 Launch it` callback POSTs /tasks | **core** | HIGH | 2026-06-12T10:04:39Z | the exact seam the marked-up card enriches/replaces (catalog kept wizard: "consumer enriches the existing confirm step") |
| 12 | R5 | `fe/app.js` — launch wizard mirrors bot (`step:"confirm"`, audience-preview call, `confirmLaunch()` POSTs /tasks) | **core** | HIGH | 2026-06-12T10:21:38Z | second client; same seam; chips = buttons per catalog §5.3 web note |
| 13 | R6 | `src/services/matching.py` (`unmet_requirements` shape, evaluator), `src/services/notifications.py` (`fan_out_task_matched` on launch) | **core** | HIGH | 2026-06-12T10:04:39Z / 10:13:16Z | downstream consumers of approval; fan-out must fire AFTER clarifier approval, not before |
| 14 | R7 | `src/db/models/notification.py` — ledger precedent: dedupe_key unique, status enum string, JSON payload, composite index | **core** | HIGH | 2026-06-12T10:13:14Z | the detection-log table should follow this house style |
| 15 | R8 | `src/services/sms.py` + `emailer.py` + `notifier.py` backend pattern (console/mock class + real class, selected by Settings string) | **core** | HIGH | 2026-06-12T09:32:07Z | the LLM backend abstraction precedent: `MockClarifierBackend` (deterministic, test-facing) vs real-API backend |
| 16 | R3 | `src/migrations/` (alembic, per backbone decision "Alembic from day one") | sub | HIGH | — (dir) | clarifier tables arrive by migration |
| 17 | R1 | catalog §8 open knobs (ToS posture, thresholds, extension trigger) + §5.3 freeze gate ("provisional until prototyped in both clients") | **core** | HIGH | 2026-06-12T13:11:23Z | BOM must carry these as config/TODO hooks without resolving them (MQ4) |
| 18 | R6 | `devdocs/filter_design.md` + matching list.md C6 — raw-statement location decision: "advisory with warning" standing; catalog §6 hands the structured-location slot adoption to matching's standing decision | sub | HIGH | 2026-06-12T07:32:28Z | the BOM must name the handover seam, not flip the decision |
| 19 | R8 | `PROJECT.md` Open Decisions (ToS posture) | side | HIGH | 2026-06-12T07:30:15Z | boundary item (MQ4: not this BOM's call) |
| 20 | R3 | `src/routers/` module list (auth/users/tasks/phone/health) + `schemas/` + `services/` naming conventions | sub | HIGH | — (dir) | placement candidates: `routers/clarifier.py` vs extend `tasks.py`; `services/clarifier.py`; `schemas/clarifier.py` |
| 21 | R4/R5 | bot `texts.py`, `keyboards.py`; fe chip-rendering | sub | MED | — | card rendering homes per client; not read deeper (implementation grain) |
| 22 | R1 | catalog §7 acid cases + §4 case seeds | sub | HIGH | 2026-06-12T13:11:23Z | the BOM's test-plan section seeds from these (hooks only — eval corpus is route 16, excluded) |

## State Summary

- **Territory echo:** canon pair + BOM precedents + `src/` integration surfaces + bot/fe clients + config/backend patterns, bounded per `_branch.md`.
- **Purpose echo:** surface everything a structural BOM needs: placement, invocation seam, data model homes, wire-schema obligations, backend abstraction precedent, client integration points, log-table house style, decision-table content.
- **Coverage map:** R1 confirmed (warm + re-cited) · R2 confirmed · R3 confirmed at BOM grain (model columns scanned-but-shallow) · R4 confirmed · R5 confirmed · R6 confirmed · R7 confirmed · R8 confirmed.
- **Confirmed-absent:** any existing clarifier/draft/LLM code in `src/` — none exists (no `clarifier` module, no draft state, no task-edit endpoint, no LLM dependency anywhere in backend). The component is greenfield; the BOM owes the first LLM dependency decision.
- **Concept-names:** `invocation seam` (#7/11/12 — clients POST /tasks from confirm; provenance tr-7) · `draft-vs-direct launch` (tr-7: does the clarifier interpose a draft resource or decorate POST /tasks?) · `backend-selector convention` (tr-6/15) · `slot-storage home` (tr-9/10: normalized slots have no column yet) · `fan-out-after-approval` (tr-13) · `ledger house style` (tr-14) · `unmet-list shape` (tr-2) · `handover seam` (tr-18, location slot → matching).
- **Recency distribution:** all items 2026-06-12 (same-day active repo); no-mtime: 4 (directory-level items); total: 22.
- **Frontier flags:** (1) `src/db/models/task.py` full column list + `Jump` states — re-read at implementation, not blocking BOM grain; (2) bot/fe card rendering ergonomics — catalog §5.3 freeze gate already owns this; (3) LLM vendor/API option space (Anthropic/OpenAI/local) — deliberately NOT surfaced as items (possibility-space for Innovation, not artifact territory).
- **Workspace-populated:** `{populated: true, populated-at: 2026-06-12T13:22Z, extent: 8/8 regions at BOM grain}`

## Telemetry

- Mode: artifact · signal-first · sub-phase: not fired
- Cycles: 3 (precedents+canon → src seams → clients/ledger/config) · items: 22 (core 14, sub 6, side 1, umbrella 0... recount: core 14, sub 7, side 1 = 22)
- items_with_mtime: 18 · items_without_mtime: 4
- Convergence: territory exhausted at BOM grain; uncertain items included (umbrella unnecessary — all confidently tagged); rejections only high-confidence (e.g. payments/escrow region not traversed: out of MQ4 bounds)
- Workspace-overload: not fired (targeted reads; ~300 lines total new content)
- Failure modes checked: Missed-relevance, Surfaced-irrelevance, Over-coverage, Territory-mis-binding, Workspace-overload, Artifact-under-spec, Desync, Recency-Equates-Idleness, Recency-Bias-Filter — none fired
- **Self-assessment: PROCEED**
