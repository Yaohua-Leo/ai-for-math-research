# Tool Contracts

Tool contracts describe when a class of tool is appropriate. They do not force
a fixed pipeline.

## Exact Linear Algebra

Preferred:

1. Python `fractions` or exact integer arithmetic.
2. SymPy.
3. Sage, Maple, or Wolfram Language.

Do not use floating point unless the experiment is explicitly numerical.

The default available adapter is `python-exact-runner`, which routes
experiments through `scripts/run_experiment.py` and records stdout, stderr,
JSON output, hashes, and environment metadata.

For registry-level smoke checks, use:

```powershell
python scripts/run_math_tool.py python --mode smoke --dry-run
```

## Commutative Algebra

Preferred:

1. Sage.
2. Singular.
3. Macaulay2.
4. OSCAR.

Record input scripts and output files under the experiment directory.

Use `scripts/run_wsl_algebra.py` for WSL-routed Sage, GAP, Singular,
Macaulay2, or OSCAR smoke checks.

## Finite Groups And Representations

Preferred:

1. GAP.
2. Sage GAP interface.

Record group definitions, library identifiers, and package assumptions.

## Numerical Experiments

Numerical experiments must state:

- precision,
- random seeds,
- stopping criteria,
- whether results are heuristic.

Numerical evidence does not prove a theorem by itself.

## Formal Proof

Preferred:

1. Lean for mathlib-adjacent reusable facts.
2. Rocq or Coq for constructive or type-theoretic developments.
3. Isabelle for structured classical proofs.
4. Agda for dependent type experiments.

Formal output should identify the theorem name, source file, command, and tool
version.

Use `scripts/run_formal_tool.py` for version checks. A version check is not
formal evidence until paired with checked proof files and build logs.
