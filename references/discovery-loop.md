# Discovery and adoption loop

Your Voice may discover new ideas automatically. It must never adopt them automatically.

## Discovery

The weekly workflow searches GitHub for agent skills related to voice calibration, editing, human writing, and AI-writing patterns. The report is a queue, not a recommendation.

Also consider primary research and official product pages when they expose a useful mechanism. Do not scrape paid content or reconstruct proprietary prompts.

## Triage

For every candidate, record:

- author and canonical URL;
- retrieved date and pinned commit or release when available;
- license;
- the exact gap it might address;
- whether the idea concerns truth, voice, structure, channel fit, or evaluation;
- privacy and supply-chain risk.

Reject candidates that optimize detector evasion, strip provenance, insert fake mistakes, fabricate experience, or require sending private writing to an unapproved service.

## Adoption

1. Write a failing eval that exposes the current gap.
2. Summarize the smallest proposed rule in original wording.
3. Run all existing evals.
4. Check that the rule does not flatten a protected voice signal.
5. Add attribution.
6. Require human review and a normal pull request.

## Rollback

Every adopted rule must be easy to remove. If approved writing becomes blander, less accurate, or less recognizable, revert the rule before tuning it.
