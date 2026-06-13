# filepath: devdocs/scoped/tg_bot_bom.md

# Telegram Bot BOM — Command Flows

> **Status: IMPLEMENTED** (2026-06-12), except the live phone-in-hand DoD which needs a
> @BotFather token (see appendix checklist). 38 tests green across backbone+bot, ruff clean.
> The bot runs as `make bot` beside `make run`; it fails fast with a clear message when
> BOT_TOKEN or BOT_BRIDGE_SECRET is missing.
> Deviations: (1) bridge accounts also needed `users.email` nullable, not just password_hash —
> migrated; password login for password-less accounts returns the same generic 401 as any bad
> login (anything more specific enumerates accounts, contra this BOM's "uses Telegram sign-in"
> message idea). (2) Browse is a one-card-per-page pager (edit-in-place) rather than a 5-task
> list — cleaner on mobile. (3) Location filter is stored as raw_statement only; the bot does
> not geocode (parsing is the matching component's job per filter_design.md).

Bill of materials for the Telegram bot: Crowdjump's primary user interface, a
command-based client of the backbone REST API. Estimated 4–6 days solo, plus
1–2 days for the file-size catch (staged below); effort noted per section.

**In scope**: bot scaffolding, account bridging to the backbone, the command/flow
surface (launch, browse, jump, manage, profile), guided FSM conversations with
inline keyboards, API client, error UX, the screen-recording upload *path*.
**Out of scope** (separate BOMs): video processing/verification logic, matching
fan-out and push notifications (the "Matching + notifications" row), payments UX
beyond what the API exposes, admin review tooling.

---

## 0. Decisions encoded here (veto before starting)

| Decision | Choice | Rationale |
|---|---|---|
| Library | aiogram 3.x | async, built-in FSM for multi-step flows, inline-keyboard ergonomics; the de-facto standard for this bot style |
| Bot ↔ backend | separate process, pure HTTP client of the API (httpx) | PROJECT.md: "the bot is a client of the API." Keeps the API honest — the bot uses only what any client could |
| Transport | long polling for MVP | no public URL/TLS needed; webhook is a prod upgrade, not an MVP need |
| Account model | Telegram-native: `POST /auth/telegram` bridge endpoint (backbone extension) | users must not type email+password into a chat; the bot authenticates users by `telegram_id` via a bot↔API shared secret |
| Token handling | bot keeps access tokens in memory only; on 401 it re-calls `/auth/telegram` | the bridge can re-mint anytime, so the bot needs no persistent token store and no refresh-token logic |
| FSM state storage | aiogram MemoryStorage for MVP | a restart loses in-progress conversations — acceptable at MVP scale; Redis storage is a drop-in later |
| Chat scope | private chats only | groups/channels rejected with a polite message; group UX is a later product question |
| Code location | `src/bot/` in the same repo/venv, own entrypoint (`make bot`) | shares config.py conventions; deploys as a second process beside the API |
| Screen recordings | staged (see section 5): size-guard now, self-hosted Bot API server later | the 20MB download cap is real; the upgrade path must not change the UX |

## 1. Scaffolding & account bridge (~1 day)

- [ ] `src/bot/` layout:
  ```
  src/bot/
    main.py          # dispatcher, polling startup, router mounting
    api_client.py    # httpx wrapper for every backbone call + auth/retry
    keyboards.py     # inline keyboard builders
    texts.py         # all user-facing strings in one place (future i18n)
    flows/           # one module per conversation (launch.py, browse.py, ...)
    middleware.py    # auth injection, private-chat-only, error boundary
  ```
- [ ] Config additions to `Settings`: `BOT_TOKEN`, `API_BASE_URL` (default `http://localhost:8000`), `BOT_BRIDGE_SECRET`; `.env.example` updated
- [ ] **Backbone extension — `POST /auth/telegram`** (see section 6): bot sends `{telegram_id, telegram_handle}` + `X-Bridge-Secret` header; API creates-or-fetches the user and returns a token pair
- [ ] `api_client.py`: typed methods (`launch_task`, `browse`, `jump`, ...), auto re-auth on 401, API `detail` strings surfaced to the error boundary
- [ ] Middleware: resolve telegram user → backbone token per update; reject non-private chats; catch-all error boundary that apologizes instead of going silent
- [ ] `make bot` target; runbook note: two processes (`make run` + `make bot`)

## 2. Entry, menu, profile (~0.5 day)

- [ ] `/start` — bridges the account on first contact, shows the main menu (inline keyboard): Launch a task · Browse tasks · My tasks · My jumps · Profile · Help
- [ ] `/help` — command list + what Crowdjump is in two sentences
- [ ] `/cancel` — **escapes any flow from any step**; every flow message also carries a Cancel button (the old concept doc's "error recovery" rule — non-negotiable UX)
- [ ] `/profile` — renders `/users/me`: email-verified flag, verification summary, placeholder trust score; "Start verification" button stubbed until the verification component lands

## 3. The launch flow — FSM (~1.5–2 days)

The heart of the bot. Guided steps, each validated, each cancellable, with a
progress indicator ("step 3 of 6"):

- [ ] Step 1: task description (free text, length-validated)
- [ ] Step 2: budget + per-Jumper pay + number of Jumpers (validate against the API's budget-covers-payouts rule *before* submitting, so users fix it in-flow)
- [ ] Step 3: filters, quick-pick style per filter_design.md — location (type a country/city, or Skip), age range (preset buttons: 18–25 / 25–35 / any / custom), gender (buttons) — each skippable; assembled into the `filters` JSON
- [ ] Step 4: deadlines (optional, parse a few friendly formats; Skip button)
- [ ] Step 5: manual Jumper approval toggle (`accept_jumpers_manually`)
- [ ] Step 6: **confirmation card** — full summary rendered back; Confirm / Edit / Cancel. Only Confirm calls `POST /tasks`
- [ ] Success message with the task card + what happens next

## 4. Browse, jump, manage flows (~1–1.5 days)

- [ ] Browse: paginated task cards (desc, pay, slots, category) with ◀ ▶ paging buttons and a **Jump** button per card; jump errors (own task / full / duplicate) rendered as friendly toasts
- [ ] My jumps: participation list with status emoji per state (pending/active/submitted/verified/rejected/forfeited), Forfeit button on forfeitable states, "Submit proof" button stubbed to the upload path (section 5)
- [ ] My tasks (Launcher view): own tasks with status + jump counts; for manual-approval tasks, list pending Jumpers with **Approve / Decline** buttons
  - Approve → existing `POST /tasks/{id}/jumps/{jump_id}/approve`
  - Decline → **backbone extension needed** (section 6)
  - Listing pending jumps → **backbone extension needed** (section 6)
- [ ] Task detail view from any card (status, filters summary, deadlines)

## 5. Screen-recording upload path (~0.5–1 day now, +1 day at stage B)

The catch from the todo table: bots can only *download* files up to ~20MB via
the standard Bot API, and screen recordings routinely exceed that.

- [ ] **Stage A (MVP, build now)**: accept video/document uploads in the
  submit-proof flow; if `file_size` > limit, reply with clear guidance
  (compress / trim) instead of failing silently; store accepted files via the
  API (upload endpoint belongs to the verification BOM — until it exists, the
  flow stops at "received, verification coming soon" behind a feature flag)
- [ ] Stage A size guard reads the limit from config (`TG_FILE_LIMIT_MB=20`) so
  Stage B is a config change, not a code change
- [ ] **Stage B (when verification lands)**: self-hosted `telegram-bot-api`
  server (Docker container, needs `api_id`/`api_hash` from my.telegram.org),
  raising the download cap to 2GB. UX unchanged — users just send the video.
  Documented as a deploy artifact, not bot code
- [ ] Rejected alternative, recorded: presigned-URL uploads to object storage —
  more moving parts (bucket + upload page) and breaks the everything-in-Telegram
  promise; reconsider only if self-hosting the Bot API proves painful

## 6. Backbone extensions this component needs (~0.5 day, in `src/`)

Small, well-bounded additions to the existing API — each with tests, same
standards as the backbone BOM:

- [ ] `POST /auth/telegram` — trusted bridge: requires `X-Bridge-Secret` header
  (constant-time compare against `BOT_BRIDGE_SECRET`); body `{telegram_id,
  telegram_handle}`; creates the user if new (no email/password — nullable
  password_hash or sentinel), updates handle drift, returns a token pair.
  Audit event `auth.telegram_bridge`
- [ ] `GET /tasks/{task_id}/jumps` — owner-only listing (filter by status) so
  the Launcher can see who jumped; powers the Approve/Decline UI
- [ ] `POST /tasks/{task_id}/jumps/{jump_id}/reject` — Launcher declines a
  pending jump (PENDING → REJECTED, `resolved_at` set); symmetric to approve;
  audit event `task.jump_rejected`
- [ ] Note: `User.password_hash` becomes nullable for bridge-created accounts —
  migration + guard in password login ("this account uses Telegram sign-in")

## 7. Polish & tests (~1 day)

- [ ] Error taxonomy: API 4xx `detail` → human phrasing in `texts.py`; network
  errors → "backend unreachable, try again"; never a stack trace in chat
- [ ] Per-user flood guard (aiogram middleware, simple token bucket)
- [ ] Logging with telegram_id + request correlation to API logs
- [ ] Unit tests for flow handlers with a mocked `api_client` (aiogram test
  utilities); integration test of `api_client` against the real API via
  TestClient-style fixture
- [ ] Manual test checklist in this file's appendix: every command, every
  cancel point, every error path, run against the live pair of processes
- [ ] **Done when**: with `make run` + `make bot` and a real bot token, a phone
  can /start, launch a filtered task through the full FSM, a second account can
  browse and jump, the Launcher approves from /mytasks, and /cancel works at
  every step of every flow

## Lessons to honor (from the old project + concept docs)

- [x] Every user-facing string lives in `texts.py` — no literals scattered through handlers
- [x] Every flow step is cancellable; no conversational dead ends
- [x] Confirmation before any money-adjacent or irreversible action
- [x] The bot owns zero business logic — if the bot needs a rule, the API grows an endpoint; grep for `SessionLocal` in `src/bot/` must return nothing
- [x] No secrets in code; `BOT_TOKEN` and `BOT_BRIDGE_SECRET` only via Settings

## Appendix — manual test checklist (live DoD, needs a @BotFather token)

Setup: put `BOT_TOKEN` in `.env`, run `make run` and `make bot`, message the bot
from a phone. Second account: any other Telegram user (or a second client).

1. `/start` — welcome + menu appears; `/profile` shows your handle, no email
2. `/launch` full flow: description → budget 50 → pay 5 → 10 Jumpers → location
   "Istanbul" → age 18–25 → gender any → deadline skip → auto-accept → confirm
   card correct → launch succeeds with task id
3. In-flow validation: text where a number belongs re-asks; pay 100 on budget 50
   is refused with the max-affordable hint
4. `/cancel` at three different steps — always escapes, `/start` works after
5. Cancel **button** mid-flow — same result
6. Second account: `/browse` shows the card "1 of N"; paging works; Jump →
   confirmation message; jumping again → "Can't jump" alert
7. Launch a manual-approval task; second account jumps → "pending" message;
   first account `/mytasks` → Jumpers → Approve and Decline both work
8. `/myjumps` on the second account — statuses correct; Forfeit works; task
   reopens for others
9. Submit proof: send a >20MB video → friendly size guidance, flow stays;
   send a small video → "got it, verification coming soon"
10. Send a text where a file is expected → guidance; group chat → polite refusal
11. Spam-tap a button rapidly — flood notice appears once, bot stays responsive
