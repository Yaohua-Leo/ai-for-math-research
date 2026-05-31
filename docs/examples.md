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

The repository also includes a complete toy case:

- `claims/CLAIM-0002-toy-homology.md`
- `plans/PLAN-0002-toy-homology.md`
- `experiments/EXP-0002-toy-homology/`
- `reports/REPORT-0002-toy-homology.md`

Run it with:

```powershell
python scripts/run_experiment.py EXP-0002-toy-homology
```

This case proves only a trivial finite-dimensional chain-complex statement.
Its purpose is to exercise the full ledger and reproducibility workflow.

Dry-run a registry tool route:

```powershell
python scripts/run_wsl_algebra.py sagemath-wsl --mode smoke --dry-run
```

Capture a selected smoke check under an experiment:

```powershell
python scripts/run_formal_tool.py lean --mode version --output experiments/EXP-0002-toy-homology/output/lean-version.json
```

A version check is environment evidence only. It is not proof evidence unless a
formal source file is also checked by the corresponding build command.
