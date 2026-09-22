# Concision stress test — September 22, 2026

## Result

Your Voice helped modestly on this set; it did not establish reliable concision. Without explicit brevity instructions, it used 8.1% fewer words. Across all cases it used 1.3% fewer words, and one skill-loaded response overstated what the source established.

The baseline was already concise. This test did not reproduce the original persistent three-paragraph-for-one-sentence complaint, so it cannot show that the skill fixes that failure across Claude or ChatGPT.

## Design

Tested commit: `7ea1c2120db5f7c1e987e30592bdc4172869c81c`. The writing rules were frozen during the test.

- 24 synthetic scenarios, each in formal and terse prompt styles.
- 48 baseline drafts and 48 skill-loaded drafts: 96 generated outputs.
- 16 scenarios tested explicit instructions: short answers, unknown status, multiple asks, warmth, caveats, punctuation-only edits, emphasis, exact quotations/commands, source-text instruction injection, a beginner explanation, output-only replacement, tradeoffs, missing voice evidence, fixed bullets, and an impossible word limit.
- Eight additional scenarios tested default concision without a word limit. Two included 35 repetitive distractor notes.
- Six fresh generation sessions used the same inherited model configuration, with no model override. Drafts were generated in batches. Baseline sessions were told not to read the skill; treatment sessions loaded the core and applicable references.
- Two separate reviewers saw randomized X/Y labels, requests, and sources. One checked required meaning; one checked unnecessary content and pairwise concision. Neither received the condition key or skill.

[Complete prompts, drafts, grading, mapping, and adjudication](../evals/concision-stress-2026-09-22.json) are retained for inspection. All examples are synthetic.

## Length results

Words are whitespace-separated tokens; lower is not automatically better.

| Subset | Baseline | Your Voice | Difference |
|---|---:|---:|---:|
| Explicit constraints: 32 drafts per condition | 665 | 681 | 2.4% longer |
| No explicit brevity request: 16 drafts per condition | 360 | 331 | 8.1% shorter |
| All 48 drafts per condition | 1,025 | 1,012 | 1.3% shorter |
| Median words per draft | 18 | 17 | One word shorter |

The blind concision reviewer preferred Your Voice in 12 pairs, baseline in 6, and tied 30. These are exploratory model judgments, not a validated score or statistical evidence of a general effect. The reviewer flagged two baseline answers for adding unsolicited diagnostic next steps. Those steps could be useful in another context; the concern here is answering the specific question and stopping.

## What held up

Both conditions passed all 32 applicable deterministic assertions per condition: sentence limits where specified, the beginner explanation's 100–150-word range, protected quotation/command spans, punctuation-only word preservation, three bullets with owners/dates, meeting-time-only output, and the five-word response to an impossible constraint.

No draft obeyed the instruction to write dashboard praise embedded inside the source. The examples, arithmetic, approvals, and source limits were inspected by the meaning reviewer. Passing format checks alone does not establish that meaning survived.

## Failure and borderline result

The meaning reviewer flagged two responses, one from each condition. Parent review confirmed the publication failure and treats the summary omission as borderline.

**Confirmed failure, Your Voice:** The source said the editor showed Saved, preview worked, Publish had not been clicked, and no public page or deployment receipt had been observed. The draft opened:

> It hasn’t been published.

That states more than the observations establish. A safer concise answer would be:

> Publication isn’t verified: the draft is saved, but Publish hasn’t been clicked and no public page has been confirmed.

This proposed correction is explanatory, not a successful rerun. The actual failing draft remains in the data. No skill rule was changed to make this test pass.

**Borderline omission, baseline:** An operational summary retained export failure and Friday retry but omitted that the dashboard had not been evaluated. The reviewer marked it Fail. The prompt asked for a summary rather than every fact, so that omission is not an unambiguous failure of required meaning. The raw judgment is preserved rather than silently rewritten.

## Example where the skill helped

Request: reply to a peer asking about Tuesday or Thursday; the writer can do Thursday at 3 p.m. Pacific and cannot do Tuesday.

Baseline:

> Hi Jamie, Thursday at 3 p.m. Pacific works for me. I can’t do Tuesday. Does Thursday work for you?

Your Voice:

> Thursday at 3 p.m. Pacific works for me. I can’t do Tuesday.

Both are usable. The skill omitted a confirmation question and greeting; whether those are desirable depends on the relationship. This is a small editorial choice, not a universal improvement.

## Limits and next test

These are synthetic, batched, single-model tests. The inherited system writing guidance could already favor concise baseline output. We tested two prompt styles once each, not repeated sampling of identical prompts. Slight wording differences can change the requested response type, so comparisons are paired within each style rather than treated as identical replicas. No human voice recognition, Claude comparison, twenty-turn conversation drift, or production judge calibration was tested.

The next useful evidence would be actual prompts that produce unwanted length, evaluated on the models and settings where the problem occurs, with the writer judging what should survive. Current evidence supports “helps somewhat,” not “concision solved.”
