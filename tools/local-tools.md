# Local Tools

This file records a machine-specific tool snapshot. Re-check paths and
versions before relying on them, especially after upgrades or PATH changes.

Last checked: 2026-05-26, Asia/Shanghai.

Do not record licenses, API keys, account details, or credentials here.

| Tool | Status | Command | Intended use | Caveats |
| --- | --- | --- | --- | --- |
| Python | verified | `python --version` | default scripting and validation | prefer exact arithmetic |
| pytest or unittest | optional | `python -m unittest discover -s tests` | regression checks | this template uses unittest only |
| ruff | optional | `python -m ruff check .` | style checks | not required for runtime |
| SymPy | optional | `python -c "import sympy"` | exact symbolic computation | verify availability first |
| Sage | optional | `sage -c "print(2+2)"` | exact algebra | path is machine-specific |
| GAP | optional | `gap -q` | finite groups and representations | verify standalone or Sage route |
| Singular | optional | `Singular` | polynomial and Groebner computations | verify path |
| Macaulay2 | optional | `M2` | commutative algebra | verify path |
| Lean | optional | `lean --version` | formalization | not part of default checks |
| Rocq or Coq | optional | `rocq --version` | formalization | not part of default checks |
| Isabelle | optional | `isabelle version` | formalization | not part of default checks |
| Agda | optional | `agda --version` | dependent type experiments | not part of default checks |
