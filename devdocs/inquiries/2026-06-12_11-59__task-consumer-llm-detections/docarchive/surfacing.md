# Surfacing — Task-Consumer LLM Detections & Scenarios

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_11-59__task-consumer-llm-detections/_branch.md` — purpose: surface everything bearing on the consumer LLM's detection/scenario catalog (all four articulation variants live; behavior commitments: rewrite-and-approve, enforce-via-suggestions).

## Mode + Entry Point

- **Mode:** artifact (the constraint sources and detection precedents pre-exist: the meta-definition, live code surfaces, in-project clarification prior art). Candidate DETECTIONS themselves are downstream Innovation work; surfacing draws their sources.
- **Entry point:** signal-first. **Territory:** explicit-bounded, six regions below. **Boundary-discovery:** skipped.
- **Prior-workspace:** supplied by runner — same-session continuity; the meta-definition inquiry's outputs and the full codebase are in context. Zero new reads required.

## Traversal Trace

| # | Region | Item identifier | Relevance | Conf | Recency annotation | Note |
|---|---|---|---|---|---|---|
| 1 | R1 meta-definition | The 11 attribute triples (definition/test/question) in devdocs/task_meta_definition.md | core | HIGH | {filesystem, 2026-06-12T11:16:19Z} | each triple IS a detection seed: test=trigger, question=response |
| 2 | R1 | Enforcement flags (gate vs clarify, axis defaults) | core | HIGH | {filesystem, 2026-06-12T11:16:19Z} | detections inherit response posture from flags |
| 3 | R1 | Task normal form ("[Do action(s)] on [target] until [end-state]…") | core | HIGH | {filesystem, 2026-06-12T11:16:19Z} | rewrite-proposal target: the LLM's "non-ambiguous understanding" renders INTO this form |
| 4 | R1 | Clarification order (goal→target→actions→completion; then feasibility trio) | core | HIGH | {filesystem, 2026-06-12T11:16:19Z} | detection firing order |
| 5 | R1 | Sufficiency rule + over-constraint warning (path tolerance) | core | HIGH | {filesystem, 2026-06-12T11:16:19Z} | implies an OVER-specification detection, not only under- |
| 6 | R1 | Definedness ≠ truth handoff (tests read text, not world) | core | HIGH | {filesystem, 2026-06-12T11:16:19Z} | bounds what the consumer may claim; implies a "can't-verify-truth" disclosure scenario |
| 7 | R1 | Stranger-Jumper summary test | sub | HIGH | {filesystem, 2026-06-12T11:16:19Z} | the consumer's self-check on its own rewrite |
| 8 | R1 | Field-backed attributes note (economics/audience/timing excluded from questions) | core | HIGH | {filesystem, 2026-06-12T11:16:19Z} | negative space: detections the LLM must NOT duplicate |
| 9 | R1 | Open parameters (ToS posture; capability envelope) | core | HIGH | {filesystem, 2026-06-12T11:16:19Z} | policy detection must be posture-parameterized; verifiability detection envelope-bound |
| 10 | R1 | Acid test (task #2 fails I1–I4; repaired version) | sub | HIGH | {filesystem, 2026-06-12T11:15:01Z} | the canonical under-specified scenario + its repair |
| 11 | R1 | Binding pair (actions+completion bind and freeze) | sub | HIGH | {filesystem, 2026-06-12T11:16:19Z} | consumer must surface the freeze consequence at confirm time |
| 12 | R2 code surfaces | Bot launch FSM steps + validations (budget guard re-ask with max-affordable hint) | core | HIGH | {filesystem, 2026-06-12T10:04:39Z} | existing DETERMINISTIC detections — the LLM layer sits beside them, mustn't duplicate |
| 13 | R2 | Audience-preview warnings (raw-location advisory on confirm card) | core | HIGH | {filesystem, 2026-06-12T10:03:34Z} | live proto-detection precedent: warn-on-card pattern |
| 14 | R2 | matching `unmet_requirements()` / parse warnings (unknown region) | sub | HIGH | {filesystem, 2026-06-12T10:04:39Z} | unmet-list shape; location free-text already produces warnings the consumer could consume |
| 15 | R2 | TaskCreate schema constraints (desc 1–5000, budget guard, filters JSON) | sub | MEDIUM | {filesystem, 2026-06-12T10:03:34Z} | the submission object the consumer reads |
| 16 | R3 prior art | articulate_simple discipline (identify-don't-interpret; typed ambiguity axes; restate-then-variant pattern) | core | HIGH | {none, null} | in-project methodology analogue for "clarify with own non-ambiguous understanding + approval" |
| 17 | R3 | SVI Task Specification Language + event expectation scripts | sub | MEDIUM | {none, null} | structured-task target the consumer's output could feed |
| 18 | R3 | Confirm-card pattern (wizard step 6: restate + Launch/StartOver/Cancel) | core | HIGH | {filesystem, 2026-06-12T10:04:39Z} | the approval-gate UX already exists; consumer extends it |
| 19 | R4 statement | Rewrite-and-approve commitment ("its own non ambigious understanding and ask for approval") | core | HIGH | {none, null} | behavior contract: propose, never silently apply |
| 20 | R4 | Enforce-with-suggestions commitment + non-unit example (atomicity detection → suggest singular part) | core | HIGH | {none, null} | anchor detection instance; "suggest back" response shape |
| 21 | R4 | "LLM detects this term" — named detections as vocabulary | sub | MEDIUM | {none, null} | detections should carry stable names (telemetry/eval) |
| 22 | R5 UX constraints | Interaction budget / abandonment risk (one confirm card, few questions; bot flood guard culture) | core | HIGH | {none, null} | caps questions-per-pass; favors batch-clarify over interrogation |
| 23 | R5 | FP2 Jumper-clarity + teaching-not-rejecting strategy anchor | sub | HIGH | {none, null} | tone of suggestions |
| 24 | R6 cross-cutting | Prohibited-category floor vs ToS posture split | core | HIGH | {none, null} | two different policy detections: floor (hard) vs posture (parameterized) |
| 25 | R6 | Injection/abuse surface (task desc is untrusted text fed to an LLM) | core | MEDIUM | {none, null} | a detection class the meta-definition never needed: prompt-injection/manipulative submissions |
| 26 | R6 | Multilingual submissions (Launchers won't all write English) | sub | MEDIUM | {none, null} | consumption-time reality the catalog must at least name |

## State Summary

- **Territory echo:** R1 canonical meta-definition (+finding) · R2 consumption-time code surfaces · R3 in-project clarification prior art · R4 the statement's behavioral commitments · R5 Launcher-UX constraints · R6 cross-cutting policy/safety.
- **Purpose echo:** sources for the consumer LLM's detection + scenario catalog, per `_branch.md` (all four variants live).
- **Coverage map:** R1 confirmed (the dominant core-density region) · R2 confirmed · R3 confirmed · R4 confirmed · R5 scanned-but-shallow (budget numbers unmeasured — flagged) · R6 scanned-but-shallow (injection surface named, not explored).
- **Confirmed-absent regions:** verification/payment internals (MQ4-excluded); fe/ web client (mirror of bot, no new constraints); notification plumbing.
- **Concept-names list:**
  - {name: "detection", type: vocabulary, provenance: 19/20, gloss: named trigger+response unit the consumer runs}
  - {name: "non-unit task", type: coined-term, provenance: 20, gloss: user's name for atomicity violation}
  - {name: "warn-on-card pattern", type: structural-reference, provenance: 13, gloss: existing precedent — surface findings on the confirm card}
  - {name: "rewrite-and-approve", type: vocabulary, provenance: 19, gloss: propose repaired task, gate on Launcher approval}
  - {name: "field-backed negative space", type: structural-reference, provenance: 8, gloss: attributes the LLM must NOT re-ask}
  - {name: "injection surface", type: vocabulary, provenance: 25, gloss: task desc as untrusted LLM input}
- **Recency distribution:** R1 {newest 2026-06-12T11:16, oldest 11:15, no-mtime 0/11} · R2 {2026-06-12T10:03–10:04, 0/4} · R3 {1 file-backed, 2 no-mtime} · R4–R6 {no-mtime 8/8}. Descriptive only.
- **Frontier flags:**
  - Candidate detections/scenarios themselves → Innovation (deliberately not generated here).
  - Interaction-budget numbers (how many questions before abandonment) — unmeasurable pre-launch; flag for Sensemaking to set a stance default.
  - Injection/manipulation detection class (item 25) — outside the meta-definition's attribute space; Sensemaking must decide whether it belongs in THIS catalog or a security layer.
- **Workspace-populated status:** {populated: true, populated-at: 2026-06-12T12:04Z, extent: R1–R6 at listed coverage; all core item content resident from same-session work}

## Telemetry

- Mode: artifact · entry: signal-first · boundary-discovery: skipped
- Cycles: 6 · items: 26 · tags: core 16 / sub 9 / side 1→0 (none demoted to side; one MEDIUM-confidence core retained per inclusion bias — item 25) / umbrella 0
- items_with_mtime: 15 · items_without_mtime: 11
- Workspace-overload: not fired (zero new reads)
- Convergence: regions exhausted at current resolution; uncertain items included (25, 26 at MEDIUM); HIGH-confidence rejections only (excluded regions)
- Failure modes checked: all 7 LAYER 1 + recency modes — none fired

## Self-Assessment

**PROCEED** — three frontier flags handed to Sensemaking (interaction-budget stance; injection-class placement; detection generation reserved for Innovation).
