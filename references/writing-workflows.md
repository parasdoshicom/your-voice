# Writing workflows

### Draft

When creating text from notes or source material:

1. Identify the reader, purpose, decision, and format.
2. Pull the writer's profile when one exists. Prefer approved writing and pre-generative-AI samples.
3. Extract the facts, examples, and point of view the source actually supports.
4. Check whether the request has enough context to produce a useful draft. Ask only questions whose answers would change the output; for a larger blank-slate piece, batch the questions instead of dribbling them out one at a time.
5. Draft in the writer's natural structure and register for this relationship. Do not start from a generic social template.
6. Run the latch pass below.

### Edit

Make the minimum effective edit. Keep the writer's progression unless it hurts comprehension. Return only the clean draft unless the user asks for commentary.

Confirm that the target is human-facing prose before rewriting a file. Do not run a whole-file prose rewrite over source code, configuration, schemas, generated data, commands, paths, identifiers, URLs, citations, tables, quoted material, or text attributed to another person. Edit around protected spans and flag any issue inside them. If the user explicitly asks to edit prose in a code comment, UI string, or similar bounded span, change only that span and preserve the surrounding syntax exactly.

A tone, relationship, or voice target controls expression only. It never authorizes adding a fact, opinion, joke, emotion, anecdote, endorsement, or instruction that the source does not support.

### Detect

If the user asks for an audit without a rewrite, quote each offending line, name the pattern, and suggest a short fix. Do not score the probability that AI wrote it.

### Calibrate

Build or update a voice profile only from material the user owns, supplied, approved, or asked you to inspect. Separate:

- durable voice signals;
- channel conventions;
- temporary campaign habits;
- patterns the writer rejected.

Use `voice-profile-template.md`. Store private examples outside a public skill repository unless the user explicitly approves publication.

When a creator or social tool supplies past-post or performance data, use it to form channel and format hypotheses. Do not treat engagement as proof of voice, truth, or quality. Promote a pattern only when approved writing and the writer's judgment support it.

### Spoken

For interview answers, narration, talks, voice notes, or text meant to be said aloud, read `human-expression.md`. Write for a listener, not a page. Preserve the speaker's way of thinking while removing syntax that becomes hard to follow in one hearing.

### Technical clarity

Use this mode for procedures, guides, explanations, operational email, and technical documentation when the user wants maximum clarity. Prefer short declarative sentences, one main instruction per sentence, active voice, and one term for one meaning.

These principles are inspired by ASD-STE100 Simplified Technical English. Do not claim ASD-STE100 compliance unless the text was checked against the current official standard and its controlled dictionary. Do not apply this mode to poems, personal essays, jokes, or other writing where voice and rhythm carry the meaning.

## The latch pass

Run these checks in order.

### 1. Truth

- Can every factual claim be traced to the prompt, a supplied source, or a cited source?
- Did the draft smuggle in confidence, causality, or consensus the evidence does not support?
- Did editing change the claim?

### 2. Human intent

- Does the draft make the right social move: answer, reassure, disagree, invite, update, apologize, or ask?
- Does it fit the actual relationship and power distance?
- Is the emotional temperature proportionate, or did polish make it colder, warmer, more certain, or more enthusiastic than the source?

### 3. Point of view and personality

- Is there a real observation, decision, example, or mechanism?
- Would this still be useful if the formatting disappeared?
- Could the same paragraph plausibly come from thousands of accounts? If yes, add supported specificity or cut it.
- Does personality come from what this person notices, values, doubts, and chooses, rather than decorative quirks?
- Did the draft invent attitude, intimacy, humor, vulnerability, or confidence that the evidence does not support?

### 4. Voice

- Does the rhythm match the writer's samples?
- Does the writer normally use first person, contractions, fragments, questions, parentheticals, or humor here?
- Did polish erase a phrase the writer would recognize as theirs?
- Is a modern platform convention overpowering the writer's established voice?

### 5. Slop

Apply `patterns.md`. Cut only what appears, and keep an intentional match when it belongs to the writer's established voice or the source requires it.

Then load the writer's private forbidden-pattern file when one is configured. See `forbidden-patterns.md`. Treat a match as a revision prompt, not evidence that AI wrote the text.

When the local skill files are available, write the draft to a temporary UTF-8 file and run `python3 <skill-directory>/scripts/audit_text.py <draft>`. Resolve `<skill-directory>` from the location of this `SKILL.md`. Add `--mode technical` for technical clarity work or `--mode spoken` for words meant to be heard. Review every finding, revise what conflicts with the writer's voice or the source evidence, and keep intentional matches. The script finds candidates; it does not make the editorial decision.

### 6. Read aloud

Read the draft as speech. Fix any line a smart person would not say naturally. Keep intentional roughness. End on the last concrete point, useful implication, or next action.
