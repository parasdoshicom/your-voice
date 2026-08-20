# Your Voice

Your Voice is an agent skill that keeps AI-assisted writing specific, truthful, and recognizably yours.

Most “humanizer” workflows stack several overlapping prompts. They remove the same em dash three times, flatten the writer's quirks, and still miss the harder problem: the draft has no point of view. Your Voice puts voice and evidence first, then runs one consolidated anti-slop pass.

It is designed for Codex, Claude Code, OpenCode, OpenClaw, GitHub Copilot, and other tools that support the Agent Skills `SKILL.md` format.

Version 1.3 turns approved revisions into a feedback loop. Your Voice records what a writing or design tool improved and what the writer rejected. It applies those decisions before paying for another external pass. The local audit still catches machine-shaped patterns, reads a private forbidden-pattern file, and can apply stricter clarity checks to technical writing.

## What it does

- drafts, edits, or audits human-facing prose;
- learns from approved writing samples without copying content into the skill;
- separates durable voice from platform habits;
- consolidates compatible rules from Humanizer, Stop Slop, No AI Slop, and related editorial workflows;
- rejects detector gaming, fake mistakes, and invented personal texture;
- runs a provenance-aware weekly discovery loop for new public techniques;
- remembers patterns you reject without publishing your drafts;
- learns from approved before-and-after comparisons without treating the external tool as the source of truth;
- offers an optional technical mode for procedures, guides, and explanations;
- includes a public Paras Doshi profile derived from his pre-2023 writing and public LinkedIn work.

## Install

Clone the repository, then run:

```bash
./scripts/install.sh
```

The installer links one canonical checkout into the user skill roots for Codex and Hermes. When OpenClaw is already installed, it also links the same checkout into its global skill root and discovered agent Codex homes. It does not create an OpenClaw installation.

For a single agent, link or copy this repository into that agent's skills directory under the name `your-voice`.

Then add this default once at the highest shared instruction layer. For Codex, use `~/.codex/AGENTS.md` so every repository inherits it:

```text
For human-facing prose, apply Your Voice by default. Your Voice satisfies any
component humanizer, stop-slop, no-ai-slop, or generic prose-cleanup requirement.
Do not restate its pattern rules in repository instructions.
```

Keep repository `AGENTS.md` files for project-specific exceptions only.

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

For a private forbidden-pattern file, follow `references/forbidden-patterns.md`. Start from `assets/forbidden-patterns.md`.

```bash
mkdir -p ~/.config/your-voice
cp assets/forbidden-patterns.md ~/.config/your-voice/forbidden.md
```

## Continuous improvement

The scheduled GitHub workflow produces a review queue. `references/discovery-loop.md` owns public-source adoption. `references/approval-learning-loop.md` turns human-approved before-and-after reviews into reusable channel and voice decisions.

## Credits

Your Voice stands on excellent work by Blake Anderson, Hardik Pandya, Peter Yang, Wikipedia's WikiProject AI Cleanup, and product ideas demonstrated by Stanley, Every's Spiral, and Dan Koe's Eden. See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for exact links and how each source influenced this skill.

## License

MIT. See [LICENSE](LICENSE).
