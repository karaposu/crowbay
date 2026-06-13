---
status: active
model: claude-fable-5
effort: max
---
# Finding: The ToS-Posture Decision

## Question

From `_branch.md`: **what is Crowdjump's stance toward tasks that are lawful and non-deceptive but breach the target platform's Terms of Service?** The contested category is the platform's own founding example — "like my 3 photos to give me a boost" is legal, honest, and prohibited by most platforms' inauthentic-engagement clauses. This is route 5 of the task-consumer inquiry's route-map and Open Decision ③ in PROJECT.md; the catalog's policy-floor entry (CJ-K3), the clarifier registry's templates, and the fail-open production stance all wait on it. The route record's own caveat bounds authority: "it is a product call, not a design task" — so this finding RECOMMENDS and the user RATIFIES. Excluded by construction: legal advice (no counsel, no declared jurisdiction), re-opening the deception gate (fraud stays gated under every posture), clause-level ToS exegesis.

## Finding Summary

- **The "posture" is not one dial — it is a published 7-row category policy.** The legal line cuts INSIDE the supposedly-uniform category: real-human engagement is ToS-breaching but mostly lawful; incentivized public reviews sit at/over the legal floor (undisclosable material connection + sentiment-buying prohibitions); fakes were never on the table. A binary allow/forbid misdescribes reality.
- **Recommended matrix (one screen, below):** engagement ALLOW with two-sided disclosure · public incentivized reviews GATE (with a private-feedback repair path) · spam/unsolicited contact GATE · political/coordinated engagement HOLD · fraud-adjacent mechanics already gated by existing canon · platform-neutral work ALLOW · unknown WARN+LOG.
- **The honesty mechanism makes the allow defensible:** a Launcher-facing card warn line (purge risk, ToS conflict) and a Jumper-facing task-card risk notice (account risk), plus a one-time active opt-in acknowledgment and an optional "hide risk tasks" feed filter — informed consent and structural avoidance, not a buried banner.
- **The posture ships as an operated policy, not a config value:** a public "what we allow and why" page, a per-row kill-switch in the clarifier registry, a one-paragraph incident playbook, a Jumper report-task affordance, and a purge-rate metric wired into the revisit gates.
- **Five revisit gates make the stance reversible and observable:** counsel review · fiat on-ramp · app-store entry · first platform contact (a C&D triggers immediate re-decision) · reported purge/ban rate exceeding threshold.
- **The values residue is yours, stated plainly:** your own philosophy says both "real people doing real tasks" and "genuine digital presence, not artificial inflation." Paid real-human engagement satisfies the first and strains the second. This analysis resolves the tension toward informed-consent permissiveness at MVP scale; the engagement row's ratification is where you accept or override that.
- **Ratification is per-row, not yes/no** — a one-screen checklist closes the decision; the five canon consumers update mechanically afterward.
- The strongest challengers were built at full strength and killed on grounds: gating engagement (it is a company pivot, not a posture value — the founding pitch leads with this category), allowing reviews with forced in-review disclosure (platforms purge disclosed-paid content anyway; targeting becomes trivial; a visibly-paid review persuades nobody), silent allowance (uninformed risk transfer to Jumpers; the highest-tail-risk quadrant).

## Finding

### 1. The recommended matrix (parameter v1, pending your ratification)

