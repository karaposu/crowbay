# filepath: how_to_run_webapp.md

# How to Run the Crowdjump Dev Web App

## The logic: what runs where

The web app is **two separate processes** (plus an optional third). Nothing
starts anything else automatically — each gets its own terminal.

```
+--------------------+        HTTP (fetch)        +----------------------+
|  Web client :5173  |  ------------------------> |  Backend API :8000   |
|  static files only |   login, tasks, jumps,     |  FastAPI + SQLite    |
|  (fe/index.html,   |   preview, notifications   |  THE product — all   |
|   fe/app.js)       |                            |  rules live here     |
+--------------------+                            +----------+-----------+
                                                             |
+--------------------+        HTTP (same API)                |
|  Telegram bot      |  -------------------------------------+
|  (optional)        |   the bot is just another client
+--------------------+
```

- **The API is the product.** Web client and bot are both thin clients of
  the same REST API; neither contains business rules.
- **The web client is just files.** `python3 -m http.server` only *serves*
  `fe/` to your browser; all real work happens via `fetch()` calls to
  `:8000`. If the API is down, every click shows "backend unreachable".

## Quick start (two terminals)

```bash
# terminal 1 — backend API
make run

# terminal 2 — web client
cd fe && python3 -m http.server 5173
```

Open **http://localhost:5173** → Register with any email + password (8+ chars).

**Two roles trick**: open a second browser tab in a *private/incognito
window* (so it has its own login) and register a second account — one tab
is the Launcher, the other the Jumper.

## What the web client can do

Telegram-style chat UI mirroring the bot's flows (wording copied from
`src/bot/texts.py`):

- **Login/register** (email+password; token refresh handled automatically)
- **Launch wizard** — six steps with the same validation as the bot
  (budget guard with max-affordable hint), audience preview + filter
  warnings on the confirmation card
- **Browse** — one task card per page, prev/next, Jump (a 403 here is the
  matching eligibility gate doing its job)
- **My jumps** — statuses, Forfeit, Submit-proof (size-guarded stub until
  the verification component lands)
- **My tasks** — Launcher view with per-task Jumper Approve/Decline
- **Profile** — resend verification email, phone OTP wizard, mute toggle
- **Bell bubbles** — notification polling every 8s
  (`GET /users/me/notifications`)

## Dev superpowers (everything is mocked, codes appear in terminal 1)

- **Phone OTP**: Profile → Verify phone → the 6-digit code is printed in
  the **API console** (mock Twilio): `SMS (mock twilio) ... body='Your
  Crowdjump verification code: 123456'`
- **Email verification**: the link is printed in the API console
  (console email backend)
- **Verified attributes** (so filtered tasks match someone): grant from a
  third terminal, e.g.
  ```bash
  cd src && ../.venv/bin/python -m db.seed_dev \
      --email jumper@example.com --country germany --gender female \
      --birth-date 2002-05-01
  ```

## Stopping things / "Address already in use"

`Ctrl+C` in each terminal stops that process. If a port is stuck (terminal
closed without Ctrl+C, or an orphaned background run):

```bash
# who is holding the port?
lsof -nP -iTCP:8000 -sTCP:LISTEN     # or :5173

# kill it
kill <PID>
```

**The --reload gotcha**: `make run` uses uvicorn `--reload`, which runs a
*watcher parent + server child*. If you kill only the child, the watcher
instantly respawns it and the port stays busy. Kill the parent (check
`ps -o ppid= -p <PID>`) or just Ctrl+C the terminal it runs in.

One-liner to free both dev ports:

```bash
lsof -tiTCP:8000 -sTCP:LISTEN | xargs kill; lsof -tiTCP:5173 -sTCP:LISTEN | xargs kill
```

## Fresh database

```bash
rm src/db/data/crowdjump.db*      # the * also removes -wal/-shm
make migrate seed
```

## Optional: the Telegram bot (terminal 3)

Only needed when testing real Telegram — the web client covers everything
else. Requires `BOT_TOKEN` from @BotFather in `.env`:

```bash
make bot
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "backend unreachable" toast | API not running | `make run` in terminal 1 |
| `[Errno 48] Address already in use` | stuck process on the port | see lsof/kill recipe above |
| Browse shows a task but Jump → 403 | matching gate: your account lacks the verified attributes the task filters on | grant attributes via `db.seed_dev` (above) |
| Filtered task invisible in Browse | same as above — the feed only shows tasks you're eligible for | same fix |
| Login says "Session expired" | refresh token (14 days) expired or DB was wiped | log in again / re-register |
| New endpoints 404 although code exists | stale API process from before the change | restart `make run` |
