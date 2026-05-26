# Examples

The default repository includes template artifacts:

- `claims/CLAIM-0001-template.md`
- `plans/PLAN-0001-template.md`
- `experiments/EXP-0001-template/`
- `reports/REPORT-0001-template.md`

Run the template experiment:

```powershell
python scripts/run_experiment.py EXP-0001-template
```

The experiment writes:

- `experiments/EXP-0001-template/output/results.json`
- `experiments/EXP-0001-template/output/stdout.txt`
- `experiments/EXP-0001-template/output/stderr.txt`
- `experiments/EXP-0001-template/output/environment.json`

This demonstrates the ledger mechanism. It does not support a mathematical
claim.
