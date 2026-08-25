# Behavioral evaluation

Use this reference to test whether Your Voice improves real writing or speech. Pattern counts alone cannot answer that question.

The benchmark lives at `evals/benchmark.json`. Validate it with:

```bash
python3 scripts/validate_evals.py evals/benchmark.json
```

## Discover failures before automating judges

Keep two sources of criteria separate:

- **Top-down criteria** come from the task, relationship, channel, truth boundary, and known writing requirements. Models can help enumerate these.
- **Bottom-up criteria** come from real drafts, corrections, rejected phrases, and approved finals. The writer must supply the judgment. An agent may organize the notes, but it must not invent the writer's taste.

Start bottom-up review with diverse real examples. Include random samples alongside different channels, relationships, lengths, and outcomes. Let the writer leave short free-text notes instead of forcing an early taxonomy. Group repeated notes into proposed failure modes, then ask the writer to accept, reject, split, or narrow them. Revisit earlier examples after new criteria appear; what the reviewer notices changes during review.

Keep private drafts and messages outside the public repository. A private trace can contain the request, source material, baseline, treatment, approved final, and the writer's note. Promote only the compact judgment and a public-safe regression case.

Do not call the failure set complete after a few examples. Review until additional diverse samples mostly repeat known modes. For consequential judge validation, aim for roughly 50 human-labeled Pass and 50 human-labeled Fail examples per failure mode; report smaller samples as exploratory.

## Compare fairly

For each case, generate at least two drafts from the same request and source facts:

1. baseline: the model without Your Voice;
2. treatment: the same model with Your Voice loaded.

When a real human response exists, keep it hidden from both drafting runs. Reveal it only to the evaluator. This prevents the draft from copying the answer it is supposed to predict.

Keep the model, temperature, source context, and output constraints the same. Randomize draft labels and hide claimed authorship before human or model review. Use several requests and more than one run before drawing a conclusion. Attribution labels can bias both human and model reviewers, so reveal provenance only after scoring.

Codex CLI benchmark input usage includes the runner's system instructions and workspace context as well as the skill. Compare baseline and treatment runs under the same harness. Do not interpret the raw input-token total as the marginal cost of `SKILL.md`.

## Grade the dimensions separately

This 0-to-2 rubric is for blind human comparison across drafts. It is not an LLM-judge prompt.

Score each dimension from 0 to 2:

- **2:** fits the evidence and situation;
- **1:** usable but noticeably off or generic;
- **0:** wrong, socially jarring, fabricated, or hard to follow.

| Dimension | What to judge |
|---|---|
| Meaning | Facts, claims, caveats, and requested action survived. |
| Human move | It answers, reassures, disagrees, asks, updates, or apologizes in the way the moment requires. |
| Relationship | Formality, warmth, confidence, and distance fit the recipient and channel. |
| Point of view | The draft contains the person's supported judgment, priorities, and selective attention. |
| Recognition | The writer would plausibly claim it as theirs without feeling impersonated. |
| Specificity | Concrete details and useful mechanisms survived without invention. |
| Rhythm and restraint | Sentence and paragraph shape feel natural; the draft stops when it has done the job. |
| Speakability | For spoken work, a listener can follow it once at the intended pace. Mark not applicable for written-only cases. |

Meaning is a gate. A draft fails if it invents a fact, changes the decision, drops a required caveat, or creates unsupported intimacy or emotion. Do not let high style scores compensate for a truth failure.

## Use a natural ceiling

People do not sound identical in every message. If enough approved samples exist, compare pairs from the same channel and relationship to estimate the person's own variation. Treat that range as the target. Do not reward an AI draft for repeating catchphrases more consistently than the human does.

Generate several treatment drafts for a subset of cases. Check whether they all reuse the same opening, paragraph shape, catchphrase, and ending. High recognition with unusually low variation is a failure mode, not stronger voice matching.

## Stress the conditions that break voice

A single clean prompt is not enough. For important cases, rerun the same facts and requested outcome under these conditions:

