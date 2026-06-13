# filepath: fe/devdocs/webapp_page.md

# Crowdjump Dev Web Client — Telegram-style UI Design

A browser client that looks and behaves like the Telegram bot, used to
exercise the backend by hand before launching on Telegram. Two browser tabs
= a Launcher and a Jumper, no phone numbers needed.

## Why this approach (and its boundary)

- **Tests the API, not the bot.** Every click below maps to a REST call
  (annotated under each screen). The bot's aiogram handlers are NOT
  exercised — the conversational flow logic is intentionally duplicated
  here in JS.
- **Stays throwaway-cheap.** One static HTML file + vanilla JS, no
  framework, no build chain. Token in localStorage, API at
  `http://localhost:8000` (CORS already allows localhost dev origins).
- **Wording is borrowed, not invented.** All strings copy
  `src/bot/texts.py` so the web flows and bot flows stay in sync by eye.
- **Auth**: email/password register/login (already built) — the Telegram
  bridge is not used by this client.

Mockups are ASCII-only for alignment; the real UI uses the same emoji as
the bot (🚀 👀 📋 🐦 ⏳ ✅ ❌ 🏳️).

## Component vocabulary

```
+----------------------------------------------+
| <  Crowdjump                            (=)  |   header bar
+----------------------------------------------+
|  +--------------------------------+          |
|  | bot bubble (left-aligned)      |          |   bot message
|  +--------------------------------+          |
|          +--------------------------------+  |
|          |        user bubble (right)     |  |   user message
|          +--------------------------------+  |
|  [ inline button ]  [ inline button ]        |   inline keyboard
|  ~ toast: error text, auto-hides ~           |   toast (API 4xx detail)
+----------------------------------------------+
| > type a message...                   [send] |   input bar
+----------------------------------------------+
```

## S0 — Login / Register