| # | Category (boundary test) | Disposition | Ground |
|---|---|---|---|
| 1 | **Engagement** — real-human actions from the Jumper's OWN account on PUBLIC surfaces, no claims made (likes, follows, subscribes, views, profile visits, watch-time) | **ALLOW + two-sided disclosure** | lawful; founding use-case; risk borne by informed, freely-choosing Jumpers; fully reversible via kill-switch + gates |
| 2 | **Public incentivized reviews** — content presented to third parties as opinion on a review surface (store ratings, map reviews, marketplace reviews) | **GATE** (decline + repair path: "want this as a private-feedback task instead?") | law-floor, not taste: the review surface carries no disclosure field (undisclosed material connection) and buying sentiment is prohibited outright; the strongest pro-allow variant (forced in-review disclosure) fails three ways |
| 3 | **Spam / unsolicited contact** — unsolicited + commercial + scale (mass DMs, comment-link blasts at strangers) | **GATE** | platform ToS + anti-spam-law adjacency + third-party harm (recipients); small-N personal recommendation to existing contacts is row 1, not spam |
| 4 | **Political / coordinated engagement** — paid engagement on political, electoral, or advocacy content | **HOLD** (operator look) | coordinated-inauthentic-behavior territory; definitional swamp where human judgment beats both gate and warn; worst-headline tail |
| 5 | **Fraud-adjacent mechanics** — account creation/handover, captcha farming, login-walled scraping | already **GATED** by existing canon (self-containment, policy floor, verifiability) | mapped, not new |
| 6 | **Platform-neutral digital work** — testing, translation, forms, research, private feedback | **ALLOW**, no warn | no conflict exists |
| 7 | **Unknown ToS-sensitive** — the consumer can't place a gray task | **WARN + LOG** (`tos_category: unknown`); hold only via the existing policy-uncertainty rule | calibration data for matrix v2; operator load stays bounded |

