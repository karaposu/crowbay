# Surfacing — Crowdjump Task Meta-Definition

## User Input

`/Users/ns/Desktop/projects/crowboy/devdocs/inquiries/2026-06-12_10-43__crowdjump-task-meta-definition/_branch.md` — purpose and territory taken from the branch file (articulated framing: attribute-based meta-definition of "Crowdjump task"; ambiguities preserved across artifact-kind / normative-vs-descriptive / definedness-inclusion / consumer axes).

## Mode + Entry Point

- **Mode:** artifact (the territory holds pre-existing items: project docs, legacy specs, SVI design docs, live code, the wizard transcript). Candidate ATTRIBUTES themselves are not generated here — that belongs downstream; surfacing draws the constraint-sources and existing task-concept fragments.
- **Entry point:** signal-first (purpose given by `_branch.md`).
- **Territory:** explicit-bounded — the Crowdjump project workspace, six regions: R1 PROJECT.md; R2 legacy generation (old_md/, depricated_src/ spec fragments); R3 SemanticVideoInspector docs (verification capability envelope); R4 live src/ task surface; R5 the inquiry's source input (wizard transcript + seed attributes); R6 cross-cutting policy/economics docs.
- **Boundary-discovery sub-phase:** skipped (explicit-bounded).
- **Prior-workspace:** supplied by runner — this session previously read the full repo; traversal re-attends from in-context content under THIS purpose; no re-reads were needed.

## Traversal Trace

| # | Region | Item identifier | Relevance | Conf | Recency annotation | Note |
|---|---|---|---|---|---|---|
| 1 | R1 | PROJECT.md `## How It Works` loop (Launch→Jump→Perform→Verify→Pay) | core | HIGH | {filesystem, 2026-06-12T07:30:15Z} | a task must be performable+verifiable+payable inside this loop |
| 2 | R1 | PROJECT.md `## The Idea` three-verifications framing (verified work) | core | HIGH | {filesystem, 2026-06-12T07:30:15Z} | "verified work" presupposes task-verifiability |
| 3 | R1 | PROJECT.md `## Open Decisions` #3 MVP task categories / ToS posture | core | HIGH | {filesystem, 2026-06-12T07:30:15Z} | legality/permissibility dimension is an OPEN decision |
| 4 | R1 | PROJECT.md roles + terminology tables | sub | HIGH | {filesystem, 2026-06-12T07:30:15Z} | Launcher/Jumper/Launch/Jump vocabulary |
| 5 | R2 | old_md/known_requirements.md "Task specification" field list | core | HIGH | {filesystem, 2025-08-04T12:42:45Z} | proto-attribute set: desired action, target platform/URL, budget, participants, timeline, filters |
| 6 | R2 | old_md/known_requirements.md AI-verification bullets (performed / correct profile / required actions / time spent) | core | HIGH | {filesystem, 2025-08-04T12:42:45Z} | verifiability decomposed into observable checks |
| 7 | R2 | depricated_src/api_spec.yaml CreateTaskRequest `operation_requirements` (e.g. "must find the profile via search bar") | core | HIGH | {filesystem, 2025-08-04T12:18:43Z} | embryo of operational-specification attribute |
| 8 | R2 | depricated_src/.../user_repository.py "korkuluk" docstring (`example_validation_video`, per_crow_budget, num_of_crows) | sub | MEDIUM | {filesystem, 2025-03-04T00:01:38Z} | example-validation-video = definedness-relevant artifact idea |
| 9 | R2 | depricated_src/assets/task_example.yaml ("share crowbay with your 3 friend; requirements: must exist chat history...") | sub | MEDIUM | {filesystem, 2025-04-18T20:37:44Z} | historical example of requirement phrasing |
| 10 | R2 | notes_to_not_forget.txt (differential rates; manual validation) | side | LOW | {filesystem, 2025-04-19T11:17:45Z} | pricing/curation, not task-ness |
| 11 | R3 | SVI known_requirements "Task Verification Capabilities" taxonomy (social, form, content creation, navigation, engagement-with-duration, transaction) | core | HIGH | {filesystem, 2025-08-25T12:16:34Z} | the checkable-task taxonomy — concretizes "recordable/verifiable" |
| 12 | R3 | SVI 04_task_specification_language.md (structured task definition; "without clear, unambiguous task definitions, the system cannot reliably determine completion") | core | HIGH | {filesystem, 2025-08-25T13:01:50Z} | in-project prior art for definedness |
| 13 | R3 | SVI 01a_event_expectation_scripts.md (tasks decompose into expected observable event sequences with variations) | sub | HIGH | {filesystem, 2025-08-25T13:26:10Z} | defined task ⇒ expected-events derivable |
| 14 | R3 | SVI VideoQuery.md inputs (`queries`: what to look for) | sub | MEDIUM | {filesystem, 2025-08-25T18:00:27Z} | verification needs enumerable look-fors |
| 15 | R3 | SVI philosophy.md (alternative valid paths; verify completion not surveil) | sub | MEDIUM | {filesystem, 2025-08-25T12:15:44Z} | definition must tolerate path variation |
| 16 | R4 | src/schemas/task.py TaskCreate (desc = free text 1–5000 chars; budget guard; filters; operation_requirements passthrough) | core | HIGH | {filesystem, 2026-06-12T09:55:11Z} | current contract: NOTHING constrains task-ness beyond money math |
| 17 | R4 | src/bot/flows/launch.py step 1 (desc collected verbatim, no clarification) | core | HIGH | {filesystem, 2026-06-12T10:04:39Z} | the gap's code location |
| 18 | R4 | src/services/tasks.py launch_task / jump lifecycle | sub | MEDIUM | {filesystem, 2026-06-12T09:54:04Z} | task lifecycle states a definition must survive |
| 19 | R4 | devdocs/filter_design.md (audience targeting) | side | MEDIUM | {filesystem, 2026-06-12T07:32:28Z} | who performs, orthogonal to what a task is |
| 20 | R5 | Seed attributes from user: achievable / recordable-via-screen-recording / digital | core | HIGH | {none, null} | the given seeds |
| 21 | R5 | Live instance: task #2 "check my instagram page and like photos to give me a boost" | core | HIGH | {none, null} | test instance: vague goal ("a boost"), no target URL, no per-Jumper action spec, no completion criterion |
| 22 | R5 | Deferred-consumer framing: "AI based data consumer which shows tasks relevant ambiguities + confirmation text" | sub | HIGH | {none, null} | consumer constraint on definition shape |
| 23 | R5 | Example definedness question: "goal is clear?" | sub | HIGH | {none, null} | seed of the derived-question form |
| 24 | R6 | Session policy flag: paid engagement vs target-platform ToS (PROJECT.md Open Decisions; earlier session analysis) | core | HIGH | {none, null} | permissibility attribute source |
| 25 | R6 | Escrow/pricing shape (you_earn per Jumper × N) | sub | MEDIUM | {none, null} | task as per-Jumper-uniform, priceable unit |
| 26 | R6 | Trust score / dispute docs | side | LOW | {none, null} | post-task quality, not task-ness |

