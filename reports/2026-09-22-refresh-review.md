# Repository refresh review — 2026-09-22

## Scope and decisions

Reviewed the writing instructions, profiles, personalization files, scripts, tests, evaluation fixtures, install path, CI workflows, and historical source records. This refresh reorganizes the existing guidance; it does not claim a fresh review of every external source in ATTRIBUTIONS.md.

- Core instructions now select the reader's needed content before drafting and work without loading the full pattern catalog for a short reply.
- One substantial-writing workflow owns selection, transformation, and final review. Spoken guidance adds delivery checks only.
- Condensation preserves requested answers, caveats, relationship work, and intentional narrative. Clearly labeled, user-requested hypothetical examples are allowed.
- Paras's course-specific design and operating choices moved to an optional channel reference without being discarded.
- Rejection-list examples are inert until selected. Approval promotion has one consistent policy.
- Tool review found and fixed percentage detection, case-sensitive protected spans, numeric token matching, canonical installation checks, and malformed enum handling.

Two independent agents reviewed editorial structure and tooling. The editorial reviewer rechecked the revised instructions; its two remaining fixes were applied. Six synthetic cases were added to the model-agnostic benchmark, covering competing requirements rather than checking for specific prose. The optional live harness also gained a concision scenario, bringing it to five scenarios.

## Small behavioral comparison

Five identical requests were sent to separate baseline and skill-loaded agent sessions using the inherited model configuration. Each produced one draft per case. The baseline was told not to load Your Voice; the treatment read the revised skill. A separate reviewer saw only anonymized X/Y drafts and the requests. This was a lightweight model-reviewed smoke check, not a fully controlled harness experiment, human preference study, or measured match to Paras's voice.

| Case | Both satisfy request | Reviewer preference after unblinding |
|---|---|---|
| Direct shipping answer with approval blocker | Yes | Treatment |
| Warm birthday apology | Yes | Tie; identical drafts |
| Punctuation-only narrative edit | Yes | Tie |
| Two asks with separate deadlines | Yes | Tie |
| Beginner explanation with a hypothetical example | Yes | Treatment, slight |

The stronger teaching draft was longer. This supports retaining useful explanation rather than optimizing word count alone. Two preferences and three ties on five synthetic cases do not establish a general improvement. No human reviewer or long-context stress run was used.

## External review boundary

Stanley had no callable plugin/MCP in the session. A browser fallback reached its sign-in page, so no Stanley review was obtained. Nothing in this report should be attributed to Stanley.

## Validation

Local validation passed: 45 unit tests and 19 behavioral-case schema checks. Python compilation, installer shell syntax, local Markdown links, and skill frontmatter also passed. CI is a separate remote check. The optional plugin-eval live harness was not run; separate agent writing comparisons are reported above. The synthetic judge-label examples validate format only.

## Comparison artifacts

The following drafts use synthetic scenarios only. Labels are revealed here after review.

### Case A

Baseline:

The review is done, but required security approval is still pending. We can ship today if that approval comes through; we need it before we ship.

Treatment:

We can ship today only if the required security approval comes through. Review is done; approval is still pending.

### Case B

Baseline:

I’m sorry I missed your birthday. I got the date wrong, and that’s on me. Hope you had a lovely day. Can I take you to lunch Saturday?

Treatment:

I’m sorry I missed your birthday. I got the date wrong, and that’s on me. Hope you had a lovely day. Can I take you to lunch Saturday?

### Case C

Baseline:

The kettle clicked off. I left your cup where you always put it, by the window.

Treatment:

The kettle clicked off; I left your cup where you always put it, by the window.

### Case D

Baseline:

Could you approve the budget by Thursday and nominate a test owner by Friday? We need both before the pilot can start. Thanks!

Treatment:

Could you approve the budget by Thursday and nominate a test owner by Friday? We need both before the pilot can start.

### Case E

Baseline:

An average combines several results into one number. That makes it useful for a quick summary, but it can hide how different the individual results are.

Here is a hypothetical example: five people wait for a bus. Four wait 5 minutes each, and one waits 30 minutes. The total waiting time is 50 minutes. Divide that by five people, and the average wait is 10 minutes.

But nobody actually waited 10 minutes. Most had a short wait, while one person had a much longer wait. Saying ‘the average wait was 10 minutes’ misses that difference.

To understand the experience better, look at the individual results or report how many people had short and long waits alongside the average.

Treatment:

An average combines several results into one number. You calculate it by adding the results and dividing by how many there are. That is useful for a quick overview, but it hides how far apart the individual results are.

Hypothetical example: five people wait 2, 2, 2, 2, and 42 minutes for help. Their total wait is 50 minutes, so the average is 10 minutes. Yet nobody actually waited 10 minutes. Four people got help quickly, while one waited much longer.

Another group could have five people who each waited exactly 10 minutes. The average would be the same, but their experiences would be very different. To understand the results, look at the individual values or how many fall into different ranges, alongside the average.
