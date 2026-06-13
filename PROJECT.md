# filepath: PROJECT.md

# Crowdjump

**Crowdjump is a peer-to-peer marketplace where verified humans get paid to perform digital tasks — and prove they did them.**

You launch a task. The crowd jumps on it.

---

## The Problem

Anti-bot defenses have made automation worthless across the digital world. Genuine human engagement — likes, reviews, follows, feedback, any action that requires a real person — has become the scarcest digital commodity. But there is no market for it:

- Businesses and creators can't buy authentic engagement; they can only buy bots that get filtered or agencies that overcharge.
- People with free time and an internet connection have no direct way to sell small units of digital work, especially outside rich banking systems.
- Platforms decide who gets visibility through opaque algorithms; there is no way to simply pay real humans to look.

## The Idea

Crowdjump is a **trust machine that makes authentic human action purchasable**. Everything in the product reduces to selling three verified things:

1. **Verified humans** — every Jumper passes identity verification (ID + selfie + biometric duplicate detection). No bots, no multi-accounts.
2. **Verified attributes** — uploaded proofs (ID, selfie, credentials, social accounts) are processed once into reusable verified attributes (age, location, gender, education, ...). These power precise demographic targeting.
3. **Verified work** — Jumpers screen-record task execution. AI analyzes the recording, extracts what happened, and produces evidence. Payment releases only on verified completion.

Payments, matching, and the bot interface are plumbing around those three verifications. The verified-attribute graph is the moat: anyone can build a task board; nobody else can prove *who* did *what*.

Interactions are intentionally transactional — Crowdjump is a marketplace crossed with social media, where attention and action have explicit prices.

## Roles

| Role | Who they are | What they do |
|---|---|---|
| **Launcher** | Businesses, creators, anyone needing human action | Launches tasks: description, budget, participant count, deadlines, demographic filters. Funds escrow. Reviews results |
| **Jumper** | Verified real humans, anywhere in the world | Jumps on tasks matching their verified attributes, performs them while screen-recording, gets paid in crypto on verification |

## How It Works

1. **Launch** — a Launcher describes the task, sets budget and per-Jumper pay, picks demographic filters and deadlines, and funds the escrow address.
2. **Jump** — matched, verified Jumpers are notified and jump on the task (optionally the Launcher approves each Jumper manually).
3. **Perform** — the Jumper completes the task while screen-recording.
4. **Verify** — the recording is uploaded; AI extracts what happened (apps, profiles, actions, timing) and assembles evidence; completion is judged against the task requirements.
5. **Pay** — escrow releases the Jumper's earnings, Crowdjump takes its commission. Disputes go to a review process with the evidence package.

## Interface

- **Telegram-first**: the entire product works through a Telegram bot — structured commands and guided flows, no app install.
- **REST API underneath**: the bot is a client of a public API. The API is a first-class product surface — open by design, including for non-human callers (when AGIs need human hands, Crowdjump is the way to hire them).

## Payments

- Cryptocurrency escrow: each task is funded up front; Jumpers are paid automatically on verified completion.
- MVP runs a single stablecoin (USDT) on a single low-fee chain.
- Crowdjump charges a commission on completed tasks.

## Scope

### MVP — the smallest loop that proves the bet

- **Verification**: email + ID/selfie with biometric duplicate detection. Hybrid pipeline: AI extracts, a human approves.
- **Targeting**: four demographics — location, age range, gender, education. Pure SQL binary matching.
- **Interface**: command-based Telegram bot backed by the REST API. No natural-language task creation.
- **Work verification**: hybrid — vision-model frame analysis extracts actions and evidence; a human makes the final approve/reject call.
- **Money**: one coin, one chain, simple escrow, fixed commission, withdrawals.
- **Trust**: simple displayed trust score (verification 40% / task success 40% / account age 20%). Manual Jumper approval (`accept_jumpers_manually`) as the cheap substitute for trust infrastructure.
- **Hygiene**: event audit log, encrypted sensitive fields, proofs stored separately from extracted attributes.

The MVP must prove three things:

1. Jumpers will complete verified onboarding to access paid tasks.
2. Launchers will fund escrow for targeted, authentic engagement.
3. Screen-recording verification is reliable enough to release money on.

### Beyond MVP

- Full attribute graph: education, employment, social-account proofs (follower counts, account age) for premium targeting.
- Autonomous verification: shrink the human review share toward zero as the video pipeline matures.
- Differential pay per attribute group (e.g. ages 18–25 earn $10, 25–35 earn $7 on the same task).
- Task halving: per-Jumper pay automatically increases over time for hard-to-fill tasks.
- Natural-language task creation, multi-chain payments, trust-gated privileges, task templates, campaign analytics.
- Web and mobile apps beyond Telegram.
- The public AGI-facing API as a product in its own right.

## Terminology

| Term | Meaning |
|---|---|
| **Launch** | Post and fund a task |
| **Jump** | Accept a task |
| **Launcher** | The paying side (formerly: poster, bay) |
| **Jumper** | The performing side (formerly: performer, crow) |
| **Proof** | A document/recording a Jumper uploads for verification (ID, selfie, credential) |
| **Attribute** | A verified fact extracted from proofs (age, location, education, ...) |
| **Evidence** | Frames and extracted data proving task completion |

## Open Decisions

- **Chain**: TRON (TRC-20 USDT is what Telegram-native users hold, but per-transfer energy costs are real) vs Polygon (near-zero gas, weaker retail USDT habit).
- **Commission**: historic docs range from 1% to 10%; pick one number before MVP pricing copy.
- ~~**MVP task categories**~~ **DECIDED 2026-06-12** — ToS-posture matrix v1 ratified (`devdocs/inquiries/2026-06-12_14-37__tos-posture-decision/finding.md`): real-human engagement ALLOWED with two-sided disclosure (Launcher purge-risk line + Jumper account-risk notice + one-time opt-in + feed filter, default show-with-notice); incentivized PUBLIC reviews GATED (private-feedback repair path); spam GATED; political/coordinated engagement HELD; per-row kill-switches in config. Positioning principle: Crowdjump markets as a verified-human digital-work marketplace, never in boost/manipulation language. Revisit gates: counsel · fiat rails · app store · platform contact · purge-rate threshold. Public form: `TASK_POLICY.md`.

## Project History

Previously named **Performerd**, then **Crowd** / **crowbay**. Older docs in `devdocs/` and `SemanticVideoInspector/` predate the rename and still use the old names and the old role words (posters/performers, bays/crows) — read them with this mapping: *poster/bay → Launcher, performer/crow → Jumper*. The first implementation attempt and its OpenAPI spec (`api_spec.yaml`) live in `depricated_src/` for reference and are scheduled for deletion. `SemanticVideoInspector/` documents the screen-recording verification engine (design only, no code yet).
