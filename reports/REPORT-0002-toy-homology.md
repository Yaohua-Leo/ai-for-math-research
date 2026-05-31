---
schema_version: 1
id: REPORT-0002-toy-homology
status: complete
claims:
  - CLAIM-0002-toy-homology
experiments:
  - EXP-0002-toy-homology
last_updated: "2026-06-01"
---
# REPORT-0002-toy-homology: Toy Homology Case Study

## Goal

Demonstrate the upgraded ledger on a complete, reproducible, domain-neutral
toy example.

## Proved

- `CLAIM-0002-toy-homology`: the chain complex `0 -> Q -> Q -> 0` with
  identity differential has zero homology in degrees zero and one.

## Supported By Computation

- `EXP-0002-toy-homology` computes the rank of the differential exactly and
  writes `output/results.json`.

## Conjectural

- Nothing conjectural in this toy case.

## Failed Or Refuted

- Nothing failed or refuted.

## Blocked

- Nothing blocked.

## Next Steps

- Use this artifact chain as the smallest regression case for future ledger
  schema changes.

## Artifacts

- Claims:
  - `claims/CLAIM-0002-toy-homology.md`
- Experiments:
  - `experiments/EXP-0002-toy-homology/`
