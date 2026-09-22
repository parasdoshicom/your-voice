# Evaluation audit: can we claim twice the concision?

No. The existing experiment is an exploratory comparison, not an acceptance test for the reported rambling problem. Its numbers are reproducible, but its baseline rarely exhibits that problem and its model judges have no human calibration.

Audited repository revision: `b980e397f5b13ab21d40d3c94e08390d0389180c`.
Method: [Eval Skills / eval-audit](https://github.com/ai-evals-course/evals-skills/blob/2edbc5b1b0dc91f74fcfa8fd8f7eaeb302e052ab/skills/eval-audit/SKILL.md). This audit applied the six diagnostic areas to the artifacts below; it did not run a new writing experiment.

Inspected: [stress outputs and labels](../evals/concision-stress-2026-09-22.json), [stress report](2026-09-22-concision-stress.md), [evaluation policy](../references/evaluation.md), [benchmark verifier](../scripts/verify_benchmark_output.py), [label scorer](../scripts/score_judges.py), [example labels](../evals/labels.example.jsonl), and [CI](../.github/workflows/test.yml).

## 1. Error analysis: the target failure is barely represented

**Status: Problem exists. Highest impact.** The concision judge labels 46/48 baseline drafts Pass and only 2 Fail. Both failures add diagnostic advice; neither demonstrates persistent three-paragraph answers to one-sentence questions. The 24 scenarios were designed synthetically rather than sampled from writer-rejected rambling. Two prompt variants are not independent user incidents.

**Fix:** Use error discovery on actual rejected replies plus a random sample of ordinary replies. Keep the request, source, response, and writer correction together. Use the current synthetic suite as regression coverage, not as evidence of prevalence or a general multiplier. Never make the baseline artificially verbose to manufacture a gain.

## 2. Judge validation: model preferences are uncalibrated

**Status: Problem exists.** No intended-writer labels or held-out TPR/TNR exist for these concision and meaning judges. The 12/6/30 preference result therefore cannot establish the writer's taste. The four rows in `labels.example.jsonl` explicitly identify themselves as synthetic examples; their `human_label` field is a schema demonstration, not human evidence.

**Fix:** Have the writer annotate diverse drafts in their original context. Convert recurring accepted failure definitions into binary judges only after review. Separate training, development, and test cases by originating incident, then validate against held-out human decisions. Until then use model judgments for triage only. Keep human labels empty until a human actually supplies them.

## 3. Evaluator design: length has no quality gate

**Status: Problem exists in the experiment, despite stronger written policy.** Total word counts combine one-word acknowledgments, constrained replies, and requested 100–150-word explanations. The treatment's publication overclaim contributes to its word total like any valid answer. Shortening those different jobs is not one interchangeable benefit. Pairwise preference also lacks a calibrated acceptance threshold.

**Fix:** Report verbosity reduction only alongside preserved meaning and human intent. Separate overlong replies, already-effective short answers, and teaching/narrative tasks. A response that cuts a necessary caveat fails regardless of length. Keep the deterministic exact-span and format checks: those are an appropriate use of code.

## 4. Human review process: no writer review occurred

**Status: Problem exists.** Reviewers were models. They saw requests, source text, and final outputs, but the committed dataset does not retain complete generation prompts, exact model identifiers/settings, or loaded host guidance. Final-only records cannot establish whether a brevity rule was loaded, forgotten, or overridden. JSON is inspectable but cumbersome for a writer's comparative review.

**Fix:** Present the original request/source and blinded drafts in a readable review surface with free-text notes. Preserve relevant generation configuration and visible message/tool traces for future runs, excluding credentials and hidden reasoning. Label absent context as absent; do not reconstruct it as observed evidence.

## 5. Labeled data: 96 outputs are not 96 independent trials

**Status: Problem exists.** Six batched generation sessions yielded 48 pairs from 24 synthetic scenarios. There is one sample per prompt/condition, no held-out evaluation split, and no human-labeled concision dataset. The explicit and default-concision subsets differ in task mix.

**Fix:** Split by scenario family before developing a revision. Repeat matched requests under the same recorded configuration. Treat related variants as a group when estimating uncertainty. Use exploratory labels as development evidence, never retrospectively relabel them as an untouched test set. Broader model claims require separate tests on those models.

## 6. Pipeline hygiene: CI validates plumbing, not writing behavior

**Status: Problem exists for any behavioral success claim.** CI runs unit tests, schema validation, example-label scoring, compilation, and the auditor version command. It does not generate fresh drafts, verify the stress dataset's aggregate results, or calibrate a judge. The stress JSON does not include executable generation and grading prompts sufficient to reproduce the run exactly.

**Fix:** Retain current CI as structural validation and name it accordingly. Archive the next run's exact prompts, skill revision, model/settings, context policy, outputs, and grading configuration. Add a reproducible result calculator before using the next experiment as a release gate. Re-run behavioral evaluation after material writing-rule changes. A green CI run must never be reported as proof of better concision.

## Proposed acceptance target, awaiting the writer's constraint

The request ended with “but,” so the following is a provisional interpretation, not an agreed or achieved target:

**On replies the writer has identified as overlong, use at most half the baseline words while retaining necessary meaning and the intended human response.**

For a next test:

1. Freeze the baseline, candidate revision, case families, and success rule before the held-out run. Compare baseline without Your Voice, current Your Voice, and a candidate under matched conditions. Choose which comparison the 2× claim refers to in advance; report both comparisons.
2. Keep development and held-out cases separate. Collect actual failing prompts rather than only asking a model to invent verbosity. Keep private traces outside this public repository.
3. Primary per-pair success: candidate uses at most 50% of baseline words AND passes meaning, required-action, and relationship checks. An invalid draft counts as a failure, not an excluded sample. Report the fraction of all eligible pairs meeting this rule and every semantic failure.
4. Proposed suite target: at least 80% of eligible held-out pairs meet that per-pair rule, with no observed required-meaning losses. This 80% threshold is a proposal requiring agreement, not a retrospectively selected result. Report uncertainty and do not interpret zero observed errors as zero risk.
5. In separate controls, reject damage to already-short replies, explanations, apologies, stories, protected text, and uncertainty. Do not force every kind of writing to halve its length.
6. Use blind writer judgments to decide whether the necessary content survived and whether the result is usable. Validate automated judges before treating them as substitutes.

The existing 8.1% default-subset reduction does not pass this proposed target. There is no honest 2× result yet. The next decisive evidence is a set of real overlong replies and the writer's judgment about what should survive, not another uncalibrated synthetic score.
