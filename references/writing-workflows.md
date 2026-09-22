# Writing workflows

Use the editorial priorities in `SKILL.md`. This file owns the transformation process; `patterns.md` owns the symptom checklist. Do one review, scaled to the job.

## Select before drafting

Privately identify the reader, situation, desired response, requested format, and available evidence. Use context already supplied. Ask only for missing information that would materially change the result; for a larger blank-slate piece, bundle necessary questions.

Sort the material into:

- **Must survive:** requested answers and actions, decisive facts, caveats, and the relationship or narrative work the piece must do.
- **Supports the point:** evidence, mechanism, example, or context the reader needs.
- **Can go:** repetition, generic setup, unnecessary chronology, and detail that does not serve this reader.

Select an order that fits the job. A status answer usually starts with the result; a personal story can earn its ending through the sequence. Do not print this planning inventory unless requested.

## Generate

Draft from the selected material in the writer's register for this recipient. Prefer approved samples over a platform template. When facts are missing, omit the claim, name the uncertainty, or use an explicit placeholder if the requested artifact needs one. User-authorized fiction or hypothetical examples must stay distinguishable from factual claims and personal experience.

For explanations, give enough mechanism and example for the intended reader to follow. Do not turn a request to teach into an unexplained slogan. Length follows the job and the user's constraints.

## Preserve

Repair only the named defect. Keep the existing progression unless restructuring was requested or is necessary to fix comprehension. A punctuation edit is not permission to replace vocabulary. An already effective sentence may need no change.

For source files, identify the editable prose span first. Keep surrounding syntax and protected content intact. Return the clean draft by default; explain changes only when asked or when a material ambiguity needs to be flagged.

## Condense

Start with the must-survive material, then choose the strongest necessary support. Remove whole redundant ideas before trimming individual words. Combine clauses only when the result remains easy to follow.

Compare the shorter version with the source: did it retain every requested answer, qualification, owner, date, and next action that matters? Did the apology, disagreement, invitation, or warmth still do its job? If the word limit cannot hold the required meaning, make the tradeoff explicit instead of silently deleting it. Do not add a recap to explain the shorter draft.

## Review without rewriting

Prioritize problems that change meaning, bury the point, or miss the relationship. Quote the relevant span and give a specific fix. Use `patterns.md` only for patterns that appear. Say when no change is needed. Do not guess authorship or score the probability that AI wrote the text.

## Technical prose

For procedures, guides, and explanations, use one term for one meaning, name the actor when known, and keep instructions in executable order. Prefer familiar words without deleting technical distinctions or required steps. Clear headings and lists are useful when they help navigation.

These general clarity principles are inspired by ASD-STE100. This skill does not include its controlled dictionary and does not certify compliance. Do not impose this mode on creative or personal writing.

## Final editorial review

Read once for the reader's experience, then compare against the source:

- Does the opening and order fit the purpose, and can the reader find every required answer?
- Did any claim, degree of certainty, social meaning, or protected span change?
- Does this sound like the supported writer in this relationship, without added personality or forced polish?
- Does each remaining detail serve the piece? Could a cut remove needed explanation, warmth, rhythm, or a caveat?

For substantial deliverables or recurring defects, consult `patterns.md` and run the local auditor when available:

```bash
python3 <skill-directory>/scripts/audit_text.py <draft-file>
```

Resolve the skill directory from `SKILL.md`; use a temporary UTF-8 draft file outside the public repo. Add `--mode technical` or `--mode spoken` when applicable. The auditor returns review candidates, not instructions to rewrite or a quality score. It masks common code, URL, and table forms but cannot recognize all quotations or attributed text; protect those manually. Review intentional matches rather than editing until the count reaches zero. A routine short reply needs no file or subprocess.

For speech, use `human-expression.md` and check delivery aloud. End when the piece has done its job.

## Calibrate a writer

Use `voice-profile-template.md` with material the user owns, supplied, approved, or asked you to inspect. Leave unsupported traits unknown. Separate durable voice from channel conventions and temporary campaign habits. Record rejected patterns as well as protected ones. For changes over time, follow `approval-learning-loop.md`; for validation, follow `evaluation.md`.
