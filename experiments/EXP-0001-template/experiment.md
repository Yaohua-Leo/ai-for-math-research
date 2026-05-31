---
schema_version: 1
id: EXP-0001-template
status: run
tool: python
command:
  - python
  - scripts/run_experiment.py
  - EXP-0001-template
inputs: []
outputs:
  - output/results.json
  - output/stdout.txt
  - output/stderr.txt
  - output/environment.json
claims_affected:
  - CLAIM-0001-template
random_seed: null
timeout_seconds: 30
---
# EXP-0001-template: Template Experiment

## Question

Can the template experiment record command, output, environment, and
interpretation in a reproducible way?

## Hypothesis

The experiment runner should produce a JSON output file and environment
metadata without making a mathematical claim.

## Plan

Run `run.py` through `scripts/run_experiment.py`.

## Tools

- Python standard library.

## Inputs

- No mathematical input.

## Expected Output

`output/results.json`, `output/stdout.txt`, `output/stderr.txt`, and
`output/environment.json` are created.

## Actual Output

The template runner completed successfully and wrote:

- `output/results.json`
- `output/stdout.txt`
- `output/stderr.txt`
- `output/environment.json`

## Interpretation

This is a template smoke test for the experiment ledger.

## Claims Affected

- `CLAIM-0001-template`: no mathematical support; template metadata only.

## Limitations

This experiment proves nothing mathematical.

## Reproducibility Notes

The command should be run from the repository root.
