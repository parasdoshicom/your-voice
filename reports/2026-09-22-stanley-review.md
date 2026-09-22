# Stanley review and follow-up — 2026-09-22

## What was reviewed

Stanley's authenticated web chat returned a review of public commit `c7d9341a4cf9ab41afbc5e12aeefcaf9e7b95274`. It reported retrieving SKILL.md, README.md, the writing workflows, human expression, patterns, Paras profile, and approval-learning reference. Its quoted passages match that revision. It reported that private profile/instruction context was unavailable; this is a public instruction review, not a verified match to Paras's private voice samples.

This review was requested by Paras. It did not authorize publishing social content, updating Stanley Brain, or changing accounts. The response was received through the normal web interface, not MCP.

## Decisions from the review

| Finding | Applied change | Limit |
|---|---|---|
| The core detail-selection test could encourage over-compression | Explicitly preserve needed explanation, warmth, rhythm, and emphasis | No mandate to make every draft longer or warmer |
| The intensifier checklist could erase honest emphasis | Flag unearned emphasis or substitution for evidence; preserve intended emphasis | Do not add feelings the writer did not supply |
| The fragment example prescribed mechanical smoothing | Cut or combine only when useful; protect distinct meaning and deliberate rhythm | Fragmented filler remains reviewable |
| Spoken rules appeared in two references | Replace the pattern section with a pointer to the delivery reference | Written prose does not inherit speech-only constraints |
| Every learning record required a rule and future test | Use a compact decision, reason, and scope; make rules/tests conditional | Existing artifact/channel/durable promotion gates remain |

These are agent-implemented revisions under the user's request, not a claim that the human approved a new personal preference. An independent agent checked both the findings and the resulting diff and reported no actionable regression.

## Behavioral checks

A separate skill-loaded agent completed three synthetic requests:

1. It preserved “I really miss you. Can we talk Sunday?” without removing honest emphasis.
2. It preserved “No fanfare. Just the two of us. That was enough.” in a typo-only edit.
3. It recorded an apology's removed joke as a decision for that apology only, with no standing preference established.

All three satisfy their supplied constraints. This is a targeted smoke check, not a blind efficacy study. The model-agnostic benchmark now has 22 cases; the deterministic suite remains 45 tests. The earlier five-case comparison remains documented separately and is not rerun evidence for this revision.

## MCP connection remains blocked

The configured endpoint is correct: `https://xapi.getstanley.ai/mcp`. A user-approved Codex OAuth login failed with:

```text
Authorization server issuer mismatch: expected https://xapi.getstanley.ai, received https://x.getstanley.ai
```

Public protected-resource metadata advertises `https://xapi.getstanley.ai` as the authorization server, and its authorization-server metadata uses the same issuer while sending consent to `https://x.getstanley.ai/mcp/consent`. A subsequent fresh CLI status query reported `not_logged_in`, despite a browser callback page reporting authentication complete. The connection was not marked healthy and issuer validation was not disabled.

Provider-side correction: the authorization response issuer must match the advertised issuer, or discovery must consistently name the actual issuer. After correction, repeat normal OAuth login and verify an authenticated MCP tool call. No credentials or callback authorization codes are included here.
