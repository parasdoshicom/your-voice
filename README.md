# Your Voice

An agent skill for writing that says what matters and still sounds like the writer. It helps choose the point before drafting, preserves meaning during edits, and removes unnecessary material without stripping warmth, explanation, or personality.

Use it for replies, updates, essays, teaching, and spoken answers. It supports the Agent Skills `SKILL.md` format used by Codex and other compatible agents. A skill supplies editorial guidance; it does not replace the writer's judgment or guarantee a voice match.

## Start here

```text
Answer this in one sentence, keeping the caveat.
```

```text
Shorten this note. Keep the apology and the invitation.
```

```text
Fix only the punctuation. Keep my words and order.
```

```text
Draft an explanation from these facts for a beginner. Use a labeled hypothetical example.
```

```text
Review this without rewriting it. Tell me which parts bury the point.
```

The core skill handles short work on its own. Longer work loads only the relevant reference. It selects before drafting and reviews afterward; it does not impose a checklist, a short word count, or an executive-summary structure on every piece.

## Install or update

Clone this repository and run:

```bash
./scripts/install.sh
```

The installer links the canonical checkout into the user skill roots for Codex and Hermes. If OpenClaw already exists, it also links its global root and discovered agent Codex homes. It does not install OpenClaw. For other agents, link or copy the repository into the supported skill directory as `your-voice`.

Set the default once in the agent's shared instructions:

```text
For human-facing prose, apply Your Voice by default. Use its instructions as
one writing policy; do not stack or restate generic prose-cleanup rules.
```

For a linked installation, pulling updates in the canonical checkout updates the skill. Check supported host links with:

```bash
python3 scripts/check_install.py
```

## Where each concern lives

| File | Responsibility |
|---|---|
| [SKILL.md](SKILL.md) | Editorial priorities, narrow task selection, and reference routing |
| [Writing workflows](references/writing-workflows.md) | Generate, preserve, condense, review, and technical prose |
| [Patterns](references/patterns.md) | Optional symptom checklist; intentional matches can stay |
| [Human expression](references/human-expression.md) | Spoken delivery and rehearsal |
| [Voice profile template](references/voice-profile-template.md) | Evidence-based personalization |
| [Paras profile](profiles/paras-doshi.md) | Paras's baseline; specialist course choices load separately |
| [Approval learning](references/approval-learning-loop.md) | Accepted and rejected decisions, with rules for promotion |
| [Evaluation](references/evaluation.md) | Behavioral comparisons and calibrated judge evaluation |
| [Discovery](references/discovery-loop.md) | Public-source review and adoption |

## Personalize

Copy [the profile template](references/voice-profile-template.md) to a private location and point your agent to it. Start with a few approved samples in the channels you use. Record what the writer notices, how they address different people, which edits they reject, and which rough edges should survive. Leave traits unknown when evidence is missing.

Keep private emails, messages, customer details, and internal drafts outside this public repository. The [approval learning loop](references/approval-learning-loop.md) explains how feedback becomes a contextual or durable preference. Engagement statistics alone do not define voice.

Optional private rejection lists use [this format](references/forbidden-patterns.md). The template's examples are commented out until the writer chooses them:

```bash
mkdir -p ~/.config/your-voice
cp assets/forbidden-patterns.md ~/.config/your-voice/forbidden.md
```

## Check a draft

```bash
python3 scripts/audit_text.py draft.md
python3 scripts/audit_text.py guide.md --mode technical
python3 scripts/audit_text.py answer.md --mode spoken
```

Add `--json` for structured findings. Exit status 1 means there are candidates to review, not that the draft failed. The auditor cannot judge truth, taste, social fit, or whether a detail earns its space. It masks common code, URL, and table forms; quotations and other protected spans still need editorial care. Do not edit toward zero findings.

Technical mode uses general clarity principles inspired by ASD-STE100; it does not certify compliance. Spoken mode flags long sentences and written-only transitions; actual delivery needs rehearsal.

## Validate changes

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_evals.py evals/benchmark.json
python3 scripts/score_judges.py evals/labels.example.jsonl --split test
```

The [September 22 review](reports/2026-09-22-refresh-review.md) records the repo audit and a five-case independent writing comparison, including its limits. The [Stanley follow-up](reports/2026-09-22-stanley-review.md) records external feedback, revisions, and targeted preservation checks.

Unit tests validate tools, and the benchmark validator checks case structure. Neither proves better writing. [Evaluation](references/evaluation.md) describes isolated baseline/treatment runs, blind review, human holdouts, and reporting limits. The synthetic judge-label file checks format, not production calibration.

An optional live Codex harness is configured in `.plugin-eval/benchmark.json`:

```bash
plugin-eval benchmark . --config .plugin-eval/benchmark.json
```

Review its model and scenarios before running it. Deterministic output checks cover selected boundaries and facts; human meaning and voice judgments remain separate.

The scheduled discovery workflow creates a review queue, never automatic rule adoption. See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for sources and influence boundaries, and [LICENSE](LICENSE) for the MIT license.
