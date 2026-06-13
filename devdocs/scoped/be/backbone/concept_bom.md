# filepath: devdocs/scoped/be/backbone/concept_bom.md

# Backbone BOM — FastAPI + JWT + DB

> **Status: IMPLEMENTED** (2026-06-12). All five sections done and verified: 18 passing tests,
> ruff clean, lessons-learned greps pass, live register→launch→jump round-trip confirmed.
> Deviations from this BOM: (1) added `POST /tasks/{id}/jumps/{jump_id}/approve` — the manual-
> approval flow needed a Launcher approve action or pending jumps would be stuck; pending jumps
> don't consume capacity, approval does. (2) `get_verified_user` exists but task routes currently
> require only `get_current_user` — whether launching/jumping demands a verified email is an open
> product call. (3) ruff: FastAPI's `Depends`/`Query`/`Security` declared immutable (B008).

Bill of materials for the backbone component: the FastAPI application, authentication, and database layer that every other component (bot, escrow, verification pipeline, matching) plugs into. Estimated 3–5 days solo; effort noted per section.

**In scope**: app skeleton, config, DB layer + all MVP tables, auth, core task/jump endpoints, tests.
**Out of scope** (separate BOMs): Telegram bot, escrow/payments logic, video verification pipeline, matching fan-out/notifications, admin review tooling.

---

## 0. Decisions encoded here (veto before starting)

| Decision | Choice | Rationale |
|---|---|---|
| JWT `sub` | always `user_id` (string-encoded int) | old code mixed email/user_id across services |
| Account model | one account can act as both Launcher and Jumper | role is per-action, not per-account; matches docs |
| Token purposes | separate `purpose` claim: `access`, `refresh`, `email_verify`, `pw_reset` | old code let an email-verify token shape pass as access |
| Refresh flow | short access token (30 min) + refresh token (14 days), `POST /auth/refresh` takes the refresh token | the old refresh-by-email endpoint was an auth bypass |
| Password reset | request → emailed one-time token → set new password | the old endpoint reset any account unauthenticated |
| Migrations | Alembic from day one | schema will evolve weekly; SQLite → Postgres path stays open |
| DB | SQLite (WAL) for MVP, engine/session defined in exactly one module | three competing conventions last time |
| Pydantic models | hand-written, no OpenAPI codegen | stale generated models caused the worst drift last time |
| Services | plain functions `(session, args) -> result`; thin routers | no `__init__`-side-effect service classes, no DI container |
| Verification tables | port `depricated_src/db/models/verification.py` near-verbatim | the one good artifact; implements the 8-table design |
| Timestamps | `datetime.now(timezone.utc)` everywhere | `utcnow()` is deprecated and was inconsistently used |
| Port | 8000 | old code had 3000-vs-8000 confusion |

## 1. Scaffolding & config (~0.5 day)

- [ ] Directory layout:
  ```
  src/
    app.py            # FastAPI factory: middleware, routers, exception handlers
    config.py         # pydantic-settings Settings (the only env access point)
    db/
      engine.py       # engine + sessionmaker — the ONLY place they exist
      base.py         # DeclarativeBase + constraint naming conventions
      deps.py         # get_db request-scoped session dependency
      models/         # user.py, task.py, jump.py, payment.py, verification.py, audit.py
      seed.py         # reference data (proof_types, verification_types)
    migrations/       # alembic
    schemas/          # auth.py, task.py, jump.py, common.py (hand-written pydantic)
    routers/          # auth.py, users.py, tasks.py, health.py
    services/         # auth.py, tasks.py — plain functions
    tests/
  ```
