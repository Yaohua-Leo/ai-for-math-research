# Status Vocabulary

Use these status values exactly.

## Claims

- `idea`: possible direction, not yet shaped.
- `conjecture`: precise enough to test or prove.
- `plausible`: supported by examples or partial arguments.
- `proof-draft`: a proof exists but has unchecked gaps.
- `checked`: proof or verification has been checked against assumptions.
- `refuted`: counterexample or contradiction found.
- `blocked`: progress requires missing input, theory, or tooling.
- `abandoned`: intentionally no longer pursued.

## Experiments

- `planned`: documented but not ready to run.
- `runnable`: command and inputs are ready.
- `run`: command has been run and outputs are recorded.
- `failed`: run failed; failure is recorded.
- `obsolete`: superseded by a later experiment.
- `blocked`: cannot run because a dependency is missing.

## Reports

- `draft`: incomplete synthesis.
- `complete`: current synthesis is complete for its stated scope.
- `superseded`: intentionally replaced by a newer report.
- `blocked`: cannot be completed because input, proof, experiment, or tooling is
  missing.

## Conservative Defaults

- New claims usually start as `idea` or `conjecture`.
- Computation can support `plausible` or `refuted`; it does not by itself imply
  `checked` unless the computation is exact, fully reproducible, and the claim
  is exactly the computed finite statement.
- New experiments start as `planned` unless their command and inputs are ready.
- Reports start as `draft` unless all sections are complete for their scope.

