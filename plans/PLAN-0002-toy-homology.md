---
schema_version: 1
id: PLAN-0002-toy-homology
status: complete
claims:
  - CLAIM-0002-toy-homology
experiments:
  - EXP-0002-toy-homology
last_updated: "2026-06-01"
---
# PLAN-0002-toy-homology: Toy Homology Case Study

## Goal

Demonstrate a complete claim, plan, experiment, and report chain without
introducing domain-specific mathematics.

## Assumptions

- Use a finite-dimensional chain complex over `Q`.
- Use exact rational arithmetic.
- Keep the example mathematically trivial so the workflow is the point.

## Claims Affected

- `CLAIM-0002-toy-homology`

## Experiments Needed

- `EXP-0002-toy-homology`

## Tool Plan

- Run a small Python exact-linear-algebra script.
- Record command output and reproducibility metadata through
  `scripts/run_experiment.py`.

## Failure Modes

- The computation writes output that is not JSON.
- The experiment metadata does not point back to the checked claim.
- The report overstates the computation beyond the toy example.

## Exit Criteria

- The experiment output exists and is valid JSON.
- The claim is checked with fully verifiable exact-computation evidence.
- The report distinguishes proof and computation.
