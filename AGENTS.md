# AGENTS.md

This repository supports AI-assisted mathematical research. The goal is to help
models work like careful research collaborators: explicit assumptions,
reproducible computations, honest uncertainty, and useful reports.

## Non-Negotiable Rules

1. Do not fabricate mathematical results.
2. Do not fabricate references.
3. Do not mark a claim as proved unless a proof is present and checked.
4. Do not turn numerical or computational evidence into a theorem.
5. Do not silently change assumptions.
6. Do not delete failed experiments; mark them `failed`, `obsolete`, or
   `blocked`.
7. Every nontrivial computation must be reproducible from files under
   `experiments/`.
8. Every major mathematical assertion must appear in `claims/`.
9. Do not store licenses, API keys, credentials, or private account data in
   this repository.

## Default Agent Workflow

For every nontrivial task:

1. Read `problem/problem.md`, `PLAN.md`, `tools/tools.md`, and relevant claims.
2. Restate the mathematical goal.
3. List assumptions and possible failure modes.
4. Write or update a plan before running experiments.
5. Use the strongest available exact tool before floating-point computation.
6. Save all computational work under `experiments/`.
7. Never convert computational evidence into a theorem without proof.
8. Update affected claims.
9. End with a report that distinguishes:
   - proved,
   - experimentally supported,
   - conjectural,
   - refuted,
   - blocked.

## Claim Status Vocabulary

- `idea`: possible direction, not yet shaped.
- `conjecture`: precise enough to test or prove.
- `plausible`: supported by examples or partial arguments.
- `proof-draft`: a proof exists but has unchecked gaps.
- `checked`: proof or verification has been checked against assumptions.
- `refuted`: counterexample or contradiction found.
- `blocked`: progress requires missing input, theory, or tooling.
- `abandoned`: intentionally no longer pursued.

## Experiment Status Vocabulary

- `planned`: documented but not ready to run.
- `runnable`: command and inputs are ready.
- `run`: command has been run and outputs are recorded.
- `failed`: run failed; failure is recorded.
- `obsolete`: superseded by a later experiment.
- `blocked`: cannot run because a dependency is missing.

## Computational Rules

1. Prefer exact arithmetic whenever possible.
2. Prefer rational or symbolic examples before floating-point examples.
3. Record the command, inputs, outputs, environment, and interpretation.
4. If an experiment fails, keep the failure evidence.
5. Do not run expensive or external-tool experiments by default; check metadata
   by default and run only explicitly selected experiments.
6. Before relying on a local tool, check `tools/local-tools.md` and verify the
   command in the current environment.

## Verification

Run these checks before claiming the workspace is healthy:

```powershell
python scripts/check_claims.py
python scripts/check_experiments.py
python scripts/check_reports.py
python scripts/make_index.py
python -m unittest discover -s tests
```

If `ruff` is available, also run:

```powershell
python -m ruff check .
```
