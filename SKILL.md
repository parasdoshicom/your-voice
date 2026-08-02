---
name: voicelatch
description: Preserve a real writer's voice while drafting, editing, or reviewing human-facing prose. Use by default for messages, reports, documentation, posts, essays, customer copy, and any text written in a named person's voice. Combines voice calibration, anti-slop editing, evidence checks, and a final read-aloud gate without optimizing for AI detectors.
license: MIT
metadata:
  author: Paras Doshi
  repository: https://github.com/parasdoshicom/voicelatch
---

# VoiceLatch

Keep the writer in the writing.

Apply this skill silently whenever a person will read the output. Do not load separate humanizer, stop-slop, no-ai-slop, or generic style-cleanup skills unless the user explicitly asks to compare them. VoiceLatch incorporates the compatible rules and credits its influences in `ATTRIBUTIONS.md`.

## Non-negotiables

1. Preserve meaning. Never invent a claim, example, quote, statistic, source, joke, emotion, or opinion.
2. Preserve voice. Keep the writer's vocabulary, cadence, bluntness, humor, uncertainty, digressions, and useful roughness.
3. Prefer evidence over polish. A concrete fact beats a better-sounding abstraction.
4. Edit proportionally. Leave strong human sentences alone. Do not make every paragraph equally tidy.
5. Do not optimize for AI detectors. They are unreliable and reward cosmetic evasion. Optimize for truthful, specific, recognizable writing.
6. Do not strip provenance metadata, inject errors, or add fake personal texture.
7. Local safety, legal, brand, and factual rules outrank this style skill.

## Choose the job

### Draft

When creating text from notes or source material:

1. Identify the reader, purpose, decision, and format.
2. Pull the writer's profile when one exists. Prefer approved writing and pre-generative-AI samples.
3. Extract the facts, examples, and point of view the source actually supports.
4. Draft in the writer's natural structure. Do not start from a generic social template.
5. Run the latch pass below.

### Edit

Make the minimum effective edit. Keep the writer's progression unless it hurts comprehension. Return only the clean draft unless the user asks for commentary.

### Detect

If the user asks for an audit without a rewrite, quote each offending line, name the pattern, and suggest a short fix. Do not score the probability that AI wrote it.

### Calibrate

Build or update a voice profile only from material the user owns, supplied, approved, or asked you to inspect. Separate:

- durable voice signals;
- channel conventions;
- temporary campaign habits;
- patterns the writer rejected.

Use `references/voice-profile-template.md`. Store private examples outside a public skill repository unless the user explicitly approves publication.

## The latch pass

Run these checks in order.

### 1. Truth

- Can every factual claim be traced to the prompt, a supplied source, or a cited source?
- Did the draft smuggle in confidence, causality, or consensus the evidence does not support?
- Did editing change the claim?

### 2. Point of view

- Is there a real observation, decision, example, or mechanism?
- Would this still be useful if the formatting disappeared?
- Could the same paragraph plausibly come from thousands of accounts? If yes, add supported specificity or cut it.

### 3. Voice

- Does the rhythm match the writer's samples?
- Does the writer normally use first person, contractions, fragments, questions, parentheticals, or humor here?
- Did polish erase a phrase the writer would recognize as theirs?
- Is a modern platform convention overpowering the writer's established voice?

### 4. Slop

Cut only what appears. Common failures include:

- throat-clearing and chatbot artifacts;
- faux-insight setups and colon reveals;
- binary contrasts and negative lists;
- significance inflation, promotional language, and vague attribution;
- trailing `-ing` clauses that pretend to explain;
- synonym cycling, forced groups of three, and robotic symmetry;
- decorative em dashes, bold, emoji headings, tiny sections, and stacked fragments;
- fake-profound closers and recap endings;
- passive constructions that hide the actor;
- abstract nouns where a concrete action or number exists.

See `references/patterns.md` for the consolidated pattern library.

### 5. Read aloud

Read the draft as speech. Fix any line a smart person would not say naturally. Keep intentional roughness. End on the last concrete point, useful implication, or next action.

## Paras Doshi profile

When writing as Paras Doshi, read `profiles/paras-doshi.md`. Treat it as a baseline, not a costume. Newer approved drafts can refine it, but one campaign or viral format must not overwrite the durable profile.

## Improvement loop

Discovery never equals adoption.

1. Search for new public writing skills, editorial research, and voice-calibration products using `scripts/discover_sources.py` or the weekly workflow.
2. Record the source, author, URL, license, retrieved date, and candidate rule.
3. Reject detector-evasion, provenance stripping, fake-error injection, unsupported claims, and rules that flatten voice.
4. Add a failing eval that demonstrates a real gap.
5. Adopt the smallest rule that passes existing and new evals.
6. Credit the source in `ATTRIBUTIONS.md`.
7. Require human review before changing the default skill.

Read `references/discovery-loop.md` before adopting a new source.

## Output gate

Before sending human-facing prose, confirm silently:

- factual meaning survived;
- the named writer would recognize the voice;
- no unsupported texture appeared;
- concrete details survived editing;
- formatting serves the content;
- the ending does real work.

