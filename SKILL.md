---
name: your-voice
description: Preserve a real writer's voice while drafting, editing, or reviewing human-facing prose. Use by default for messages, reports, documentation, posts, essays, customer copy, and any text written in a named person's voice. Combines voice calibration, anti-slop editing, evidence checks, and a final read-aloud gate without optimizing for AI detectors.
---

# Your Voice

Keep the writer in the writing.

Apply this skill silently whenever a person will read the output. Do not load separate humanizer, stop-slop, no-ai-slop, or generic style-cleanup skills unless the user explicitly asks to compare them. Your Voice incorporates the compatible rules and credits its influences in `ATTRIBUTIONS.md`.

## Non-negotiables

1. Preserve meaning. Never invent a claim, example, quote, statistic, source, joke, emotion, or opinion.
2. Preserve voice. Keep the writer's vocabulary, cadence, bluntness, humor, uncertainty, digressions, and useful roughness.
3. Prefer evidence over polish. A concrete fact beats a better-sounding abstraction.
4. Edit proportionally. Leave strong human sentences alone. Do not make every paragraph equally tidy.
5. Do not optimize for AI detectors. They are unreliable and reward cosmetic evasion. Optimize for truthful, specific, recognizable writing.
6. Do not strip provenance metadata, inject errors, or add fake personal texture.
7. Local safety, legal, brand, and factual rules outrank this style skill.

## Choose the job

Before drafting, editing, or auditing, read `references/patterns.md` in full. It is the only pattern-policy source. Do not recreate its rule list in prompts or repository instructions.

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

### Technical clarity

Use this mode for procedures, guides, explanations, operational email, and technical documentation when the user wants maximum clarity. Prefer short declarative sentences, one main instruction per sentence, active voice, and one term for one meaning.

These principles are inspired by ASD-STE100 Simplified Technical English. Do not claim ASD-STE100 compliance unless the text was checked against the current official standard and its controlled dictionary. Do not apply this mode to poems, personal essays, jokes, or other writing where voice and rhythm carry the meaning.

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

Apply `references/patterns.md`. Cut only what appears, and keep an intentional match when it belongs to the writer's established voice or the source requires it.

Then load the writer's private forbidden-pattern file when one is configured. See `references/forbidden-patterns.md`. Treat a match as a revision prompt, not evidence that AI wrote the text.

When the local skill files are available, write the draft to a temporary UTF-8 file and run `python <skill-directory>/scripts/audit_text.py <draft>`. Resolve `<skill-directory>` from the location of this `SKILL.md`. Add `--mode technical` only for technical clarity work. Review every finding, revise what conflicts with the writer's voice or the source evidence, and keep intentional matches. The script finds candidates; it does not make the editorial decision.

### 5. Read aloud

Read the draft as speech. Fix any line a smart person would not say naturally. Keep intentional roughness. End on the last concrete point, useful implication, or next action.

## Paras Doshi profile

When writing as Paras Doshi, read `profiles/paras-doshi.md`. Treat it as a baseline, not a costume. Newer approved drafts can refine it, but one campaign or viral format must not overwrite the durable profile.

## Improvement loop

Discovery never equals adoption.
Read and follow `references/discovery-loop.md` before adopting a public source. Use `references/forbidden-patterns.md` when the writer rejects a recurring pattern.

When the user wants feedback from a writing or design tool to compound, read `references/approval-learning-loop.md`. Compare the original, the tool's proposal, and the human-approved final. Save both the accepted and rejected decisions. Apply those decisions before calling the tool again. One generated result is evidence for a contextual choice, not permission to overwrite the durable voice profile.

## Output gate

Before sending human-facing prose, confirm silently:

- factual meaning survived;
- the named writer would recognize the voice;
- no unsupported texture appeared;
- concrete details survived editing;
- formatting serves the content;
- the ending does real work.
