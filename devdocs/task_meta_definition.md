# filepath: devdocs/task_meta_definition.md

# Crowdjump Task — Meta-Definition

> **Status:** canonical, v1 (2026-06-12). Derived in
> `devdocs/inquiries/2026-06-12_10-43__crowdjump-task-meta-definition/finding.md`
> (full reasoning, killed alternatives, open questions there).
> Consumers: the AI clarification pipeline (future), the launch gate, product
> vocabulary, the verification component, dispute resolution.

**A Crowdjump task is a digital, self-contained, policy-permissible, verifiable
unit of work** (the admissible KIND) **whose submission names a clear goal, an
identified target, the per-Jumper actions, and an on-screen completion
criterion, and is performable, bounded, and atomic** (the defined INSTANCE).

Normative: this states what *qualifies*, not what currently exists.
Meaning-layer: this document defines; schemas and pipelines implement later.

## Form of every attribute

Each attribute is a **triple** — definition · satisfaction test · clarifying
question — plus an optional example violation and an **enforcement flag**:

- **gate** (kind-axis default): failure means the task is not admissible; the
  rejection text says why.
- **clarify** (instance-axis default): failure fires the attribute's question
  back to the Launcher — confirm or fix, never silent rejection.

Flag changes and new attributes require a version note (see Evolution).

**Tests read the submission, not the world.** "Does the text name a target
URL?" is definitional; whether that URL exists is the verification component's
job at submission time. Definedness ≠ truth — say this to Launchers explicitly.

## Axis 1 — Admissible kind (gate)

| Attribute | Definition | Satisfaction test | Example violation |
|---|---|---|---|
| **digital** | Work happens entirely on internet-connected devices/services | Does the described work occur on-screen, on digital platforms? | "hand out flyers downtown" |
| **self-contained** | Performable by an ordinary verified Jumper using only their own accounts/devices, on public surfaces — no credential transfer, no Launcher-account access | Does it require someone else's login or non-public access? | "log into my account and clean my inbox" |
| **policy-permissible** | Lawful, non-harmful floor; **ToS posture = matrix v1, ratified 2026-06-12** (engagement allowed+disclosed; public reviews/spam gated; political held — see task_consumer_catalog.md v1.3 CJ-K3/CJ-C5) | Does the work fall into a prohibited category (illegal, harassment, deception targeting individuals, incentivized public reviews, spam-at-scale, …)? | "post a review claiming you bought it" |
| **verifiable-in-principle** | This kind of work produces completion observable via the platform's approved evidence channel — **currently screen recording; capability-versioned** against the verification design | Could completion of this sort of work be visible within a recording session? | "make my song famous" |

## Axis 2 — Defined instance (clarify), in clarification order

| # | Attribute | Definition | Clarifying question |
|---|---|---|---|
| 1 | **goal-clear** | Intent stated well enough to disambiguate everything below | "What outcome do you want from this task?" |
| 2 | **target-identified** | Exact object named (URL, handle, app screen) | "Which exact page/profile/app should Jumpers open? Paste the link or handle." |
| 3 | **actions-specified** | Per-Jumper actions enumerated | "What exactly should each Jumper do, step by step?" |
| 4 | **completion-criterion-observable** | An on-screen end state is named | "What will be visible on the Jumper's screen when the task is complete?" |
| 5 | **performable** | An ordinary verified Jumper can do it with own accounts/skills | "Does this need any special account, skill, or access beyond your audience filters?" |
| 6 | **bounded** | Finite; completable in one recording session | "Can one Jumper finish this in a single sitting? Roughly how long?" |
| 7 | **atomic** | Exactly one uniform per-Jumper unit, identical across slots | "Is this the same single job for every Jumper? If not, split into separate tasks." |

**Summary criterion (the stranger-Jumper test):** an instance is defined iff a
stranger Jumper could perform it and prove it without asking a single question.

**The binding pair:** actions-specified + completion-criterion-observable are
what BINDS (the Jumper's obligation; a dispute's adjudication basis — not the
goal text) and what FREEZES (immutable once the first Jumper is active;
changing them = a new task version). Ask-order is goal-first; bindingness
belongs to the pair.

## The task normal form

> **"[Do action(s)] on [target] until [observable end-state], by any matching
> Jumper, within [bound]."**

Slots map to attributes 3, 2, 4, the audience filters, and 6. A task is
defined exactly when its submission renders into this sentence with no empty
slots. The form is the canonical **rendering** — Launchers write free text;
the clarifier maps text into the form and asks for the empty slots.

Worked examples: *"Open instagram.com/⟨handle⟩, like the 3 most recent photos,
until all 3 show a filled heart, in one session."* · *"Watch video V until the
player shows ≥30s elapsed."* · *"Complete fields A–C on form F and submit,
until the confirmation page is visible."*

## Definedness rule

- **Normative:** defined = all seven instance attributes satisfied (checklist).
- A graded score may exist internally (clarifier UX, analytics); numeric
  thresholds are unset until ≥100 real tasks exist to calibrate against.
- **Sufficiency, not maximization:** beyond all-satisfied, more constraint is
  worse — Jumpers may take alternative valid paths (path tolerance); the
  clarifier should warn against over-specification.

## Field-backed attributes (definitionally required, already enforced)

Economics (budget, per-Jumper pay, slots — incl. budget-covers-payouts),
audience (filters per `devdocs/filter_design.md`), timing (deadlines) are part
of every task but structurally collected by the wizard/schema. Excluded from
the clarifier's question set.

## Evolution

- **Extension:** adding an attribute = a full triple + version note. Flag
  change = version note.
- **Open-parameter register:** ① target-platform ToS posture — **RESOLVED
  2026-06-12** (matrix v1 ratified; carried by catalog v1.3 CJ-K3 + CJ-C5;
  revisit gates listed there) · ② capability envelope version (owned by the
  verification component, still open).
- **Feedback register (stub):** per-attribute "known misses," to be populated
  from clarifier failures and dispute outcomes once the clarifier ships.
  - digital: — · self-contained: — · policy-permissible: — ·
    verifiable-in-principle: — · goal-clear: — · target-identified: — ·
    actions-specified: — · completion-criterion-observable: — ·
    performable: — · bounded: — · atomic: —

## Implementation note (for the future clarifier/gate)

The natural check shape is `undefined_requirements(task) -> list[str]` — the
same unmet-list shape matching already uses (`services/matching.py`,
`unmet_requirements`). One mental model: gates return unmet lists.

## Seed provenance

| Original seed (user) | Landed as |
|---|---|
| digital | **digital** (unchanged) |
| recordable via screen recording | **verifiable-in-principle** (kind) + **completion-criterion-observable** (instance) — recordability alone discriminates nothing; observable completion is the structural core |
| achievable | **performable** + **bounded** — one word, two failure modes, two questions |
| "goal is clear?" | **goal-clear**'s question template, plus six siblings derived the same way |
