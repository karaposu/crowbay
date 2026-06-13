# filepath: devdocs/scoped/be/matching/list.md

# Matching + Notifications — Concept List

> **Status: IMPLEMENTED** (2026-06-12) — all 10 concepts, 83 tests green across the suite,
> ruff clean. Decisions taken (all config-overridable): raw-statement locations are
> **advisory** with a warning on the bot's confirmation card (C6 option b); notify cap 50
> newest-first (`MATCH_NOTIFY_CAP`); privacy floor 10 (`AUDIENCE_PRIVACY_FLOOR`); age from
> `birth_date` translated to lexicographic ISO date bounds; confidence ≥ 0.8 with NULL
> counting as confident (`MATCH_CONFIDENCE_MIN`). Canonical attribute names live in
> `services/attributes.py` — the verification component MUST import them from there.
> Implementation notes: the evaluator has two modes that share one parser — SQL predicate
> (audience/fan-out) and Python snapshot eval (gate/feed, one DB read per user); tests
> assert the modes agree on every semantic case. The feed scans up to `BROWSE_SCAN_LIMIT`
> open tasks and paginates the eligible subset (per-task JSON filters can't be one WHERE
> clause) — revisit when open tasks exceed the scan limit.

The concepts that make up the "Matching + notifications" row (todo.md: Easy,
1–2 days, SQL WHERE clauses). Matching turns persisted task filters into
"who sees / who may jump"; notifications close the loop ("the crowd jumps on
it" only happens if the crowd hears about it). Per devdocs/filter_design.md:
binary matching, verified attributes only, absence-is-failure.

## Concepts

### 1. Filter Expression Evaluator
The core. Compiles a task's persisted `filters` JSON into a SQL predicate
over `verification_data` (one EXISTS subquery per filter field: `field_name`
matches, `is_current = true`, confidence ≥ threshold). AND across fields, OR
within location lists, exceptions subtract from their parent scope, missing
attribute = no match. Built as a reusable object with two outputs — a
per-user boolean and a user-set query — because four consumers need it:
eligibility checks, the task feed, audience counts, and (later) differential
pay rate groups.

### 2. Jump Eligibility Gate
**Closes a real gap that exists today**: `POST /tasks/{id}/jump` currently
lets anyone jump on any task regardless of filters. The gate runs the
evaluator for (task, user) inside `jump_on_task` and rejects with a reason
listing the unmet requirements. A task with no filters keeps matching
everyone.

### 3. Filtered Task Feed
Browse today returns all open tasks. With matching, the Jumper feed shows
only tasks whose filters the Jumper passes (exclusive mode). The old docs'
"inclusive mode" (show locked tasks with their unlock requirements as a
verification incentive) is explicitly **later** — it needs per-filter
explain output, not just a boolean.

### 4. Audience Preview
Launcher-facing count before funding: "your filters match N verified
Jumpers." Same evaluator, count output, exposed as a preview endpoint the
bot calls during the launch flow (after the filters step, before the
confirmation card). Apply a privacy floor — below a small N, show "fewer
than 10" rather than exact counts that can identify individuals
(filter_design open question 5).

### 5. Region Taxonomy
Static region → countries mapping (EMEA, LATAM, APAC, ...) as a config
asset (yaml) + seed, consumed by the evaluator to expand `regions` entries.
Without it, only country/city entries evaluate. Someone must own the
definition — we ship an explicit list rather than implying one.

### 6. Location Raw-Statement Parser  *(decision point)*
The bot stores location filters as `raw_statement` only — it does not
geocode. Something must turn "EMEA but not Russia, plus Istanbul" into the
structured form the evaluator reads. Options: (a) LLM parse at launch time
with Launcher confirmation in the bot flow, (b) MVP punt — treat
raw-only location filters as **advisory** (warn the Launcher they won't
constrain matching until parsed). (b) keeps this row at 1–2 days; (a) adds
the first LLM dependency to the backend. The evaluator must behave sanely
either way: a location filter with raw_statement and no structured entries
must not silently exclude everyone.

### 7. Match-on-Launch Fan-out
When a task launches, run the audience query and notify matched Jumpers.
Cap per launch (e.g. first 50, recency-ordered) so a broad-filter task
doesn't message the whole platform; record who was notified. Synchronous
in-request is fine at MVP scale; the seam should allow moving it to a
background job without API changes.

### 8. Telegram Notifier
The delivery mechanism the bot BOM explicitly left out. The **API side**
sends messages directly via the Bot API (httpx + BOT_TOKEN, sendMessage) —
the bot process stays a pure client and is not involved. Handles per-second
rate limiting, swallows "user blocked the bot" gracefully, and is a seam:
console backend for dev/tests (same pattern as emailer/sms), real Telegram
backend in prod.

### 9. Notification Ledger + Mute
A `notifications` table (user, type, payload, status, sent_at) giving
idempotency (never notify twice for the same event), an audit trail, and a
user-level mute flag surfaced later as a bot command. Event types at MVP:
`task.matched` (Jumper), `jump.approved` / `jump.rejected` (Jumper),
`jump.pending` (Launcher), `task.full` (Launcher).

### 10. Dev Attribute Seeding
Matching reads verified attributes, and the verification pipeline doesn't
exist yet — so in a fresh dev environment, every filtered task matches
nobody (correctly!). A seed script granting test users verified
`location_country` / `birth_date` / `gender` rows makes the whole component
exercisable end to end before the verification component lands.

## Sequencing & dependencies

- 1 → 2/3/4 (everything consumes the evaluator); 5 feeds 1; 7 → 8 → 9.
- 10 is first in practice — without it nothing is testable.
- Depends on: backbone (done), filters persisted verbatim (done),
  `verification_data` schema (done, empty until the verification component).
- Canonical attribute names must be agreed now (`location_country`,
  `location_city`, `birth_date`, `gender`) — the verification component will
  write what matching reads; mismatched field names would fail silently.

## Decisions to make before the BOM

1. Raw-statement locations: advisory-with-warning (MVP) vs LLM-parse-at-launch.
2. Notify cap per launch and ordering (first-N by recency vs random sample).
3. Privacy floor value for audience preview (suggest: exact counts only ≥ 10).
4. Age evaluation source: `birth_date` computed against today (preferred —
   ages stay current) vs stored `age` snapshots.
5. Confidence threshold for attributes to count (suggest: ≥ 0.8, config).
