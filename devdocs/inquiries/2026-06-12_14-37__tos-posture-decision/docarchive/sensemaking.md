# Sensemaking — ToS-Posture Decision

## User Input

/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_14-37__tos-posture-decision/_branch.md

## SV1 — Baseline Understanding

Pick a stance — allow or forbid paid-engagement tasks, probably some middle option with warnings — and write it down so the catalog's policy-floor entry (CJ-K3) can finalize its wording.

## Phase 1 — Cognitive Anchor Extraction

**Constraints**
- C1: The canon floor is FIXED: illegal / harmful / deceptive-presented-as-genuine stays gated under every posture (meta-definition `policy-permissible`; catalog CJ-K3 core). The decision governs only the residual: **lawful + non-deceptive + ToS-breaching** tasks.
- C2: Named consumers wait on the output: CJ-K3 wording + few-shots, hold semantics, the clarifier BOM's fail-open production stance, PROJECT.md Open Decisions ③, the meta-definition's open-parameter register ①.
- C3: Not legal advice; no jurisdiction declared anywhere in the project; no counsel artifacts exist.
- C4: MVP infrastructure already shapes exposure: crypto rails (processor acceptable-use bypassed), Telegram + web (no app-store review), unfunded dev escrow, tiny scale.
- C5: Authority: the route record itself says "a product call, not a design task" — final ratification is the user's.
- C6: Philosophy commitments (`old_md/philosophy.md` §5): no fake personas · real people doing real tasks · "building genuine digital presence, not artificial inflation" · performer freedom-of-choice.

**Key Insights**
- KI1: **The category set is not uniform — the legal line cuts inside it.** Real-human engagement (likes/follows/views) breaches platform ToS but is mostly lawful. Incentivized PUBLIC reviews are regulated territory (FTC 2024 review rule, EU UCPD: sentiment-buying prohibited; material-connection disclosure mandatory). Fake-persona/bot engagement is illegal-adjacent AND already gated. Platform-neutral work (testing, translation, forms) has no issue. A single binary knob misdescribes reality; the parameter is naturally a **category matrix**.
- KI2: **The founding-use-case overlap:** forbidding the contested category doesn't trim demand — it deletes the founding pitch (the original project description's task list LEADS with engagement). A posture that kills the founding use-case is a pivot decision, which exceeds this inquiry's authority.
- KI3: **Risk asymmetry:** routine enforcement cost (purges, strikes, bans) lands on the Jumper's account — not on the platform, not on the Launcher. Philosophy's freedom-of-choice plus the protect-jumpers motivation converge on **disclosure (informed consent)**, not prohibition, as the mechanism.
- KI4: **Tail risk is positioning-sensitive:** intermediaries get sued when they use fakes (NY AG v. Devumi — bots; already gated here), brand themselves as manipulation-for-hire, or scale loudly. Real-human microtask marketplaces in this niche have operated openly for years. Marketing language ("verified humans for digital work" vs "boost your metrics") does as much risk work as mechanics.
- KI5: **Reviews are the genuinely dangerous category.** A paid public review cannot be made compliant by task design: the review platform offers no disclosure surface, and buying reviews "expressing a particular sentiment" is prohibited outright. This category sits AT or OVER the legal floor — it is a law line hiding inside the ToS question. ("Honest review, any stars" does not cure the undisclosed-incentive problem.)
- KI6: **Posture × fail-open are coupled dials.** Category detection is an LLM judgment; during fail-open (LLM down ⇒ code-only checks) any gated category passes silently. The stricter the posture, the less acceptable fail-open is. Rule needed, not just a value.
- KI7: **Disclosure has two cheap surfaces:** Launcher-facing (card warn line: "this breaches ⟨platform⟩'s ToS; engagement may be purged") and Jumper-facing (task-display risk notice: "performing this may risk your ⟨platform⟩ account"). Neither exists in canon yet — a new warn-class detection entry + a task-display field; extension-trigger material, cheap.
- KI8: **MVP posture ≠ permanent policy.** At MVP (tiny, Telegram, crypto, pre-counsel) permissive-with-disclosure is low-cost and reversible. The calculus shifts at: counsel review, fiat on-ramp, app-store entry, scale, or first platform contact (C&D). These are the revisit gates.
- KI9: No jurisdiction is declared anywhere — the operator entity's location materially changes the legal read. Bounds confidence; doesn't block an MVP posture.

