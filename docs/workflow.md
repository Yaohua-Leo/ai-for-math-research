# Workflow

## Main Loop

1. Read the problem statement, current plan, tool registry, and affected
   claims.
2. State assumptions and failure modes.
3. Write or update a plan.
4. Create or select claims.
5. Create an experiment directory if computation is needed.
6. Run the selected tool.
7. Save input, command, output, environment, hashes, and interpretation.
8. Update affected claim statuses.
9. Write a report.

## Artifact Rule

Every nontrivial research action must leave an artifact:

- planning belongs in `plans/`,
- mathematical assertions belong in `claims/`,
- computations belong in `experiments/`,
- synthesis belongs in `reports/`,
- tool knowledge belongs in `tools/`.

Each claim, plan, experiment, and report starts with YAML frontmatter. Keep the
frontmatter small and factual: IDs, statuses, dependency lists, evidence
entries, tool commands, and reproducibility fields. Put mathematical discussion
in the Markdown body.

## Default Checks

The default checks validate the ledger shape. They do not run expensive
experiments.

```powershell
python scripts/check_claims.py
python scripts/check_experiments.py
python scripts/check_reports.py
python scripts/check_tools.py
python scripts/make_index.py
python -m unittest discover -s tests
```

`python scripts/make_index.py` also refreshes `CLAIM_GRAPH.md`,
`OPEN_GAPS.md`, `FAILED_EXPERIMENTS.md`, and `NEXT_ACTIONS.md`.

External tool smoke checks are selected explicitly. Use dry-run first:

```powershell
python scripts/run_math_tool.py sagemath-wsl --mode smoke --dry-run
python scripts/run_formal_tool.py lean --mode version --dry-run
```

When a smoke check matters as evidence, write its metadata under the experiment
output directory with `--output`.
