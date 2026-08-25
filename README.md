# Your Voice

Your Voice is an agent skill that keeps AI-assisted writing specific, truthful, and recognizably yours.

Most “humanizer” workflows stack several overlapping prompts. They remove the same em dash three times, flatten the writer's quirks, and still miss the harder problem: the draft has no point of view. Your Voice puts voice and evidence first, then runs one consolidated anti-slop pass.

It is designed for Codex, Claude Code, OpenCode, OpenClaw, GitHub Copilot, and other tools that support the Agent Skills `SKILL.md` format.

Version 1.6 adds bottom-up failure discovery and calibrated judge evaluation. Your Voice now separates designed requirements from failures found in real edits, keeps the human comparison rubric out of automated judge prompts, and measures binary judges with TPR and TNR on held-out human labels. It also treats social performance as a channel signal rather than proof of voice.

## What it does

- drafts, edits, or audits human-facing prose;
- prepares interview answers, narration, talks, and voice notes for natural delivery;
- learns from approved writing samples without copying content into the skill;
- separates durable voice from platform habits and relationship-specific registers;
- consolidates compatible rules from Humanizer, Stop Slop, No AI Slop, and related editorial workflows;
- rejects detector gaming, fake mistakes, and invented personal texture;
- runs a provenance-aware weekly discovery loop for new public techniques and newer tracked upstream releases;
- remembers patterns you reject without publishing your drafts;
- learns from approved before-and-after comparisons without treating the external tool as the source of truth;
- offers an optional technical mode for procedures, guides, and explanations;
- includes information-isolated behavioral evals for meaning, social fit, personality, recognition, restraint, and speakability;
- separates top-down requirements from bottom-up failures found in approved edits and rejections;
- validates one binary failure mode per automated judge instead of asking for a vague style score;
- keeps creator-performance data in its proper lane: useful for topic and format tests, insufficient as a voice rule;
- stress-tests prompt-style variation, long-context voice drift, embedded instructions, and protected spans;
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
python3 scripts/audit_text.py draft.md
python3 scripts/audit_text.py draft.md --json
```

For procedures, guides, and technical explanations, add the technical checks:

```bash
python3 scripts/audit_text.py guide.md --mode technical
```

Technical mode uses general clarity principles associated with ASD-STE100. It is not a compliance checker and does not bundle the standard's controlled dictionary.

For words meant to be heard, use spoken mode:

```bash
python3 scripts/audit_text.py answer.md --mode spoken
```

Spoken mode flags long breath groups and written-only transitions. It does not inject filler words or fake mistakes.

## Evaluate behavior

The deterministic audit catches candidates for review. It does not score whether the writing sounds like the person or fits the relationship.

`evals/benchmark.json` contains realistic preserve, condense, generate, spoken, and technical cases. `references/evaluation.md` explains how to run information-isolated baseline-versus-skill comparisons and grade the result without letting style compensate for invented facts.

```bash
python3 scripts/validate_evals.py evals/benchmark.json
```

The benchmark also defines prompt-style, long-context, output-variation, and blind-review stress tests. See `references/evaluation.md` for the protocol and `ATTRIBUTIONS.md` for the primary research behind it.

The human 0-to-2 rubric is for blind comparison across drafts. Automated judges must check one failure mode with binary `Pass` or `Fail` labels and cite evidence. Score a private human-labeled test set with:

```bash
python3 scripts/score_judges.py private-labels.jsonl \
  --split test --min-per-label 50 --min-rate 0.90
```

`evals/labels.example.jsonl` documents the JSONL shape with synthetic rows. Its perfect scores are a format check, not evidence that a real judge is production-ready.

The repository also includes `.plugin-eval/benchmark.json` for live, isolated Codex runs with OpenAI's `plugin-eval` harness. Review the scenarios before running them, then use:

```bash
plugin-eval benchmark . --config .plugin-eval/benchmark.json
```

## Personalize

Copy `references/voice-profile-template.md` to a private location, fill it with evidence from your own approved writing, and point your agent instructions to it. Keep private emails, DMs, customer details, and internal drafts out of public repositories.

For a private forbidden-pattern file, follow `references/forbidden-patterns.md`. Start from `assets/forbidden-patterns.md`.

```bash
mkdir -p ~/.config/your-voice
cp assets/forbidden-patterns.md ~/.config/your-voice/forbidden.md
```

## Continuous improvement

The scheduled GitHub workflow produces a review queue. `references/discovery-loop.md` owns public-source adoption. `references/approval-learning-loop.md` turns human-approved before-and-after reviews into reusable channel and voice decisions. `references/evaluation.md` explains the human-led error-discovery loop and the production judge gate.

## Credits

Your Voice stands on excellent work by Blake Anderson, Hardik Pandya, Peter Yang, Wikipedia's WikiProject AI Cleanup, and newer open-source work on research-backed humanizing and persona evaluation. It also learns from product ideas demonstrated by Gamma, Stanley, Every's Spiral, and Dan Koe's Eden. See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for exact links and how each source influenced this skill.

## License

MIT. See [LICENSE](LICENSE).
