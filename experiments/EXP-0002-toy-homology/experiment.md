---
schema_version: 1
id: EXP-0002-toy-homology
status: run
tool: python
command:
  - python
  - scripts/run_experiment.py
  - EXP-0002-toy-homology
inputs: []
outputs:
  - output/results.json
  - output/stdout.txt
  - output/stderr.txt
  - output/environment.json
  - output/run-metadata.json
claims_affected:
  - CLAIM-0002-toy-homology
random_seed: null
timeout_seconds: 30
---
# EXP-0002-toy-homology: Exact Homology Smoke Test

## Question

Can a complete toy case record an exact computation that supports a checked
claim?

## Hypothesis

The identity differential on `Q -> Q` has zero kernel in degree one and full
image in degree zero, so both homology dimensions are zero.

## Plan

Run `run.py` through `scripts/run_experiment.py`. The script computes matrix
rank exactly using rational arithmetic and writes `output/results.json`.

## Tools

- Python standard library.

## Inputs

- No external input files.

## Expected Output

- `output/results.json`
- `output/stdout.txt`
- `output/stderr.txt`
- `output/environment.json`
- `output/run-metadata.json`

## Actual Output

The experiment runner records the output files listed above.

## Interpretation

The output verifies the toy chain complex has zero homology in degrees zero
and one. This supports only the stated toy claim.

## Claims Affected

- `CLAIM-0002-toy-homology`

## Limitations

This toy example is a workflow demonstration, not a new mathematical result.

## Reproducibility Notes

Run from the repository root:

```powershell
python scripts/run_experiment.py EXP-0002-toy-homology
```
