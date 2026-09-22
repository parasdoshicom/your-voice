# Two-stage concision experiment

See [the report](../../reports/2026-09-22-concision-rerun.md) for results and limitations. Both stages failed their predeclared 2× target. Stage 2 tests the released policy; stage 1 is retained as a failed development revision.

Each stage stores source cases, policy snapshots, exact generation prompts, outputs, configuration manifests, blind mappings, two independent model reviews, merged records, and recomputed summaries. No raw CLI diagnostics or credentials are included. All examples are synthetic.

`run_experiment.py` launches six authenticated Codex CLI sessions and can consume account usage. Copy a stage directory to a temporary directory before running it so its new outputs do not overwrite the archived evidence. The script uses CLI defaults; compare the new manifest's resolved model/settings with the archived manifest before treating runs as comparable. It does not regenerate reviewer judgments. The disabled skill path in its command is specific to the original host; adjust it for your installation. Common host context is not fully archived or guaranteed identical across machines.

`prepare_review.py` reconstructs blinded review input and draft records. It intentionally leaves reviews absent: judgments must be performed separately. Do not run it over an archived merged record unless you intend to discard its locally stored review fields. The summary script in the repository root fails the quality gate when reviews are missing.

Regression probes in stage 2 are separate known examples and are excluded from the paired comparison. The manifests record six comparison sessions per stage; the two regression outputs came from one additional session using the same CLI flags/model default and final policy.
