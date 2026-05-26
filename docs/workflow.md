# Workflow

## Main Loop

1. Read the problem statement, current plan, tool registry, and affected
   claims.
2. State assumptions and failure modes.
3. Write or update a plan.
4. Create or select claims.
5. Create an experiment directory if computation is needed.
6. Run the selected tool.
7. Save input, command, output, environment, and interpretation.
8. Update affected claim statuses.
9. Write a report.

## Artifact Rule

Every nontrivial research action must leave an artifact:

- planning belongs in `plans/`,
- mathematical assertions belong in `claims/`,
- computations belong in `experiments/`,
- synthesis belongs in `reports/`,
- tool knowledge belongs in `tools/`.

## Default Checks

The default checks validate the ledger shape. They do not run expensive
experiments.

```powershell
python scripts/check_claims.py
python scripts/check_experiments.py
python scripts/check_reports.py
python scripts/make_index.py
python -m unittest discover -s tests
```