**Structural Points**
- SP1: Parameter shape: per-category rows × {allow · allow+warn · hold · gate} + a default-for-unknown row.
- SP2: Consumers: CJ-K3 gate text + few-shots · new ToS-warn entry candidate · hold semantics · fail-open coupling rule · PROJECT.md + meta-def registers · BOM knobs.
- SP3: Authority split: the inquiry structures and recommends; the user ratifies; consumers update post-ratification.

**Foundational Principles**
- FP1: The deception gate is immovable.
- FP2: Definedness ≠ truth; the consumer judges intent semantically — posture changes the ROUTING of the contested category, never the detection.
- FP3: **Whatever is allowed must be allowed openly** — warn lines, disclosure, honest positioning. Philosophy §5 and tail-risk analysis point the same direction: quiet permissiveness is the worst quadrant.

**Meaning-Nodes:** the contested category · the policy line (matrix) · informed consent · positioning language · revisit gates.

## SV2 — Anchor-Informed Understanding

Not "pick a knob value." The question decomposes into: (1) the parameter's SHAPE (binary vs matrix — and the law-inside-ToS discovery forces matrix), (2) per-category VALUES (where engagement and reviews must diverge), (3) the MECHANISM (two-sided disclosure), (4) the COUPLING rule (fail-open), (5) the AUTHORITY protocol (recommend vs commit), (6) revisit GATES. The founding docs lean allow-by-identity but are internally torn at exactly the contested point — the decision resolves a tear the philosophy itself couldn't.

*Meta-inspection (H4/H5): "the contested category" is validated as the project's own framing (PROJECT.md: "paid engagement violates most target platforms' ToS"); the acid task is an instance of the pattern, and the matrix addresses the pattern (specific-vs-pattern cue honored).*

## Phase 2 — Perspective Checking