Placement is a runtime judgment the task-consumer LLM already makes (CJ-K3's semantic-intent reading); the clarifier registry maps `tos_category → severity + template`. Every run logs its category — clear rows included — so matrix v2 is an evidence revision, not a guess.

### 2. The ratification checklist (the one decision you make)

> **Row 1 — engagement: this is an identity choice, not a config.** Your philosophy says both: *"Real people doing real tasks"* and *"Building genuine digital presence, not artificial inflation."* Paid real-human engagement is the first AND arguably the second. Platforms will treat it as inauthentic; routine enforcement lands on Jumpers' accounts (mitigated by the notices, the ack, and the filter); the commons sees purchased signals (the "third human"). Adopting row 1 = running the founding demand test with eyes open. Rejecting row 1 = pivoting Crowdjump to a neutral-work marketplace — a different company.
>
> - [ ] Row 1 engagement: ALLOW+disclose — adopt / amend
> - [ ] Row 2 public reviews: GATE w/ repair path — adopt / amend
> - [ ] Row 3 spam: GATE — adopt / amend
> - [ ] Row 4 political: HOLD — adopt / amend
> - [ ] Rows 5–7 (mapped / neutral / unknown): adopt / amend
> - [ ] Sub-item: Jumper feed default = **show-risk-tasks-with-notice** (recommended; "hide by default" protects harder but may zero MVP engagement supply) — adopt / flip
> - [ ] Wrappers (positioning principle · kill-switch + playbook · revisit gates · policy page): adopt / amend

### 3. The honesty mechanism (what makes row 1 defensible)

Launcher-side, on the clarifier card: *"⟨platform⟩'s rules prohibit paid engagement — purges can remove results; you're choosing this risk."* Jumper-side, on the task card at a fixed position: *"Doing this may risk your ⟨platform⟩ account."* Both lines are registry-owned boilerplate (consistency is what keeps warnings legible), one line each. A Jumper accepts a one-time acknowledgment naming the concrete consequence on first risk-task acceptance (re-shown after 90 days dormant), and can set "don't show me account-risk tasks" as a feed preference. Disclosure becomes agency: the notice informs, the ack commits, the filter avoids.

### 4. The governance layer (the posture as an operated policy)

- **Public policy page:** the matrix published as "what we allow and why" — platform-rule conflict stated honestly, the Launcher's risk ownership explicit, zero encouragement language. Transparency is positioning armor: it is what distinguishes a disclosed marketplace from manipulation-for-hire in exactly the cases that matter.
- **Per-row kill-switch:** a registry flag flips any row to gate instantly — config, no deploy.
- **Incident playbook (one paragraph):** on purge wave or platform contact — flip the row's switch, notify affected Launchers and Jumpers, point at the refund-stance decision (payments component owns it), fire the revisit gate.
- **Report affordance:** Jumpers can flag a task that feels wrong; reports route to the existing operator hold queue, capped per user.
- **Positioning principle:** Crowdjump markets itself as a verified-human digital-work marketplace, never in boost/manipulation language — the principle does tail-risk work no gate can.

### 5. The consequence map (who bears what, per the recommended values)

| Party | Exposure under matrix v1 | Mitigation |
|---|---|---|
| Jumper | account strikes/bans on the acting platform (the routine cost) | notice + active ack + feed filter + ban-report loop |
| Launcher | purged engagement = wasted spend | card warn line; refund stance deferred to payments component |
| Crowdjump entity | tail: intermediary suits, C&D, press framing | fakes prohibited (canon); honesty mechanism; positioning principle; kill-switch + playbook; counsel gate before production |
| The ecosystem ("the third human") | purchased signals in feeds/metrics | the values residue — resolved at ratification, monitored via policy page honesty |

**Epistemic banner:** the legal claims here are representative training knowledge (FTC 2024 review rule scope, platform-policy categories, EU UCPD direction), NOT verified-current and NOT counsel. The risky categories sit at gate/hold — the conservative side — precisely because of this. The lifts are named: a web currency-check before production, counsel review at its gate.

### 6. What changes where, once you ratify

| Consumer | Update |
|---|---|
| `devdocs/task_consumer_catalog.md` (CJ-K3) | final wording + few-shots per row; reviews decline gains the repair-path text; version note v1.2 → v1.3 |
| Clarifier registry (BOM §2) | per-category severities + templates + `tos_category` enum + per-row kill-switch flags |
| `PROJECT.md` Open Decisions ③ | closed with the matrix + a pointer here |
| `task_meta_definition.md` open-parameter register ① | closed (posture decided; capability envelope ② remains) |
| Clarifier BOM fail-open knob | gains the coupling rule: any GATED row must be acceptable-to-miss during fail-open at current scale, else fail-open degrades to fail-hold (at MVP: acceptable — gated rows are law-floor categories whose miss-risk equals the pre-existing residual) |

## Next Actions

### MUST
- **What:** Ratify the matrix (the §2 checklist — per-row, ~30 seconds)
  **Who:** user · **Gate:** on reading this finding · **Why:** every consumer below is staged behind it; the engagement row is an identity choice only you can make
- **What:** Execute the consumer-propagation plan (§6: catalog v1.3, registry spec, PROJECT.md, meta-def register, BOM knob)
  **Who:** AI session · **Gate:** immediately after ratification · **Why:** unblocks CJ-K3 wording and the clarifier build's policy templates
  **Depends-on:** MUST item "Ratify the matrix". GATED — no propagation before the user's answer.

### COULD
- **What:** Draft the public policy page (one md page, the matrix in public language)
  **Who:** AI session · **Gate:** with or right after propagation · **Why:** transparency armor + Launcher education
  **Depends-on:** MUST item "Ratify the matrix". GATED.
- **What:** Web currency-check of the FTC review-rule scope + 2–3 platform policy pages
  **Who:** AI session (web) · **Gate:** before production launch (or on request) · **Why:** lifts the representative-knowledge quarantine short of counsel
- **What:** Declare the operating entity's jurisdiction
  **Who:** user · **Gate:** before counsel engagement · **Why:** every legal read sharpens or shifts with it

### DEFERRED
- **What:** Counsel review of matrix + policy page — **Gate:** before fiat on-ramp / app-store entry — **Why (if revived):** the full quarantine lift; production legitimacy
- **What:** Refund-on-purge stance — **Gate:** payments/escrow component design — **Why:** the Launcher-side cost of purge waves needs a money-owner
- **What:** Volume-cap circuit breaker — **Gate:** first purge wave — **Why:** blast-radius limiter if the kill-switch proves too binary
- **What:** Risk-priced pay floors — **Gate:** real pay/fill-rate data — **Why:** market signal beats paternalism only with data
- **What:** Matrix v2 — **Gate:** meaningful `tos_category` log volume (≥100 gray-row runs) — **Why:** rows become evidence, not judgment

## Reasoning

- **Why a matrix, not a knob:** the inquiry's central discovery is that LAW cuts inside the "ToS-violating" category. A single ALLOW admits incentivized public reviews (regulated/prohibited territory); a single FORBID kills lawful engagement along with them. No one value is honest about both. The binary framing canon inherited ("posture", singular) was the only casualty of this inquiry — and canon anticipated it by leaving the parameter open.
- **Why engagement survives (with bindings):** the prosecution was given everything — the philosophy's own "not artificial inflation" line, the third-human externality, the detection half-life. The defense held on: lawfulness; the founding demand test (the original project description's task list LEADS with engagement — gating it is a pivot, which exceeds an analysis's authority); epsilon marginal commons-harm at MVP scale; full reversibility; and the honesty mechanism converting risk transfer into informed choice. The survival is CONDITIONAL: the four wrappers are constitutive, and the ratification text must carry the philosophy's tension verbatim — both conditions implemented above.
- **Why reviews die (and stay dead):** the strongest pro-allow variant — force "I was paid" disclosure into the review text — was constructed and killed on three independent grounds: platforms purge disclosed-paid reviews anyway; disclosure makes purge-targeting trivial; a visibly-paid review persuades nobody, so Launcher value ≈ 0. The repair path (private-feedback tasks) preserves the demand's legitimate kernel and answers the "reviews were in the founding pitch too" prosecution.
- **Why two rows were missing:** innovation's absence pass caught spam/unsolicited-contact (mass-DM promos are not harassment per canon's existing few-shots, yet clearly gate-worthy: anti-spam law adjacency + recipient harm) and political/coordinated engagement (CIB territory; hold, because a definitional swamp needs a human, not a rule).
- **Why silent allowance and boost-branding die:** quiet permissiveness transfers account risk to uninformed Jumpers (the philosophy's freedom-of-choice premise requires information) and occupies the highest-tail-risk quadrant — enforcement history targets loud manipulation branding and fakes, not disclosed real-human marketplaces.
- **Why recommend-then-ratify:** the route record's own words ("a product call, not a design task"); the values residue is genuinely the user's; and per-row ratification (an innovation refinement) is strictly more honest than a yes/no — the user can adopt engagement and still tighten any other row.
- **Why permanent-posture and no-TTL-of-the-decision die:** the allow verdict leans on reversibility; removing the revisit gates removes the verdict's own ground.
- Inheritance note: this finding operates the meta-definition and catalog v1.2 as canon (the deception gate, the hold semantics, the severity vocabulary) and re-tests none of them; what it adds is the value of a parameter canon deliberately left open. The frame-premise "representative legal knowledge suffices for an MVP posture" is mitigated structurally: the legally-risky rows sit conservative (gate/hold), and the lifts (currency check, counsel) are scheduled, not vague.

## Open Questions

### Monitoring
- Unknown-row rate: if >20% of gray tasks land `tos_category: unknown`, the boundary tests need sharpening (matrix v2 trigger).
- Purge/ban-report rate once real: the engagement row's revisit gate reads this number.
- Hold-queue volume from the political row: if it's >a handful/month at MVP, the row needs few-shot tightening rather than operator absorption.

### Blocked
- Final CJ-K3 wording: blocked on ratification (the MUST above).
- Jurisdiction-sharpened legal read: blocked on the user declaring the operating entity's jurisdiction.
- Production-stance confirmation: blocked on counsel review at its gate.

### Research Frontiers
- Licensed-boost partnerships: platforms increasingly sell official boosts (ads, creator marketplaces); an official-API lane would convert gray inventory to licensed inventory and restructure the matrix.

### Refinement Triggers
- A C&D or platform legal contact: immediate re-decision of the contacted row (playbook fires).
- Reported purge/ban rate > threshold (set at first data): engagement row re-opens.
- FTC/DSA scope expansion reaching real-human paid engagement: row 1 migrates toward row 2's treatment (the currency-check + counsel gates exist to catch this).

## Source Input

<details>
<summary>Raw user input for this finding</summary>

```text
lets do this dive deep 

the ToS-posture decision (open parameter)    project-space    teleological    INVESTIGATE-FRONTIER    HIGH

from /Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/docarchive/routelister.md
```

</details>
