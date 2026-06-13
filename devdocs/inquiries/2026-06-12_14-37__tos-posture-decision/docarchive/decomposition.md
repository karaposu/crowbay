# Decomposition — ToS-Posture Decision

## User Input

/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_14-37__tos-posture-decision/_branch.md
(operating on sensemaking SV6: 5-row category policy + honesty mechanism + wrappers + recommend-then-ratify)

## Step 1 — Coupling Map

Elements: row definitions (engagement / public-reviews / fraud-adjacent / neutral / unknown) · boundary tests (public-review vs private-feedback; engagement vs fraud-adjacent) · per-row dispositions + rationales · decline/warn text seeds · Launcher disclosure line · Jumper risk notice · the notice's HOME (task display — outside the clarifier) · per-row exposure map (Jumper account, Launcher spend, platform legal, reputational/positioning) · enforcement-reality evidence · positioning principle · fail-open coupling rule · revisit gates · values-residue presentation · ratification protocol · consumers-update plan (CJ-K3 wording, clarifier registry templates, PROJECT.md ③, meta-def register ①, BOM knob) · jurisdiction/counsel flags.

**Clusters:**
- K1 *the line*: row definitions ↔ boundary tests (a definition change moves every test)
- K2 *dispositions*: row values ↔ rationales ↔ decline/warn text seeds (one verdict per row, text follows verdict)
- K3 *the evidence*: exposure map ↔ enforcement reality ↔ who-bears-what (the audit layer that justifies K2)
- K4 *the honesty mechanism*: Launcher line ↔ Jumper notice ↔ notice's home (one mechanism, two surfaces)
- K5 *wrappers*: positioning ↔ fail-open coupling ↔ revisit gates (system rules AROUND the matrix, none row-specific)
- K6 *ratification & propagation*: authority protocol ↔ values-residue presentation ↔ staged consumer updates ↔ flags (everything that happens AT and AFTER the decision)

**Valleys:** K1↔K2 cross only via row definitions; K3↔K2 only via per-row evidence; K2↔K4 only via "which rows warn"; K5 touches all but through stated rules, not shared state; K6 consumes finished outputs only.

## Step 2 — Boundaries (Top-Down)

Six pieces: P1=K1, P2=K2, P3=K3, P4=K4, P5=K5, P6=K6. The evidence (P3) is deliberately cut FROM the dispositions (P2): the audit has standalone value (the risk-audit articulation) and a different epistemic status (representative knowledge, not-counsel) than the verdicts it supports — different change drivers (new evidence updates P3; new values update P2).

## Step 3 — Bottom-Up Validation

Atoms: the public-vs-private-feedback test → K1 ✓ · the "no claims made" qualifier on engagement → K1 ✓ · per-row severity enum → K2 ✓ · the FTC sentiment-buying fact → K3 ✓ · the Jumper notice's home (task display, outside clarifier) → K4 ✓ (cross-component, flagged in interfaces) · the C&D revisit gate → K5 ✓ · the one-line ratification ask → K6 ✓ · `tos_category: unknown` log field → K2 (disposition) with its consumer in K6 (registry update) ✓ (definition-vs-consumer split, normal). No atom splits against its cluster. **Confidence: HIGH.**

## Step 4 — Question Tree

**P1 — The category line.** *What exactly are the rows, and what test places a task in each?*
- [ ] row definitions: engagement (real-human actions on public surfaces, no claims made, paid-for-action) · public incentivized reviews (content presented to third parties as opinion, on a review surface) · fraud-adjacent mechanics (account handover, captcha farming, login-walled scraping) · platform-neutral work · unknown-ToS-sensitive
- [ ] the carve-out test: public surface + third-party audience = review; private delivery to the Launcher = feedback (neutral work)
- [ ] the engagement/fraud boundary: acting from one's OWN account on PUBLIC surfaces vs creating/handing-over/automating access
- [ ] each definition phrased as an LLM-judgable test (CJ-K3 prompt-compatible)

**P2 — Row dispositions.** *What value does each row get, with what rationale and what text seed?*
- [ ] engagement → ALLOW+DISCLOSE; rationale (founding use-case, risk-borne-by-Jumper mitigated by informed consent, reversibility)
- [ ] public reviews → GATE; rationale (law-floor: undisclosable material connection + sentiment-buying prohibition); honest decline text seed
- [ ] fraud-adjacent → map to EXISTING gates (K2/K3/verifiability), no new rule
- [ ] neutral → ALLOW, no warn
- [ ] unknown → WARN + LOG (`tos_category: unknown`); hold only via existing K3-uncertainty
- [ ] the determination mechanism named: CJ-K3's semantic judgment emits `tos_category`; registry maps category → severity + template

**P3 — The consequence map (the audit).** *What exposure does each disposition carry, for whom?*
- [ ] per-row × per-party grid: Jumper (account strikes/bans), Launcher (purge = wasted spend; refund question deferred), platform entity (tail legal: intermediary suits, C&D; positioning-sensitivity), ecosystem (the third human: signal pollution)
- [ ] enforcement-reality notes (purge waves; bans hit the acting account; intermediary suits target fakes/automation/loud branding)
- [ ] what the MVP infrastructure already absorbs (crypto rails, no app store)
- [ ] epistemic status banner: representative knowledge, jurisdiction undeclared, NOT counsel

