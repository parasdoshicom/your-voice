# Concision rerun: two revisions, with failures retained

## Result

The revised skill is shorter on these samples, but **the requested 2× improvement is not demonstrated**. The final revision used 13.1% fewer words than the previous skill on narrow questions and only 3.9% fewer than the no-skill baseline. One of 16 paired narrow-question outputs reached half the previous skill's length. The target was at least 80%, with preserved meaning; it failed.

A reviewer also flagged the same unsupported booking-timing instruction in both the previous and final skill. Do not describe this release as having zero meaning failures, a proven general benefit, or solved concision.

## What changed

The final skill forms the minimum complete answer before expanding it, excludes adjacent source facts that do not answer the question, and tests whether each extra sentence earns its space. Condensation starts from essential content rather than trimming every source sentence. Explicit exceptions protect explanations, stories, warmth, and multi-part requests. Unverified evidence and conditional claims must remain qualified.

The tested final policy is archived in [stage 2's snapshot](../evals/concision-rerun-2026-09-22/stage-2/candidate-policy.json). Its contents match the released `SKILL.md` and writing workflow. The preceding skill came from commit `1573c562e78ad69a44afbe7aff9a1dabb2c0d68d`.

## Design and sequence

We applied the [Eval Skills audit approach](https://github.com/ai-evals-course/evals-skills/blob/2edbc5b1b0dc91f74fcfa8fd8f7eaeb302e052ab/skills/eval-audit/SKILL.md), retaining failures and separating deterministic checks from exploratory model review.

- Stage 1: 18 new synthetic scenarios, three conditions, two repetitions: 108 drafts. Six scenarios involved generation, six condensation, and six controls.
- Stage 2: after inspecting stage 1, a second revision targeted unnecessary adjacent facts. An independent case author who did not inspect policies or generated outputs created 12 fresh scenarios: eight narrow questions and four controls. Three conditions and two repetitions yielded 72 drafts.
- Two known-failure regression probes produced two additional drafts. These were development checks, not held-out evidence.
- Total: 180 comparison drafts across 30 scenarios, plus two regression drafts. Each stage used six separate CLI generation sessions; examples within a session were batched. These are not 180 independent trials.
- All comparison runs recorded `gpt-6-astra`, OpenAI provider, reasoning effort `none`, Codex CLI `0.155.0-alpha.9.2`. The CLI selected its default model; no model override was supplied. Temperature was not exposed or set.
- Requests and source facts were identical across conditions. Case order matched by repetition; condition launch order was randomized. Candidate instructions were frozen before their stage's generation. The second test concerns a narrower distribution, so its percentages are not a direct improvement over stage 1's percentages.
- CLI user config was ignored, project instructions were disabled, and automatic loading of the known Your Voice skill path was disabled. Policies were supplied inline. Common host instructions, tool/skill descriptions, and CLI scaffolding may still influence every condition. This is not a raw foundation-model comparison.
- Two independent model reviewers received randomly labeled individual drafts with requests and source facts. One checked required meaning; the other checked communicative usability. Neither saw arm identities or skill policies. They were not calibrated against human labels; their complete host context and exact model settings were not independently captured. The [review protocol](../evals/concision-rerun-2026-09-22/review-protocol.md) records their criteria. Review labels are triage evidence, not proof of human voice quality.

## Stage 1: the first revision failed

| Task group, 12 drafts per condition | No skill words | Previous skill words | First revision words | Reduction versus previous |
|---|---:|---:|---:|---:|
| Generation | 526 | 540 | 507 | 6.1% |
| Condensation | 676 | 693 | 660 | 4.8% |
| Controls | 875 | 871 | 821 | 5.7% |

The primary condensation target had **0/12** half-length successes. Both a no-skill draft and a first-revision draft assumed the questioner had a reservation. The source guaranteed seats only for reservation holders. Those failures remain in the [full stage 1 record](../evals/concision-rerun-2026-09-22/stage-1/experiment.json).

A separate audit, blind to outputs and policy, found optional or conditional items in 11 of 18 proposed content checklists. The original cases and [criteria audit](../evals/concision-rerun-2026-09-22/stage-1/criteria-audit.json) are both retained. Reviewers were instructed that the actual request and source govern: merely appearing in the source does not make a fact mandatory. Checklist items were not given to drafting sessions.

## Stage 2: narrower answers, still below the target

| Task group | Drafts per condition | No skill words | Previous skill words | Final revision words | Reduction versus previous |
|---|---:|---:|---:|---:|---:|
| Narrow questions | 16 | 283 | 313 | 272 | 13.1% |
| Controls | 8 | 559 | 558 | 538 | 3.6% |

For narrow questions, the corresponding reduction versus no skill was **3.9%**. The primary half-length success rate was **1/16 (6.25%)**, below the predeclared 80% target. A shorter control is not automatically better; those rows are reported for completeness, not rewarded for compression.

**Unresolved fidelity flag:** two previous-skill drafts and two final-revision drafts advised reserving a pottery wheel “before you come.” The source required reservations but did not specify booking before arrival. The reviewer treated that extra timing instruction as an unsupported requirement. Parent review retains the conservative flag: it may read as sensible advice, but the timing is not established by the source. It is one repeated scenario, not four independent failure types.

No communicative-usability failures were flagged in either stage. All supplied deterministic word-range, exact-span, and punctuation-preservation checks passed. Neither observation cancels the semantic flags or establishes a personal voice match.

The two known regression probes passed their separate meaning review: the reservation answer explicitly says “If you have a reservation,” and the publication answer says “Publication is unverified.” These are successful checks of known examples, not a measured population error rate.

[Full stage 2 outputs and judgments](../evals/concision-rerun-2026-09-22/stage-2/experiment.json) and [separate regression judgments](../evals/concision-rerun-2026-09-22/stage-2/regression-review.json) remain inspectable.

## Reproduce and interpret

The [experiment directory](../evals/concision-rerun-2026-09-22/README.md) contains exact prompts, policy snapshots, outputs, randomized mappings, judgments, configuration manifests, and executable generation scripts. Recompute results with:

```bash
python3 scripts/summarize_concision_run.py evals/concision-rerun-2026-09-22/stage-1/experiment.json --check-summary evals/concision-rerun-2026-09-22/stage-1/summary.json
python3 scripts/summarize_concision_run.py evals/concision-rerun-2026-09-22/stage-2/experiment.json --check-summary evals/concision-rerun-2026-09-22/stage-2/summary.json
```

Missing reviews cannot count as a quality pass; failed drafts stay in the denominator. CI checks calculation integrity and code behavior, not whether the 2× target passed. Both stored `proposed_target_met` values are false.

These are synthetic, single-model, batched experiments with only two repetitions and uncalibrated model reviewers. There was no Claude test, human evaluation, long-conversation test, or evidence of statistical significance. The rule revision adds instruction context; output-word reductions are not a claim of lower total model-token cost. Its strongest supported result is a modest reduction on the narrow-question sample, with unresolved fidelity risk. Larger claims require new evidence.