```
+----------------------------------------------+
|              C R O W D J U M P               |
|       Launch a task. The crowd jumps.        |
|                                              |
|   email     [ jumper1@example.com        ]   |
|   password  [ ************              ]    |
|                                              |
|        [ Log in ]      [ Register ]          |
|                                              |
|   ~ toast: Invalid email or password ~       |
+----------------------------------------------+
```
- Register → `POST /auth/register` → store token pair
- Log in  → `POST /auth/login`
- On 401 anywhere later → `POST /auth/refresh`, retry once (same trick as
  the bot's ApiClient)

## S1 — Home (main menu as chat)

```
+----------------------------------------------+
| <  Crowdjump                            (=)  |
+----------------------------------------------+
|  +--------------------------------+          |
|  | Welcome to Crowdjump!          |          |
|  | Launch a task - the crowd      |          |
|  | jumps on it.                   |          |
|  | What would you like to do?     |          |
|  +--------------------------------+          |
|                                              |
|  [ Launch a task ]                           |
|  [ Browse tasks  ]                           |
|  [ My tasks ]  [ My jumps ]                  |
|  [ Profile  ]  [ Help     ]                  |
|                                              |
+----------------------------------------------+
| > type /launch, /browse ...           [send] |
+----------------------------------------------+
```
- Typed commands work like buttons (`/launch`, `/browse`, `/cancel`...)
- `GET /users/me` on load (header shows who you are)

## S2 — Launch wizard (chat steps, mirrors the bot FSM)

Step 2 of 6 (money) and the budget guard:

```
|  +--------------------------------+          |
|  | Step 2/6 - Jumpers             |          |
|  | How many Jumpers do you need?  |          |
|  +--------------------------------+          |
|          +-----------+                       |
|          |    100    |                       |
|          +-----------+                       |
|  +--------------------------------+          |
|  | That needs 500.0 total but     |          |
|  | your budget is 50.0.           |          |
|  | With this pay you can afford   |          |
|  | at most 10 Jumpers - enter a   |          |
|  | smaller count:                 |          |
|  +--------------------------------+          |
|  [ Cancel ]                                  |
```

Confirmation card (step 6) with audience preview + advisory warning:

```
|  +--------------------------------+          |
|  | Step 6/6 - Confirm your task   |          |
|  |                                |          |
|  | Review our app                 |          |
|  | Budget: 50 USDT                |          |
|  | 10 Jumper(s) x 5 USDT          |          |
|  | Who: location: EMEA but not    |          |
|  |   Russia, age 18-25, female    |          |
|  | Deadline: 7 days               |          |
|  | Mode: auto-accept              |          |
|  |                                |          |
|  | Verified Jumpers matching      |          |
|  | right now: fewer than 10       |          |
|  | ! Location is free text only - |          |
|  |   it won't constrain matching  |          |
|  |   until parsed                 |          |
|  |                                |          |
|  | Launch it?                     |          |
|  +--------------------------------+          |
|  [ Launch it ] [ Start over ] [ Cancel ]     |
```
- Validation rules identical to the bot (client-side copy)
- Audience line → `POST /tasks/audience-preview` (filters from the wizard)
- Launch it → `POST /tasks` (assemble the same payload as
  `bot/flows/launch.py:build_payload`)

## S3 — Browse (one card per page, like the bot pager)

```
|  +--------------------------------+          |
|  | Task 2 of 7                    |          |
|  |                                |          |
|  | Review our shiny app           |          |
|  | You earn: 5 USDT               |          |
|  | Slots: 10   Category: reviews  |          |
|  | auto-accept                    |          |
|  +--------------------------------+          |
|  [ < Prev ]  [ Next > ]                      |
|  [ Jump on this ]                            |
|  [ Menu ]                                    |
|                                              |
|  ~ toast: Can't jump: Task is full ~         |
```
- Page → `GET /tasks?status=open&page=N&size=1` (eligible feed — tasks the
  logged-in user doesn't match are simply absent)
- Jump → `POST /tasks/{id}/jump`; 403 shows the unmet requirements toast —
  this is how you demo the eligibility gate

## S4 — My jumps (Jumper view)

```
|  +--------------------------------+          |
|  | Your jumps                     |          |
|  | [#12] Review our app - 5 USDT  |          |
|  |       status: active           |          |
|  | [#09] Follow my page - 2 USDT  |          |
|  |       status: pending          |          |
|  | [#07] Old task - 3 USDT        |          |
|  |       status: forfeited        |          |
|  +--------------------------------+          |
|  [ Submit proof #12 ] [ Forfeit #12 ]        |
|  [ Forfeit #09 ]                             |
```
- `GET /tasks/participated`; Forfeit → `POST /tasks/{id}/forfeit`
- Submit proof → file input; client-side size guard mirrors
  `TG_FILE_LIMIT_MB`, then the "received, verification coming soon" stub

## S5 — My tasks (Launcher view + Jumper management)

```
|  +--------------------------------+          |
|  | Your launched tasks            |          |
|  | [#14] curated task             |          |
|  |       1 slot - open            |          |
|  +--------------------------------+          |
|  [ Jumpers of #14 ]                          |
|                                              |
|  +--------------------------------+          |
|  | Jumpers of task #14            |          |
|  | Jumper 7 - pending             |          |
|  | Jumper 9 - active              |          |
|  +--------------------------------+          |
|  [ Approve 7 ]  [ Decline 7 ]                |
```
- `GET /tasks/my`, `GET /tasks/{id}/jumps`
- Approve/Decline → `POST /tasks/{id}/jumps/{jid}/approve|reject`

## S6 — Profile (incl. the full phone-OTP demo)

```
|  +--------------------------------+          |
|  | Your profile                   |          |
|  | Email: jumper1@example.com     |          |
|  |   verified: no  [ Resend ]     |          |
|  | Phone: -                       |          |
|  | Verifications: none yet        |          |
|  | Trust score: -                 |          |
|  | Notifications: on  [ Mute ]    |          |
|  +--------------------------------+          |
|                                              |
|  phone [ +49 170 1234567 ] [ Send code ]     |
|  code  [ ______ ]          [ Verify    ]     |
|                                              |
|  ~ the OTP appears in the API console        |
|    (mock Twilio) - paste it here ~           |
```
- `GET /users/me`, `POST /auth/resend-verification`
- `POST /auth/phone/request` → code in API logs → `POST /auth/phone/verify`
- Mute → `POST /users/me/notifications {muted}`

## Error handling pattern

Every non-2xx response renders its `detail` as a toast in bot voice
("Can't do that: …"), same mapping as `bot/texts.friendly_api_error`.
Never show a stack trace; network failure → "backend unreachable".

## Known gaps this client exposes

1. **No notifications read endpoint.** The ledger exists
   (`notifications` table) but there is no `GET /users/me/notifications`,
   so the web client can't show "you were approved" the way Telegram push
   would. Smallest backend addition this UI wants — until then, statuses
   are visible by refreshing My jumps.
2. **Proof upload is a stub** behind `PROOF_UPLOAD_ENABLED` — the flow ends
   at "received" by design until the verification component lands.
3. This client bypasses the bot entirely — flows that live in aiogram
   (cancel-anywhere, flood guard) are re-implemented or skipped here and
   still need the phone-in-hand checklist before a real Telegram launch.

## Build plan (deliberately tiny)

- `fe/index.html` — markup + styles (chat layout, bubbles, buttons)
- `fe/app.js` — state machine for the wizard, fetch wrapper with refresh
  retry, screen renderers
- Serve with anything static (`python -m http.server 5173`) — CORS for
  localhost:5173 is already allowed by the API
- No dependencies, no build step; if it ever needs a framework, that's the
  signal it's becoming the real web app and deserves its own BOM