**P4 — The honesty mechanism.** *What do the two disclosure surfaces say, and where do they live?*
- [ ] Launcher-facing card warn line (template seed: "⟨platform⟩'s rules prohibit paid engagement — purges can remove results; you're choosing this risk")
- [ ] Jumper-facing risk notice (template seed: "doing this may risk your ⟨platform⟩ account") + its HOME: task display surface (bot browse/task card + fe) — OUTSIDE the clarifier; cross-component requirement named, not built here
- [ ] the new warn-class detection entry candidate (catalog extension trigger: `CJ-C5 tos-sensitive` or similar — naming deferred to the catalog's own convention)
- [ ] disclosure ≠ legalese: one line each, Launcher-benefit phrasing per catalog card rules

**P5 — The wrappers.** *What system rules surround the matrix?*
- [ ] positioning principle: market and describe as verified-human digital work; never manipulation-for-hire language (the principle does tail-risk work)
- [ ] fail-open coupling rule: any GATED category must be acceptable-to-miss during fail-open at current scale, else fail-open → fail-hold; MVP assessment recorded
- [ ] revisit gates, each observable: counsel review completed · fiat on-ramp added · app-store submission · first platform contact (C&D = immediate) · scale threshold (e.g. >1k launches/mo)
- [ ] jurisdiction declaration named as user TODO bounding legal confidence

**P6 — Ratification & propagation.** *How is the decision presented, ratified, and propagated?*
- [ ] the values-residue presented honestly (the third-human tension; what this analysis resolved and what remains the user's)
- [ ] the ratification ask: one explicit question (adopt matrix v1 as-recommended / amend rows)
- [ ] staged consumer updates (post-ratification): CJ-K3 wording + few-shots (catalog v1.3) · clarifier registry per-category severities/templates (BOM §2 knob) · PROJECT.md Open Decisions ③ closed · meta-def open-parameter register ① closed · fail-open coupling note on BOM knob
- [ ] `tos_category` logging lands in the BOM's detection-record shape (one field)
- [ ] counsel/jurisdiction flags recorded as standing TODOs

## Step 5 — Interface Map

| From → To | What flows | Direction | Assumption check |
|---|---|---|---|
| P1 → P2 | row definitions + placement tests | one-way | P2 assumes tests are LLM-judgable as phrased (P1 criterion enforces) |
| P1 → P3 | the row set to map | one-way | — |
| P3 → P2 | per-row exposure evidence | one-way | P2's rationales must cite P3, not free-float (evidence-verdict link) |
| P2 → P4 | which rows carry warns + text seeds | one-way | P4 assumes engagement is the only warn-row at v1 (unknown-row shares the template) |
| P2 → P6 | dispositions → CJ-K3 wording implications | one-way | P6 assumes catalog versioning convention (v1.2 → v1.3 note) |
| P4 → P6 | new-entry candidate → catalog extension trigger | one-way | P6 routes it through the catalog's own extension convention, not ad-hoc |
| P5 → P6 | gates + coupling rule → register/knob text | one-way | revisit gates must be copied VERBATIM into registers (drift guard) |
| P4 → (cross-component) | Jumper notice home = task display | one-way flag | NOT this inquiry's to build; recorded as a requirement on the task-display surface |
| P6 → (user) | ratification ask | blocking | all propagation is GATED on the user's answer |

## Step 6 — Dependency Order

1. **P1** (definitions first — everything places against them)
2. **P3 ∥ P5** (evidence and wrappers are independent of dispositions)
3. **P2** (consumes P1 + P3)
4. **P4** (consumes P2's warn rows)
5. **P6** last (consumes all; blocked at its midpoint by user ratification — propagation stages behind the ask)

No cycles. P6's user-gate is a deliberate external dependency, not a defect.

## Step 7 — Self-Evaluation (full, 7 dimensions)

| Dimension | Verdict | Note |
|---|---|---|
| Independence | PASS | each piece answerable through stated flows; P3 standalone (the audit articulation's value) |
| Completeness | PASS | all four articulations land: decision-brief (P2+P6), parameter-setting (P6's default-pending-ratification), policy-line (P1+P2), risk-audit (P3); all SV6 wrappers in P5; MQ4 exclusions respected (no counsel substitution — P3 banner; no consumer edits mid-inquiry — P6 staging) |
| Reassembly | PASS | walk the acid task: P1 places it (engagement) → P3 prices it → P2 disposes it (allow+disclose) → P4 words the two lines → P5 wraps → P6 ratifies & propagates to CJ-K3/registry/registers — the parameter is decided, worded, and consumed |
| Tractability | PASS | each piece ≈ one focused pass |
| Interface clarity | PASS | assumptions column populated; one cross-component flag (Jumper-notice home) named explicitly |
| Balance | PASS | P3 largest (grid + evidence) ≈ 2× smallest; tolerated |
| Confidence | HIGH | top-down and bottom-up agree; no disputed boundary |

**Determination-mechanism check:** the load-bearing runtime determination — "which row does a task fall in" — has an owning piece (P2 names the mechanism: CJ-K3 semantic judgment emits `tos_category`; registry maps category → severity/template; P1 supplies the judgable tests). Unknown-row default owned (P2). Ratification-state determination owned (P6: propagation explicitly staged behind the user's answer). No presupposed-but-unowned determination.

**Verdict: 7/7 PASS — the six pieces are the decision brief's section skeleton.**
