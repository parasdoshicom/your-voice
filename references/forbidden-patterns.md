# Personal forbidden patterns

Your dislikes are part of your voice profile. Keep them in a private file that can change as you approve and reject drafts. Do not publish private examples just to configure the skill.

## File format

The local auditor accepts literal text and Python regular expressions:

```text
# ~/.config/your-voice/forbidden.md
literal: Here's the thing.
literal: And that matters.
regex: \bseamless(?:ly)?\b
```

Blank lines and lines that start with `#` are ignored. A `- ` prefix is optional, so the rules can remain a normal Markdown list.

The auditor loads `~/.config/your-voice/forbidden.md` automatically when it exists. Pass another file one or more times when a project needs its own rules:

```bash
python scripts/audit_text.py draft.md \
  --forbidden ./project-forbidden.md
```

Use `--no-default-forbidden` to skip the default file for one run.

Add a pattern only after you reject it in real writing. Record the preferred fix in your private voice profile when the replacement reflects a durable preference. A forbidden file is a review aid, not a claim that any matching sentence came from AI.
