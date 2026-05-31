---
schema_version: 1
id: CLAIM-0002-toy-homology
status: checked
type: theorem
depends_on: []
evidence:
  - type: exact-computation
    path: experiments/EXP-0002-toy-homology/output/results.json
    fully_verifiable: true
assumptions:
  - The chain complex is 0 -> Q -> Q -> 0 with differential [1].
  - Linear algebra is performed exactly over the rational numbers.
last_updated: "2026-06-01"
---
# CLAIM-0002-toy-homology: Toy Acyclic Chain Complex

## Statement

For the finite chain complex `0 -> Q -> Q -> 0` whose only nonzero
differential is the identity map `d_1: Q -> Q`, the homology dimensions are
`H_1 = 0` and `H_0 = 0`.

## Assumptions

- The coefficient field is `Q`.
- The boundary map is the `1 x 1` identity matrix.
- Homology is computed as `ker(d_n) / im(d_{n+1})`.

## Proof Sketch

The differential `d_1` has rank `1`. Its kernel is zero, so `H_1 = 0`.
Its image is all of `Q`, so `H_0 = Q / Q = 0`.

## Known Gaps

- None; this is a finite exact computation with a direct proof.

## References

- Standard definition of homology of a chain complex.

## Computational Evidence

- `experiments/EXP-0002-toy-homology/output/results.json`

## Formalization Status

Not formalized.

## Verification Notes

The supporting experiment computes the rank of the boundary matrix using exact
rational arithmetic and records the zero homology dimensions.
