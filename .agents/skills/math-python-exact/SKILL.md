---
name: math-python-exact
description: Use for exact Python mathematical computation in this research workspace, especially SymPy, fractions, integer linear algebra, finite examples, toy experiments, and any task that should produce reproducible experiment evidence under experiments/.
---

# Math Python Exact

Use Python when the computation can be expressed with exact integers, rationals,
finite combinatorics, or symbolic algebra without introducing a heavier CAS.

Workflow:

1. Check `tools/registry.yaml` for the `python` or `python-scientific-stack`
   route.
2. Put nontrivial code in an experiment directory, not in the chat transcript.
3. Prefer `fractions.Fraction`, `decimal`, `sympy`, or integer algorithms over
   floats when the result may affect a claim.
4. Run experiments through `python scripts/run_experiment.py <EXP-ID>` when the
   experiment has a ledger entry.
5. Record output JSON, stdout/stderr, hashes, and interpretation before touching
   claim status.

Evidence boundary:

- Exact finite computation may be `exact-computation`.
- Random or sampled finite checks are `finite-experiment`.
- Floating-point numpy/scipy results are `numerical-evidence`.
- No computation proves a theorem unless the claim also has a checked proof or a
  fully verifiable exact computation marked in the claim evidence.

Runner:

```powershell
python scripts/run_math_tool.py python --mode smoke --dry-run
python scripts/run_math_tool.py python --mode smoke --output experiments/<EXP-ID>/output/python-smoke.json
```