## State Summary

- **Territory echo:** Crowdjump workspace, regions R1–R6 as specified above.
- **Purpose echo:** surface everything bearing on an attribute-based meta-definition of "Crowdjump task" (per `_branch.md`, all four articulation variants kept live).
- **Coverage map:** R1 confirmed (core density high) · R2 confirmed (legacy fragments captured) · R3 confirmed (capability envelope captured) · R4 confirmed (current-contract gap captured) · R5 confirmed (seeds + test instance) · R6 scanned-but-shallow (policy/economics touched at the level this purpose needs).
- **Confirmed-absent regions:** `fe/` web client (UI mirror only — no definitional content); payments/wallet remnants (nothing on task-ness beyond item 25); matching notification internals (delivery plumbing, not task concept).
- **Concept-names list:**
  - {name: "operation_requirements", type: vocabulary, provenance: 7, gloss: per-task operational constraints field, already in schema}
  - {name: "Task Specification Language", type: structural-reference, provenance: 12, gloss: SVI's structured task-definition prior art}
  - {name: "event expectation script", type: vocabulary, provenance: 13, gloss: expected observable event sequence per task}
  - {name: "example_validation_video", type: coined-term, provenance: 8, gloss: legacy idea — Launcher supplies an example proof}
  - {name: "task verification capabilities taxonomy", type: structural-reference, provenance: 11, gloss: SVI's checkable task types}
  - {name: "three verifications", type: vocabulary, provenance: 2, gloss: verified humans / attributes / work}
- **Recency distribution:** R1 {newest 2026-06-12, oldest 2026-06-12, no-mtime 0/4-ish} · R2 {newest 2025-08-04, oldest 2025-03-04, no-mtime 1(notes counted with mtime), total 6} · R3 {newest 2025-08-25, oldest 2025-08-25, total 5} · R4 {newest 2026-06-12, oldest 2026-06-12, total 4} · R5 {no-mtime 4/4} · R6 {no-mtime 3/3}. Descriptive only; no relevance weight taken from mtimes (legacy 2025 items carry core tags where content warrants).
- **Frontier flags:**
  - Candidate-attribute generation (the actual attribute set) is deliberately NOT surfaced — it is downstream Innovation work over these sources.
  - The ToS/permissibility posture (item 3/24) is an open product decision the definition will have to either absorb or parameterize — flagged for Sensemaking.
  - SVI's Task Specification Language (item 12) overlaps the inquiry so strongly it may function as a competing prior design — flagged for Sensemaking to position it (adopt / supersede / ignore).
- **Workspace-populated status:** {populated: true, populated-at: 2026-06-12T10:49Z, extent: R1–R6 at listed coverage; all core/sub items' full content resident in session context from prior reads}

## Telemetry

- Mode: artifact · entry: signal-first · boundary-discovery: skipped
- Cycles: 6 (one per region) · items enumerated: 26 · tags: core 12 / sub 9 / side 4 / umbrella 0 (umbrella unneeded — warm context gave HIGH/MED confidence throughout; one LOW-confidence side item retained per inclusion bias)
- items_with_mtime: 15 · items_without_mtime: 11 (in-session/conceptual items)
- Workspace-overload trigger: not fired (no new reads required; traversal from warm workspace)
- Convergence: territory exhausted at current resolution; uncertain items included; rejections only HIGH-confidence (out-of-territory plumbing)
- Failure modes checked: Missed-relevance, Surfaced-irrelevance, Over-coverage, Territory-mis-binding, Workspace-overload, Artifact-under-specification, Workspace-artifact-desync, Recency-Equates-Idleness, Recency-Bias-Filter — none fired

## Self-Assessment

**PROCEED** — convergence criteria met; three frontier flags handed to Sensemaking (attribute generation reserved for Innovation; ToS posture decision; SVI Task Specification Language positioning).
