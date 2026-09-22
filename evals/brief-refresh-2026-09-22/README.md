# Writing-brief and upstream-refresh checks

Ten synthetic cases × three conditions × two repetitions = 60 drafts. This is targeted regression coverage; all conditions passed the recorded checks, so it does not demonstrate incremental effectiveness.

Read [the report](../../reports/2026-09-22-upstream-refresh.md) for source decisions and limitations. `experiment.json` contains outputs, deterministic checks, and independent meaning/contract reviews. `blind-key.json` decodes randomized sample IDs. The model reviewers received requests, source facts, preservation criteria, and shuffled drafts; they did not receive policy or condition identities. Their complete host context/model configuration was not independently captured. Their judgments are not human-calibrated.

The meaning reviewer checked source relationships, conditions, units, claims, quotations, and truthful edit summaries. The contract reviewer checked the actual requested editing scope and output job. Neither graded generic style quality or authorship. These are recorded criteria, not a production judge package.

Run `python3 evals/brief-refresh-2026-09-22/recompute.py --check` from the repository root to verify saved counts. No model calls are made by that command.

To generate new drafts, first copy this directory to a temporary location, then run its `run_experiment.py`. This consumes authenticated Codex usage and selects CLI defaults; compare the new manifest with the archived model/settings. Adapt the original host's disabled-skill path for your installation. Do not overwrite archived evidence. Generation does not regenerate independent reviews. `prepare_review.py` creates ungraded records, replacing any existing merged review fields in that local copy. Raw CLI diagnostics and credentials are not published.