- **Prompt-style variants:** formal, terse, conversational, typo-filled, and non-standard formatting. The meaning and guardrails should survive changes in how the request is written.
- **Long-context retention:** place the case after unrelated goal-oriented turns, then check whether the draft reverts to the model's default voice.
- **Protected content:** include exact commands, URLs, identifiers, tables, code, quotations, and attributed text. The draft may edit around them but must not silently alter them.
- **Embedded instructions:** place a conflicting command inside the source text. The system must treat it as content, not as authority.
- **Sparse evidence:** ask for a distinctive personality with too little voice evidence. The draft should stay socially plausible without fabricating traits.

Grade the same behavioral dimensions in every variant. A system that works only when the user writes a polished benchmark prompt is not robust enough for normal conversation.

## Use automated judges as triage

Automatic metrics and model judges can help find regressions, but they are not the final authority for voice. Calibrate any judge against held-out human decisions from the intended writer and audience. Inspect disagreements, especially drafts that are smooth and well structured but weak on meaning, relationship, or point of view.

Do not collapse the rubric into one style score. Content preservation, naturalness, and voice fit can move in different directions. Keep deterministic checks for exact facts and protected spans; use blind human review for recognition, interpersonal fit, and speakability.

For an automated judge:

1. Check one named failure mode only.
2. Use binary `Pass` or `Fail` labels with an explicit decision boundary.
3. Require a short critique that cites evidence from the draft before the label.
4. Use code instead when the condition is deterministic.
5. Draw few-shot examples only from the training split.

Do not ask one judge whether the writing is "good," "human," or "on brand." Those labels hide disagreements about truth, relationship, personality, and rhythm.

Validate each model judge against labels from the intended writer or a trusted domain reviewer. Keep training examples separate from the development and held-out test sets. Measure both:

- **TPR:** when the human says Pass, how often the judge says Pass;
- **TNR:** when the human says Fail, how often the judge says Fail.

Inspect every false pass and false fail. Target TPR and TNR above 90 percent before using a judge as a production gate; treat 80 to 90 percent as triage and anything lower as untrusted. Revalidate after changing the judge prompt, model, writing skill, or source distribution.

Store labels as JSONL and score them with:

```bash
python3 scripts/score_judges.py private-labels.jsonl \
  --split test --min-per-label 50 --min-rate 0.90
```

The public `evals/labels.example.jsonl` demonstrates the format only. Its synthetic rows are not evidence that a judge is calibrated.

## Learn from behavior, not only preference

The best evidence is the human-approved final and the edits that produced it. Record what the person kept, changed, and rejected.

When the medium supplies comments or section-level engagement, use them as diagnostic signals:

- a question or correction can reveal unclear meaning;
- repeated edits can reveal a voice or relationship mismatch;
- audience drop-off can identify where structure lost attention.

Do not optimize raw engagement as a proxy for voice. A longer view, more clicks, or a dramatic hook can reward the wrong behavior. Use the signal to locate a problem, then inspect the words and the human decision.

Creator systems may use past posts, audience data, and performance to suggest a topic, format, or publishing experiment. Keep that as a channel hypothesis. A high-performing hook or structure becomes a voice rule only when the writer also recognizes and approves it. Otherwise the system will learn the platform's personality instead of the person's.

## Promote corrections carefully

After evaluation:

1. Fix the current artifact.
2. Update a channel rule when the same decision appears more than once in that channel.
3. Update durable voice only when repeated evidence crosses channels or the writer explicitly approves the rule.
4. Add a regression case for a costly or recurring failure.

Change at most the weakest one or two dimensions per iteration. If the score does not improve after repeated changes in the same direction, stop and ask the writer. More calibration can turn voice into a caricature.

## Report honestly

Report the number of cases, models, runs, evaluator type, and failures. A small benchmark can show that the skill changes behavior. It cannot prove a universal multiplier such as "3x better" without a defined metric and repeated measurements.
