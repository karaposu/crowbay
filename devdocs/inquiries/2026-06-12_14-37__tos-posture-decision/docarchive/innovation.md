# Innovation — ToS-Posture Decision

## User Input

/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_14-37__tos-posture-decision/_branch.md
(operating on sensemaking SV6's 5-row matrix + mechanism + wrappers, and decomposition P1–P6)

## Seed & Methodology Mode

**Seed (constraint+question):** SV6 committed a 5-row category policy with disclosure and wrappers; what design content fills the pieces, what's missing from the matrix, and do the load-bearing dispositions survive deliberate challenge?

**Mode:** (a) inherited: **Standard default** (the branch asks for a decision artifact; no weighting signals). (b) Alternative: Contrarian-rethink (Framer-weighted). (c) Under it the run would re-litigate sensemaking's A2/A3 wholesale — but those carry tested counters already, and the Inherited Frame Audit below forces explicit challenges regardless. (d) **Decision: default**, audit-backed.

**Production-task classification:** P2 (dispositions — evaluation criteria), P5 (wrappers — framing), P6 (ratification — framing) are meta-decision pieces → piece-level Inversions mandatory. P1/P3/P4 content-production.

## Phase 2 — Generate (7 × 3)

### Lens Shifting (Framer)
- *Generic — the platform's-eye lens:* what makes Instagram see Crowdjump as "manipulation-for-hire" vs "a microtask marketplace with disclosed gray inventory"? Not the mechanics — the PRESENTATION. → **V-L1: a public "what we allow and why" policy page** — the matrix itself, published. Transparency as positioning armor; the policy IS marketing.
- *Focused — the Jumper's-eye lens:* a bare "may risk your account" notice reads as liability-shifting, not informed consent. Real consent matures with risk-RATE data. → **V-L2: notice v1 = honest minimum + collect ban/purge reports** to make notice v2 quantitative.
- *Contrarian — the regulator's-eye lens:* under FTC/DSA eyes the matrix splits correctly — a paid like deceives no consumer the way a paid review does; the engagement/reviews divergence is exactly where a regulator would draw it. CONFIRMS sensemaking's A3 from independent ground (convergence, not novelty).

### Combination (Generator)
- *Generic:* matrix + the existing filter system → **V-C1: ToS-risk as a Jumper-side preference** — "don't show me account-risk tasks" (one attribute + a feed filter clause; reuses matching). Disclosure becomes agency.
- *Focused:* matrix + profile → **V-C2: one-time profile-level risk acknowledgment** (opt-in bool) instead of a per-task nag — the per-task notice stays visible, but acceptance is asked ONCE.
- *Contrarian:* matrix + pricing → risk-priced pay floors (account-risk tasks must pay ≥ X). Tested: paternalistic, unenforceable without market data, fights the philosophy's market-pricing principle. KILL → seed (revisit with real pay/fill data).

### Inversion (Framer)
- *Generic (P2 engagement row — piece-level, mandatory):* "allow+disclose is right" → "gate engagement at MVP." Depth-iterated to system level: gating the founding category is not a posture value — **it is a company-pivot decision** (the demand test the MVP exists to run never runs). Killed AS POSTURE; survives as a REQUIREMENT on P6: the ratification ask must present the engagement row as an identity choice, not a config default.
- *Focused (P2 reviews row — piece-level):* "reviews must be gated" → "allow reviews WITH forced in-review disclosure ('I was paid to evaluate this')." What follows: review platforms purge disclosed-paid reviews anyway (incentivized = banned regardless of disclosure); disclosure makes purge-targeting trivial; a visibly-paid review persuades nobody, so Launcher value ≈ 0. KILLED on three independent grounds — the reviews gate emerges STRONGER (the strongest pro-allow variant was constructed and still died).
- *Contrarian (P6 — piece-level):* "ratification is one yes/no" → **"ratification is PER-ROW"** — the user may adopt engagement, tighten unknown, amend gates independently. SURVIVES: the ask becomes a short per-row checklist; cheap, strictly more honest about authority.

### Constraint Manipulation (Framer — both directions)
- *ADD (generic):* "EVERY run carries `tos_category`, not just warn-rows" → **V-CM1: full-coverage category logging** — matrix-v2 evidence accrues from day one (clear rows included).
- *ADD (focused):* a per-category volume cap (circuit-breaker while evidence accumulates). Tested: arbitrary threshold, signals self-distrust, partially redundant with the kill-switch (below). **DEFER** — revival: first purge wave.
- *REMOVE (contrarian):* remove the "MVP" qualifier — make the posture permanent. Kills the reversibility that justified the allow verdict (sensemaking A2 leaned on revisit gates). KILLED — confirms the gates are load-bearing, not decoration.

### Absence Recognition (Generator — patch + redesign, bidirectional)
- *Patch (what the 5-row matrix MISSES — two real catches):*
  - **V-A1: unsolicited-contact/spam row** ("DM 50 people my promo", mass comments-with-links): platform ToS + anti-spam law adjacency (CAN-SPAM/ePrivacy-class) + third-party harm (recipients) → **GATE**. Not derivable from any existing row.
  - **V-A2: political/coordinated-engagement row** (paid engagement on political/advocacy content): coordinated-inauthentic-behavior territory, election-law adjacency, reputational tail far above commercial engagement → **HOLD at minimum** (operator look), plausibly gate.
- *Patch (minor):* age/region-sensitive surfaces (engagement on adult/gambling content) — interacts with existing filters; a registry condition, not a row.
- *Redesign (what's missing if designed from scratch):* **V-A3: incident semantics** — nothing says what happens on the first purge wave or C&D. → per-category **kill-switch flag** in the registry (config flip = instant gate for that row) + a one-paragraph incident playbook (pause row → notify affected Launchers/Jumpers → refund stance pointer → revisit gate fires).
- *Redesign (already-present-in-different-form):* the warn-line muscle already exists (matching's raw-location "advisory with warning on the confirmation card"); the Jumper notice is the same pattern on the task card. Feasibility confirmed; nothing new.

### Domain Transfer (Generator — native source included)
- *Native (marketplace governance — eBay/Etsy prohibited-items model):* published category policy + user reporting + graduated enforcement. Imports: the public policy page (= V-L1, second ground) and **V-D1: a report-task affordance** — Jumpers flag a task that feels wrong → routes to the EXISTING hold/operator queue (one button + one status; no new infra).
- *Different field (brokerage risk-disclosure):* standardized risk statements + suitability opt-in for complex products → confirms V-C2 (one-time opt-in) and adds: the risk text is REGISTRY-OWNED boilerplate, never per-task improvisation (consistency is what makes warnings legible).
- *Different field (tobacco/alcohol labeling):* warnings work via consistency + unavoidability → the Jumper notice must sit IN the task card at a fixed position, not behind a link. Placement rule for P4.

### Extrapolation (Generator)
- *Generic:* platform AI detection improves → real-human paid engagement becomes pattern-detectable (behavior graphs); purge rates rise; the engagement category has a **half-life**. → **V-E1: wire a purge-report-rate metric into the revisit gates** ("reported purge/ban rate > X% → engagement row re-opens").
- *Focused:* the regulatory trend (FTC 2024 → EU DSA → UK DMCC) expands paid-signal regulation → the reviews gate ages well; engagement may migrate toward regulated; monitoring + gates already absorb this. Confirms architecture.
- *Contrarian:* platforms increasingly SELL boosts themselves (ads, creator marketplaces) → the gray space may become licensable (official creator-task APIs, whitelisted partnerships). RESEARCH FRONTIER — no MVP change, recorded.

## Inherited Frame Audit

- **Seed central assumption** — "MVP allows real-human engagement (allow+disclose)": explicitly challenged by the P2 generic inversion (gate-at-MVP), killed at system level WITH a surviving requirement (ratification presents it as identity choice). Satisfied.
- **P2 reviews-gate commitment**: challenged by the strongest pro-allow construction (forced in-review disclosure) — killed on three grounds. Satisfied.
- **P5 positioning principle**: challenged — invert to "lean into boost-marketplace branding" (maximize demand). Killed: it maximizes exactly the tail risk (intermediary suits target loud manipulation branding) and closes app-store/partnership doors for a marketing phrasing the demand doesn't need. Principle confirmed.
- **P6 recommend-then-ratify**: challenged (commit-now inversion absorbed at sensemaking; per-row refinement generated here). Satisfied.
- **Audit verdict:** every load-bearing commitment carries an explicit tested challenge; no overrides needed.

## Phase 3 — Test

| # | Candidate | Novel | Scrutiny (strongest objection → outcome) | Fertile | Actionable | Mech-indep | Disposition → piece |
|---|---|---|---|---|---|---|---|
| T1 | public policy page (V-L1) | ✓ | "publishing the gray list invites platform attention" → survives: platforms find marketplaces via their own telemetry, not your docs; honesty differentiates intermediary-suit targets from disclosed marketplaces; it's ALSO the Launcher-education surface | ✓✓ | ✓ (one md page at MVP) | lens + transfer + absence | **ACTIONABLE → P5/P6** |
| T2 | Jumper risk-preference filter (V-C1) | ✓ | "over-engineering at MVP" → survives: one verified-attribute-style boolean + one feed clause; reuses matching wholesale | ✓ | ✓ | combination + Jumper-lens | **ACTIONABLE → P4** |
| T3 | one-time profile risk opt-in (V-C2) | ✓ | "an ack wall depresses Jumper supply" → survives: asked once, only on first risk-task encounter; the alternative (per-task nag) erodes the warning's meaning | ✓ | ✓ | combination + brokerage transfer (2 grounds) | **ACTIONABLE → P4** |
| T4 | per-row ratification checklist | ✓ | none that holds (strictly more honest, ~6 lines) | – | ✓ | P6 inversion | **ACTIONABLE → P6** |
| T5 | full-coverage `tos_category` logging (V-CM1) | ✓ | "log bloat" → trivial: one enum per run | ✓ (matrix v2) | ✓ | constraint + extrapolation | **ACTIONABLE → P2/P6** |
| T6 | spam/unsolicited-contact row → GATE (V-A1) | ✓ | "K3 harassment already covers it" → survives partially-: mass-DM promo is not harassment per se; the row is genuinely missing; law-adjacency + recipient harm justify gate | ✓ | ✓ | absence (patch) | **ACTIONABLE → P1/P2 (matrix +1 row)** |
| T7 | political/coordinated-engagement row → HOLD (V-A2) | ✓ | "rare at MVP; why pre-build" → survives: the cost is one registry row; the tail (election-cycle CIB story) is the project's worst headline | ✓ | ✓ | absence (patch) | **ACTIONABLE → P1/P2 (matrix +1 row)** |
| T8 | per-category kill-switch + incident playbook (V-A3) | ✓ | "YAGNI" → survives: the switch is a config read the registry already does; the playbook is one paragraph; first-incident improvisation is how marketplaces die | ✓✓ | ✓ | absence (redesign) | **ACTIONABLE → P5** |
| T9 | report-task affordance (V-D1) | ✓ | "operator can't absorb reports" → survives at MVP volume: reports route to the EXISTING hold queue; cap reports per user | ✓ | ✓ | transfer (native) | **ACTIONABLE → P4/P5** |
| T10 | purge-rate metric wired to revisit gates (V-E1) | ✓ | "no data source yet" → REFINED: source = Jumper ban-report button (pairs with V-L2) + Launcher purge complaints; the gate text names the metric, collection starts simple | ✓ | ✓ | extrapolation + Jumper-lens (V-L2 pairing) | **ACTIONABLE (refined) → P5** |
| T11 | risk-priced pay floors | ✓ | paternalistic + fights market-pricing principle + no data | – | ✗ now | single | **KILL → seed** (revisit with pay/fill data) |
| T12 | per-category volume cap | ✓ | arbitrary + self-distrust signal + redundant w/ T8 | – | partial | single | **DEFER** — revival: first purge wave |
| T13 | disclosed-paid public reviews | ✓ | killed on 3 grounds (platforms purge disclosed too; targeting trivial; persuades nobody) | seed value: names the non-product | – | inversion | **KILLED** (strengthens reviews gate) |
| T14 | permanent posture (no MVP qualifier) | – | kills the reversibility the allow verdict leans on | – | – | constraint-REMOVE | **KILLED** (gates confirmed load-bearing) |
| T15 | boost-marketplace branding | – | maximizes tail risk for zero demand gain | – | – | P5 inversion | **KILLED** (positioning confirmed) |

**RE-TEST TRIGGER scan:** T6/T7 add rows to a committed structure (the 5-row matrix) → re-test the matrix claim: "5 rows" becomes **7 rows**; no disposition of the original five changes; sensemaking's A4 row-inventory was explicitly "v1 … foreseeable rows" — extension is in-frame, not contradiction. T10's refinement updates V-L2's pairing only.

**Artifact-grounding:** claims checked — matching's advisory-warning precedent exists (`devdocs/scoped/be/matching/list.md` header) ✓; hold queue exists in BOM §6 ✓; verified-attribute filter mechanics exist (`services/matching.py`, attributes) ✓; registry/config seam exists (BOM §2) ✓.

## Assembly Check

- **The governance layer (emergent):** T1 (public policy page) + T8 (kill-switch + playbook) + T9 (report affordance) + T10 (purge-rate gate) compose into something none is alone: **the posture ships as an operated policy, not a config value** — published, monitorable, reversible per-row, with an incident path. This reframes the deliverable: matrix + governance loop.
- **The Jumper-agency pair (emergent):** T2 (risk filter) + T3 (one-time opt-in) together convert disclosure from a warning INTO a preference system — Jumpers who opt out never see risk tasks; Jumpers who opt in stop being nagged. Philosophy's freedom-of-choice realized mechanically.
- **Matrix v1 final shape:** 7 rows (engagement · public reviews · fraud-adjacent · neutral · unknown · spam/unsolicited-contact · political/coordinated).
- **Axis coverage:** rows (T6/T7) · mechanism (T2/T3) · governance (T1/T8/T9/T10) · economics (T11/T12 killed/deferred — axis examined) · authority (T4) · logging (T5). No axis without a variant.
- **Per-piece trace:** P1: T6/T7 rows + boundary tests · P2: piece-inversions ×2 + T5 · P3: T10's evidence loop · P4: T2/T3 + placement rule · P5: T1/T8/T9/T10 + positioning inversion · P6: T4 + identity-choice requirement. All pieces show mechanism trace.

## Telemetry

- Generators: 4/4 · Framers: 3/3
- Convergence: YES — public policy page (3 mechanisms), one-time opt-in (2), purge-monitoring (2), reviews-gate (regulator lens + inversion kill, 2 independent grounds)
- Survivors tested: 15/15 (10 ACTIONABLE, 1 DEFER, 4 KILL w/ grounds + 1 frontier)
- Piece classification: P2/P5/P6 meta-decision (Inversion compliance: **satisfied** — P2 ×2 axes, P5, P6); P1/P3/P4 content-production
- Failure modes: none observed (the uncomfortable challenges — gate-the-founding-category, allow-disclosed-reviews — were constructed at full strength and killed on grounds, not comfort)
- **Overall: PROCEED**