- **Technical/Logical:** the matrix is implementable today — CJ-K3's semantic-intent judgment already categorizes; add a `tos_category` output + per-category severity in the clarifier registry. ~0.5 day on the BOM. New anchor: implementation is NOT a differentiator between postures; all are cheap.
- **Human/User — three humans, not two:** Launchers (want boosts; an honest purge-risk warning beats silent wasted spend) · Jumpers (bear the account risk — informed choice requires the risk notice BEFORE accepting) · **the third human: end-consumers of the boosted signals** (the people whose feeds and review pages get shaped). Restrictive postures protect the third human; philosophy's "not artificial inflation" speaks for them. New anchor: the ethical residue is a real values call, not a risk calculation.
- **Strategic/Long-term:** positioning decides tail risk (KI4) and door-openness (app stores, partnerships, acquirers). "Verified-human digital-work marketplace that permits some gray tasks with disclosure" keeps doors open; "boost marketplace" closes them. Path dependence: if engagement dominates early revenue, identity ossifies around it. New anchor: the positioning principle belongs IN the decision, not beside it.
- **Risk/Failure:** worst realistic outcomes — allow-all-silent: Jumper ban wave + "bot farm with humans" press + platform legal letter, all unannounced. Forbid-all: demand evaporates; project dies politely. Allow+disclose matrix: purge waves still happen but informed; Launcher refund question surfaces (deferred); operator hold load bounded. The failure asymmetry favors graded-with-honesty.
- **Resource/Feasibility:** all postures feasible; matrix costs two warn templates + one registry field + one task-display notice. Not a deciding axis.
- **Ethical/Systemic:** the externality argument (paid signals degrade the commons) vs counters (paid visibility is ALREADY the legal norm — ads, influencer marketing; Crowdjump's variant uses real humans who may freely decline). The philosophy text does not resolve engagement-without-belief vs real-people-real-tasks; the decision must — and should SAY it is resolving it, not pretend the tension away. New anchor: A2's verdict carries an explicit values-residue flag for the user.
- **Phase/Calibration-State:** REQUIRED here — the posture is phase-dependent by nature. MVP default + named revisit gates (counsel · fiat rails · app-store entry · first platform contact/C&D · scale threshold) rather than a permanent stance.
- **Definitional/Internal Consistency:** a permissive matrix does NOT contradict canon (the dial was left open by design — meta-def register ①). It PARTIALLY contradicts philosophy §5's "not artificial inflation" while satisfying its "real people, real tasks, freedom of choice" — the philosophy is internally torn; the decision resolves the tear explicitly (and the finding should quote both halves).

## SV3 — Multi-Perspective Understanding

The "ToS posture" is a **published category policy plus an honesty mechanism plus revisit gates** — not one dial. The pipeline-relevant discoveries: reviews ≠ engagement (law vs ToS); disclosure is the mechanism that reconciles demand-reality with Jumper protection; positioning language is part of the policy; the ethical residue is the user's, explicitly. Six decision points now visible (shape, row values, mechanism, coupling, authority, gates).

## Phase 3 — Ambiguity Collapse

#### A1: Parameter shape — binary knob vs category matrix
**Counter (binary):** canon §8 says "posture", singular; one line; simplest.
**Why it fails (structural):** KI1/KI5 — the legal line cuts inside the category set. A binary ALLOW also admits incentivized public reviews (regulated/prohibited territory); a binary FORBID needlessly kills lawful engagement along with them. No single value is simultaneously honest about both categories.
**Confidence:** HIGH. **Resolution:** the parameter is a **category matrix** (rows below) + default-for-unknown. **Fixed:** matrix shape; registry carries per-category severity. **Excluded:** single-valued posture.

#### A2: Engagement row (likes, follows, subscribes, views, profile visits — real humans, no claims made) — allow+disclose vs allow-silent vs gate
**Counter (gate):** philosophy's "not artificial inflation"; the third human's feeds; cleanest conscience.
**Why gate loses AT MVP:** it deletes the founding use-case (KI2) — a pivot decision above this inquiry's authority; the MVP risk profile is small, Jumper-borne, and mitigable by disclosure (KI3); it is reversible via revisit gates while the inverse (launching restrictive, going permissive later) wins nothing now.
**Counter (allow-silent):** zero friction, max conversion.
**Why silent loses:** it transfers account risk to Jumpers uninformed (violates philosophy's freedom-of-choice premise — choice requires information); and quiet permissiveness is the highest-tail-risk quadrant (KI4: loud-and-dishonest is what draws suits and press).
**Confidence:** HIGH as recommendation — **with an explicit values-residue flag: the "artificial inflation" tension is resolved toward real-human-informed-consent by THIS analysis; the user may weigh the third human differently, and ratification is the place to do it.**
**Resolution:** **allow + two-sided disclosure** (Launcher card warn: ToS-breach/purge risk; Jumper task-display notice: account risk). **Fixed:** the disclosure mechanism (new warn-class entry + task-display field). **Excluded:** silent allowance; MVP gate.

#### A3: Reviews row (public reviews/ratings on stores, maps, marketplaces — incentivized)
**Counter (treat like engagement — allow+warn):** same "contested category", real humans, honest opinions permitted ("any stars you want").
**Why it fails:** KI5 — compliance is impossible by task design: the review surface carries no disclosure field, and paid-for-sentiment is prohibited outright (FTC 2024 rule; UCPD blacklist). This row sits at/over the LEGAL floor — it is not a taste decision. "Honest review" framing doesn't cure the undisclosed material connection the reading consumer never sees.
**Confidence:** HIGH. **Resolution:** **gate at MVP** — CJ-K3 gains an explicit sub-rule: incentivized public reviews decline with an honest reason ("paid public reviews can't carry the legally required disclosure"). **Carve-out (stays allowed):** private feedback to the Launcher ("test my app and send ME your impressions") — that is platform-neutral work, not a public review. **Fixed:** the engagement/reviews divergence; the carve-out line (public-surface vs private-feedback). **Excluded:** review tasks at warn severity.

#### A4: The remaining rows
**Counter (leave unlisted categories to runtime judgment):** the LLM judges intent anyway.
**Why partial:** unlisted ≠ unconsidered — the matrix must place the foreseeable rows or the registry templates can't be written. **Resolution (rows enumerated):** **fraud-adjacent mechanics** (account creation for handover, captcha farming, login-walled scraping) → already gated by existing canon (self-contained K2 / policy K3 / verifiability) — the matrix MAPS them, adds nothing new. **Platform-neutral digital work** (testing, translation, forms, research) → allow, no warn. **View/listen farming** (watch/stream minutes) → engagement row's treatment (allow+disclose). **Confidence:** MED-HIGH. **Fixed:** row inventory v1. **Excluded:** inventing new gates beyond canon for these rows.

#### A5: Default-for-unknown — when the consumer can't place a ToS-sensitive task
**Counter (hold everything uncertain):** safest.
**Why it fails:** operator load at MVP is one person; holds must stay rare (canon already reserves hold for policy-floor uncertainty). **Resolution:** default = **warn + log** (`tos_category: unknown` recorded — calibration data for matrix v2); escalation to hold only under the EXISTING K3-uncertainty rule. **Confidence:** MED (revisit at calibration). **Fixed:** unknown-row semantics.

#### A6: The fail-open coupling
**Counter (ignore — fail-open was already accepted):** the BOM committed visible fail-open.
**Why refinement is needed anyway:** the acceptance was made before the posture existed; the rule must be explicit: **any category at GATE must be acceptable-to-miss during fail-open at current scale, else fail-open degrades to fail-hold.** At MVP under this matrix: gates are law-floor categories (reviews, fraud-adjacent) whose fail-open miss risk equals the pre-existing K3 residual — acceptable at dev scale with operator eyeballs, re-evaluated at the BOM's existing revisit gate.
**Confidence:** MED-HIGH. **Resolution:** the coupling rule is recorded next to the fail-open knob. **Fixed:** posture and degradation are formally coupled.

#### A7: Decision authority — commit the parameter vs recommend-and-ratify
**Counter (commit now, articulation 2):** "lets do this dive deep" + momentum; ratification friction.
**Why it fails:** the route record's own caveat ("a product call, not a design task") is the user's prior words about authority; A2 carries a genuine values residue (the third human) that analysis cannot own; ratification costs one message.
**Confidence:** HIGH. **Resolution:** **decision-brief with a committed-by-default recommendation** — the finding presents the matrix as the recommended parameter; canon consumers (CJ-K3 wording, registry templates, registers) update AFTER the user ratifies (gated next-actions). Articulation 2 is absorbed as "default pending ratification," not killed.

*(Load-bearing concept tests: "the contested category" — project's own framing, confirmed against PROJECT.md verbatim; "category matrix" — proxy check: rows are structurally distinct by LEGAL regime, not by convenience labels; determination mechanism specified (LLM tos_category judgment + registry severity). Specific-vs-pattern: acid task = instance; matrix = pattern; honored.)*

## SV4 — Clarified Understanding

The posture is a five-row published policy: engagement allowed with two-sided disclosure · public incentivized reviews gated (law, not taste) with a private-feedback carve-out · fraud-adjacent mapped to existing gates · neutral work untouched · unknown warned-and-logged. Plus three wrappers: the positioning principle (market it as verified-human work, never manipulation-for-hire), the fail-open coupling rule, and revisit gates (counsel · fiat · app store · platform contact · scale). Authority: recommend now, user ratifies, consumers update after. No longer viable: binary knob, forbid-all, allow-all-silent, reviews-at-warn, commit-without-ratification.

## Phase 4 — Degrees-of-Freedom Reduction

**Fixed:** matrix shape + row inventory v1 + row values (as A2–A5) · disclosure mechanism (Launcher warn line + Jumper task-display notice; new warn-class entry) · positioning principle · fail-open coupling rule · revisit gates · recommend-then-ratify protocol · consumers-update plan (CJ-K3 wording, registry, PROJECT.md, meta-def register, BOM knob — all post-ratification).
**Eliminated:** P0 forbid-all (pivot, not posture) · P1 allow-all-silent (uninformed risk transfer; worst tail quadrant) · P4 per-platform allowlist (empty in practice — founding platforms all hostile) · P5 defer/neutral-launch (delays the viability question the MVP exists to answer) · binary parameter · review tasks at warn.
**Remaining open (named, carried):** jurisdiction declaration (user TODO; bounds legal confidence) · counsel review (gate) · Launcher refund policy on purge waves (deferred to payments component) · matrix v2 calibration (unknown-row log data).

## SV5 — Constrained Understanding

The solution space is one artifact away: a decision brief presenting the five-row matrix + mechanism + wrappers as the recommended parameter, with ratification as the explicit next step and the consumer-update plan staged behind it. Everything else (templates, registry fields, register edits) is mechanical once ratified.

## Phase 5 / SV6 — Stabilized Model

**The "ToS posture" resolves into a published category policy with an honesty mechanism, recommended for MVP and revisit-gated:**

1. **Engagement** (likes/follows/subs/views/visits by real, freely-choosing humans, no claims made): **ALLOW + two-sided disclosure** — Launcher card warn (ToS breach, purge risk) + Jumper task-display risk notice (account risk).
2. **Public incentivized reviews**: **GATE** (law-floor: undisclosable material connection + sentiment-buying prohibition); honest decline text; **carve-out:** private feedback to the Launcher remains allowed (platform-neutral work).
3. **Fraud-adjacent mechanics** (account handover, captcha farming, login-walled scraping): already gated by existing canon (K2/K3/verifiability) — mapped, not new.
4. **Platform-neutral digital work**: allow, no warn.
5. **Unknown ToS-sensitive**: warn + log (`tos_category: unknown` = matrix-v2 calibration data); hold only under the existing K3-uncertainty rule.

Wrappers: **positioning principle** (verified-human digital work; never manipulation-for-hire language) · **fail-open coupling rule** (gated categories must be acceptable-to-miss during fail-open at current scale, else fail-hold) · **revisit gates** (counsel review · fiat on-ramp · app-store entry · first platform contact/C&D · scale threshold). Authority: **recommended now; the user ratifies; the named canon consumers update after ratification.** The values residue (the "third human" / "artificial inflation" tension) is explicitly the user's call at ratification — this analysis resolves it toward informed-consent permissiveness and says so rather than hiding it.

**Delta from SV1:** SV1 wanted a knob value. SV6 discovered the knob is a matrix because LAW cuts inside the supposedly-uniform category; found the mechanism (two-sided disclosure) that reconciles the founding pitch with Jumper protection; split reviews from engagement on structural legal grounds; coupled the posture to the fail-open dial; and split authority honestly (analysis recommends, user ratifies).

**Ambiguity ledger:** 7 collapsed (6 HIGH, 1 MED) · OPEN carried: jurisdiction, counsel, refund policy, matrix-v2 calibration.

## Saturation Telemetry

- Perspective saturation: reached — Resource and Definitional confirmed rather than added; Ethical and Legal were the last to add anchor types (values residue; law-inside-ToS).
- Ambiguity ratio: 7/7 collapsed; 4 OPEN explicitly carried.
- SV delta: substantial (knob → matrix + mechanism + wrappers + authority protocol).
- Anchor diversity: all five types; eight perspectives; sources span founding docs, today's canon, and representative external knowledge.
- Failure modes scanned: Status Quo (no prior commitment existed to defend — confirmed-absent), Premature Stabilization (three perspectives produced genuine surprises: third human, law-split, positioning-as-policy), Anchor Dominance (founding-pitch anchor ruled AGAINST on the reviews row — not dominating), Clean Resolution Trap (A2 deliberately preserves the values residue instead of dissolving it; counters stated with structural grounds throughout), Perspective Blindness (the uncomfortable perspective — ethical/externality — was checked and shaped the verdict), Self-Reference (n/a — target is a product policy).