- [ ] `requirements.txt`, minimal: fastapi, uvicorn, sqlalchemy, alembic, pydantic, pydantic-settings, pyjwt, bcrypt (or passlib[bcrypt]), email-validator, pytest, httpx
- [ ] `Settings` via pydantic-settings: `SECRET_KEY` (required — **fail at startup with a clear message**, not at request time), `DATABASE_URL`, `ACCESS_TOKEN_MINUTES`, `REFRESH_TOKEN_DAYS`, `ENV`
- [ ] `.env.example` committed; `.env` ignored; add `*.db` to `.gitignore` (the old `crowd.db` was committed with a user row in it)
- [ ] Middleware: request-ID (keep the old pattern — it was fine), CORS restricted to localhost dev origins (the old list was another project's production domains)
- [ ] Logging: stdlib config, console + optional file via settings; **never log passwords or tokens** (old code logged both at debug)
- [ ] `Makefile` or `justfile`: `run`, `test`, `migrate`, `makemigration`, `seed`

## 2. Database layer (~1–1.5 days)

- [ ] `engine.py`: engine from `Settings.DATABASE_URL`, absolute path resolution (the old relative path silently created an empty second DB), `check_same_thread=False`, WAL mode for SQLite
- [ ] `base.py`: `DeclarativeBase` with naming conventions (named FKs/uniques/indexes so Alembic diffs stay clean)
- [ ] `deps.py`: yield-session dependency — commit on success, rollback on exception, always close
- [ ] Alembic init wired to the same Base/engine; initial migration generates the full schema
- [ ] Models:
  - [ ] `User` — email (unique), password_hash, telegram_id/handle, created_at, `is_email_verified` (**fix the `is_eamil_verified` typo in the port**), demographic columns stay OUT of users (they live in `verification_data`)
  - [ ] `Task` — owner FK, desc, total_budget, you_earn, num_jumpers, status (enum: draft/open/full/completed/cancelled/disputed), partition_deadline, submission_deadline, category, `accept_jumpers_manually`, `launcher_review`, **`filters` JSON column** (persisted verbatim per `devdocs/filter_design.md` — the old model silently dropped filters), `operation_requirements`/`other_requirements` JSON
  - [ ] `Jump` (task participation — the table the old schema never had) — task FK + jumper FK (unique together), status (enum: jumped/approved/submitted/verified/rejected/forfeited), timestamps per transition
  - [ ] `Payment` — ledger rows: user FK, optional task FK, type (deposit/withdrawal/escrow_hold/payout/commission), coin_ticker, amount, status, tx reference, created_at (escrow *logic* is the payments BOM; the table lands here so FKs exist)
  - [ ] Verification tables — port the 8 tables from `depricated_src/db/models/verification.py`: ProofType, VerificationType, VerificationProofRequirement, UserProof, UserVerification, VerificationProofUsage, VerificationData, VerificationHistory; keep indexes; swap `datetime.utcnow` for tz-aware
  - [ ] `AuditEvent` — single table per the event-based audit concept: event_type, actor_id, target ids, JSON payload, created_at, indexed on (event_type, created_at) and actor (the old `logs.py` had its own orphaned Base — don't repeat that)
- [ ] `seed.py`: MVP reference rows — proof_types (government_id_photo, selfie_video), verification_types (basic_identity, age, gender, location) + their proof requirements
- [ ] Sanity check: `alembic upgrade head` + seed on a fresh checkout produces a working DB with zero manual steps

## 3. Auth (~1 day)

One module owns every token and hash. No second implementation, ever.

- [ ] Password hashing: bcrypt; verify + needs-rehash helper
- [ ] Token mint/verify helpers: `purpose` claim enforced on decode (an `email_verify` token can never authenticate a request), `exp`/`iat`, single `SECRET_KEY` from settings — **no hardcoded fallback** (the old `"your_secret_key"` literals meant tokens couldn't verify across services)
- [ ] Endpoints:
  - [ ] `POST /auth/register` — email + password, returns access + refresh; fires email-verification send (email sending itself may stub to log in dev)
  - [ ] `POST /auth/login`
  - [ ] `POST /auth/refresh` — refresh token in body, rotates and returns new pair
  - [ ] `GET /auth/verify-email?token=` — purpose-checked, idempotent
  - [ ] `POST /auth/request-password-reset` — always 200 (no account enumeration), emails one-time token
  - [ ] `POST /auth/reset-password` — token + new password
- [ ] Dependencies: `get_current_user` (decode → load → 401), `get_verified_user` (email verified) — routers depend on these instead of re-decoding (the old `get_token_bearerAuth` was an unimplemented stub returning None)
- [ ] No dev backdoors of any kind (the old code had a `dev@test.com` predefined token)
- [ ] Deferred, note only: rate limiting on auth routes, token revocation/denylist

## 4. Core endpoints (~1 day)

- [ ] `GET /health` — DB ping + version
- [ ] `GET /users/me` — profile, email-verified flag, verification summary (which verifications current), placeholder trust score
- [ ] Tasks:
  - [ ] `POST /tasks` (launch) — validates against schemas incl. typed `basic_filters` subset from filter_design.md; persists filters verbatim; status `open`
  - [ ] `GET /tasks` — browse with query params (status, category, budget floor); plain pagination envelope; **no matching logic yet** (matching BOM)
  - [ ] `GET /tasks/{id}`, `GET /tasks/my`, `GET /tasks/participated`
  - [ ] `POST /tasks/{id}/jump` — creates Jump; honors `accept_jumpers_manually` (pending vs auto-approved); rejects when full/closed/own task/duplicate
  - [ ] `POST /tasks/{id}/forfeit` — Jumper backs out; frees the slot
  - [ ] Boundary: proof submission + validation endpoints belong to the verification BOM; payment endpoints to the payments BOM
- [ ] Consistent error envelope (`{"detail": ...}`), exception handlers for ValidationError/IntegrityError/404; audit events written for register, login, task launch, jump, forfeit

## 5. Tests & definition of done (~0.5–1 day)

- [ ] pytest + httpx `TestClient`; per-test tmp SQLite via the same engine module (proves there's only one)
- [ ] Auth: register→login→me round-trip; refresh rotation; wrong-purpose token rejected; expired token rejected; password-reset full flow; no account enumeration
- [ ] Tasks: launch persists filters byte-identical; jump happy path; duplicate/own-task/full rejections; forfeit frees slot; manual-approval path
- [ ] ruff (lint + format) clean
- [ ] **Done when**: fresh clone → `make migrate seed run` → register, login, launch a task with filters, jump on it from a second account — all via tests and once by hand via `/docs`

## Lessons-learned checklist (from the deprecated src — verify before calling done)

- [ ] Exactly one engine/sessionmaker definition; grep proves it
- [ ] Exactly one place mints/verifies JWTs; grep for `jwt.encode` proves it
- [ ] No secrets or absolute personal paths in code; settings only
- [ ] No model attribute written that isn't a mapped column (`hashed_password`, `is_verified`, `user_id` were all silent bugs)
- [ ] Filters arrive → filters persist → filters return; nothing dropped silently
- [ ] No file claims a different `# filepath:` than where it lives
