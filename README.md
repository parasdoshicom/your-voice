# Your Voice

Your Voice is an agent skill that keeps AI-assisted writing specific, truthful, and recognizably yours.

Most “humanizer” workflows stack several overlapping prompts. They remove the same em dash three times, flatten the writer's quirks, and still miss the harder problem: the draft has no point of view. Your Voice puts voice and evidence first, then runs one consolidated anti-slop pass.

It is designed for Codex, Claude Code, OpenCode, OpenClaw, GitHub Copilot, and other tools that support the Agent Skills `SKILL.md` format.

Version 1.2 turns personal taste into a feedback loop. The local audit catches more machine-shaped patterns, reads a private forbidden-pattern file, and can apply stricter clarity checks to technical writing.

## What it does

- drafts, edits, or audits human-facing prose;
- learns from approved writing samples without copying content into the skill;
- separates durable voice from platform habits;
- consolidates compatible rules from Humanizer, Stop Slop, No AI Slop, and related editorial workflows;
- rejects detector gaming, fake mistakes, and invented personal texture;
- runs a provenance-aware weekly discovery loop for new public techniques;
- remembers patterns you reject without publishing your drafts;
- offers an optional technical mode for procedures, guides, and explanations;
- includes a public Paras Doshi profile derived from his pre-2023 writing and public LinkedIn work.

## Install

Clone the repository, then run:

```bash
./scripts/install.sh
```

The installer links one canonical checkout into supported global skill locations. It can also install into OpenClaw agent Codex homes found on the host.

For a single agent, link or copy this repository into that agent's skills directory under the name `your-voice`.

Then add this default to the highest shared `AGENTS.md` your agents inherit:

```text
For human-facing prose, apply Your Voice by default. Your Voice satisfies any
component humanizer, stop-slop, no-ai-slop, or generic prose-cleanup requirement;
do not load those component skills separately unless comparison is requested.
```

## Use

Ask your agent to draft, edit, or review prose. Your Voice is meant to run as the default final pass, not as a separate ceremony.

Examples:

```text
Draft this update in my voice from these notes.
```

```text
Edit this. Keep the roughness and do not add claims.
```

```text
Audit this for AI-writing patterns without rewriting it.
```

The local audit explains each finding and returns a nonzero status when it finds something to review:

```bash
python scripts/audit_text.py draft.md
python scripts/audit_text.py draft.md --json
```

For procedures, guides, and technical explanations, add the technical checks:

```bash
python scripts/audit_text.py guide.md --mode technical
```

Technical mode uses general clarity principles associated with ASD-STE100. It is not a compliance checker and does not bundle the standard's controlled dictionary.

## Personalize

Copy `references/voice-profile-template.md` to a private location, fill it with evidence from your own approved writing, and point your agent instructions to it. Keep private emails, DMs, customer details, and internal drafts out of public repositories.

Copy `assets/forbidden-patterns.md` to a private path, then add phrases or structures you have rejected in real drafts:

```bash
mkdir -p ~/.config/your-voice
cp assets/forbidden-patterns.md ~/.config/your-voice/forbidden.md
python scripts/audit_text.py draft.md
```

The auditor loads that default file automatically. Pass `--forbidden PATH` to add another file or `--no-default-forbidden` to skip the default. See `references/forbidden-patterns.md` for the small file format.

## Continuous improvement

The scheduled GitHub workflow searches for candidate public skills and research once a week. It produces a report for review. It never auto-merges a new writing rule. Every adoption needs provenance, a license check, an eval, and human review.

## Credits

Your Voice stands on excellent work by Blake Anderson, Hardik Pandya, Peter Yang, Wikipedia's WikiProject AI Cleanup, and product ideas demonstrated by Stanley, Every's Spiral, and Dan Koe's Eden. See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for exact links and how each source influenced this skill.

## License

MIT. See [LICENSE](LICENSE).
