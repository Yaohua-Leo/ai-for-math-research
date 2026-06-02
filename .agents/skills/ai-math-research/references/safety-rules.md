# Safety Rules

Use this reference when deciding what a claim, experiment, or report is allowed
to say.

## Mathematical Honesty

- A theorem requires a proof or a checked formal/exact verification.
- Numerical or sampling evidence is not a theorem.
- A failed or inconclusive computation is useful evidence and must be recorded
  honestly.
- Do not introduce new assumptions to make a proof or computation work without
  recording them in the artifact metadata/body.

## Evidence Boundaries

- `human-proof`: proof text is present and checked by the agent or user.
- `formal-check`: a formal system checked the statement or source file.
- `exact-computation`: exact arithmetic or symbolic computation was recorded.
- `finite-experiment`: finite bounded check; state the bound.
- `numerical-evidence`: floating-point or heuristic evidence only.
- `literature-reference`: reference support only; do not fabricate citations.
- `counterexample`: refutes or narrows a claim; record the construction.

## Claim Status Guardrail

Do not mark a claim `checked` unless all of these are true:

1. The statement is precise.
2. The assumptions are explicit.
3. The proof or verification exactly matches the statement.
4. Any computation is reproducible from files under `experiments/`.
5. The artifact records what was checked and what remains unchecked.

## Secrets

Never write API keys, license keys, private account data, Codex auth files, or
raw credential material to this repository. Mention environment variable names
only when setup guidance requires them.

