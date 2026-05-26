# EXP-0001: Template Experiment

Status: run

Question:

Can the template experiment record command, output, environment, and
interpretation in a reproducible way?

Hypothesis:

The experiment runner should produce a JSON output file and environment
metadata without making a mathematical claim.

Plan:

Run `run.py` through `scripts/run_experiment.py`.

Tools:

- Python standard library.

Inputs:

- No mathematical input.

Run command:

```text
python scripts/run_experiment.py EXP-0001-template
```

Expected output:

`output/results.json`, `output/stdout.txt`, `output/stderr.txt`, and
`output/environment.json` are created.

Actual output:

The template runner completed successfully and wrote:

- `output/results.json`
- `output/stdout.txt`
- `output/stderr.txt`
- `output/environment.json`

Interpretation:

This is a template smoke test for the experiment ledger.

Claims affected:

- `CLAIM-0001-template`: no mathematical support; template metadata only.

Limitations:

This experiment proves nothing mathematical.

Reproducibility notes:

The command should be run from the repository root.
