# Writing-brief suggestions and upstream refresh

Your Voice now has an optional writing brief for recurring jobs: reader, output shape, required content, and exclusions. The refresh also adds focused preservation checks. These are scoped instructions, not a new universal persona or a claim of 2× better writing.

## Suggestions supplied by the reader

Source: the excerpts Paras supplied from Andrea Leewong’s discussion. The comments are practitioner suggestions, not controlled evidence of effectiveness.

| Suggestion | Decision | Implementation or reason |
|---|---|---|
| Luis Carballo: named roles with a job, audience, shape, and forbidden content | Adopt the mechanism | [Writing briefs](../references/writing-briefs.md) make selection explicit. A role is a reusable brief, not invented expertise or personality. |
| Action-only team messages: work, dates, next steps, no rationale or diagnosis | Scope to the requested job | Handoffs retain owners, dates, blockers, and dependencies. A later request for a decision or explanation still gets rationale. Missing assignments stay unknown. |
| Ray Wei: no em dashes; write like a human marketer | Keep as a possible user preference, not a universal rule | Honor an explicit punctuation preference. Punctuation does not establish authorship, quality, or a specific human voice. |
| Ana Dujmovic: generate, then shorten | Already covered; clarify the bounded workflow | Draft for the brief, make one final editorial review, and recheck meaning after cuts. Avoid mandatory multi-draft output or endless shortening. |
| Prompt 20% below the desired length | Do not adopt as a fixed rule | It is an unvalidated heuristic that may overcut. Count the finished artifact against the actual limit instead. |
| Use a sentence or paragraph shape | Adopt with verification | A concrete format helps specify the job; it is not a guarantee of compliance. |
| Set an output-token ceiling | Treat as a runtime bound, not an editorial method | Tokens are not words or characters, and a ceiling can truncate required material. No generator settings were changed. |
| Humans own the message and nuance | Retain writer ownership | Supplied or approved positioning governs adaptations. Do not infer approved messaging from a persona label. |
| Writer.com is superior; models cannot count | Do not promote these categorical claims | No comparative product evidence was supplied, and a blanket inability claim is unnecessary. Validate the actual output with a counter. This refresh is not a vendor comparison. |

## Repository sources

Seven credited writing/evaluation repositories were fetched and compared with their previously recorded revisions on 2026-09-22: five changed, two did not. Reviews focused on substantive writing instructions, relevant diffs, and licensing, not every upstream executable or benchmark. These repositories inform an original synthesis; they are not automatically inherited runtime dependencies.

| Source | Previously reviewed → reviewed now | Decision |
|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer/tree/9862685f575c65a8247f90369951df1b3416e3d6) | `e2e92e7b4b82` → `9862685f575c` | v3.0.0; adopt precise preservation of ranking and event timing; most pattern guidance already covered. Correct the Siqi Chen credit. |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop/tree/8da1f030185bdfe8471220585162991eaeb970e9) | `8da1f030185b` → `8da1f030185b` | Unchanged. Keep existing minimum-effective-editing influence; no new rules. |
| [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop/tree/000650b156983f5159695b441477f4e63b25dc85) | `d30eddb9e045` → `000650b15698` | Removes a planning/self-check ritual. Already consistent with silent selection and a single final artifact; no new policy needed. |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing/tree/35149473c6a70e64a76c09860bca82a08dda137b) | `40328bd292bc` → `35149473c6a7` | Material guidance reviewed amid substantial packaging/tooling changes. Adopt source-imperative preservation and truthful edit summaries; keep semantic relation checks. Do not import its router, detector scores, or numerical style targets. |
| [cosmos-makers/writer-persona](https://github.com/cosmos-makers/writer-persona/tree/5eee0fd5b0c2ce00fc3bd12ea546efb163d96cf8) | `5eee0fd5b0c2` → `5eee0fd5b0c2` | Unchanged. Existing profile and information-isolated evaluation guidance retained. |
| [AshwinSathian/humanize-writing-skill](https://github.com/AshwinSathian/humanize-writing-skill/tree/65f84fab8361184960410186f99d5b4cf506c972) | `0c3f05bc4f37` → `65f84fab8361` | v1.1.1; adopt explicit language and genre boundaries: purposeful reference parallelism and supported persuasive closes survive. Fiction/user-priority boundaries already covered. |
| [ai-evals-course/evals-skills](https://github.com/ai-evals-course/evals-skills/tree/2edbc5b1b0dc91f74fcfa8fd8f7eaeb302e052ab) | `b91c188388ef` → `2edbc5b1b0dc` | Entry point renamed to evals-start; packaging and README updated. Evaluation methodology unchanged in reviewed skill diffs. No implementation copied; no repository license file found. |

All six writing-source repositories retain MIT licenses. Eval Skills has no tracked license file at the reviewed revision; only its ideas are summarized, with credit, and no source implementation is bundled. The [revision ledger](2026-09-22-upstream-revisions.json) records full hashes. [Attributions](../ATTRIBUTIONS.md) now use those pins and correct Humanizer’s credit to the name in its license, Siqi Chen.

This was a repository-source refresh. Product inspiration, linked papers, Wikipedia, and other non-repository sources were not represented as newly researched. The Plugin Eval repository link is a schema-compatibility reference, not an inherited writing-rule source.

## Changes and exclusions

- The core routes recurring roles and strict output contracts to one [brief reference](../references/writing-briefs.md). The profile template can store writer-approved recurring briefs; one-off requests do not become permanent preferences.
- [Writing workflows](../references/writing-workflows.md) now explicitly check ranking, concurrent events, quantities/units, negation, causal relationships, and required versus suggested actions. These are checks on meaning, not targets for a style score.
- Genre and language boundaries preserve useful parallel reference structure, functional boilerplate, natural non-English usage, and a supported marketing call to action.
- Source imperatives can remain quoted content without becoming instructions to the assistant. Requested change summaries must describe the delivered edit, not the editing plan.
- Existing rules already cover fictional versus factual writing, intentional fragments, minimum-effective changes, calibrated evaluation, protected content, and voice evidence. They were not copied into additional rule sets.

We did not adopt detector-evasion tactics, authorship scores, mandatory punctuation bans, unsupported historical claims about AI-free writing, rigid diversity targets, reaction-invention permissions, multi-agent routers, or a required draft/critique/rewrite display. Argument-order diagnostics and visual-prompt-specific templates were left out because the current task did not establish a gap they would solve.

## Validation

A targeted comparison covers ten synthetic cases: action-only handoff, decision rationale on the same facts, missing assignments, comparative/timing fidelity, a quoted imperative, an honest edit summary, French grammar, parallel API reference entries, a supported call to action, and a hard 35-word limit with a condition.

There are three conditions (no skill, previous skill, refreshed skill), two repetitions, and 60 drafts across six batched CLI sessions. Generation used the same recorded default model and settings, with matched requests and source facts. Policies were frozen before generation. The case author knew the source-review goals but did not inspect proposed policy edits; this is targeted regression coverage, not a representative or independent discovery sample.

| Condition | Drafts | Exact-text/length assertions passed | Meaning flags | Output-contract flags |
|---|---:|---:|---:|---:|
| No skill | 20 | 24/24 | 0 | 0 |
| Previous skill | 20 | 24/24 | 0 | 0 |
| Refreshed skill | 20 | 24/24 | 0 | 0 |

All conditions passed the recorded checks. This is evidence that the new scoped rules did not introduce an observed regression on these cases; it does **not** establish an incremental gain over the old skill or no skill. No failing old-skill example was established for these newly explicit boundaries, so the additions are scoped clarifications supported by the user's request and upstream review, not claimed fixes to measured failures.

The 52 existing code tests pass, and the benchmark schema now validates 32 cases. Schema validity and CI success are separate from behavioral quality.

The prompts, policy snapshots, raw drafts, model configuration, blind mapping, and reviews are in [the evaluation record](../evals/brief-refresh-2026-09-22/README.md). Reviewers are models without human calibration. Hard-limit checks verify finished text; generation sessions were instructed not to use tools, so they do not test a tool-assisted counting workflow. Common CLI instructions and discovery metadata may still influence all conditions. Passing this set does not establish general writing quality, persona effectiveness, or the previously unmet 2× concision target.
