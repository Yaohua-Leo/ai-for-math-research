# Local Tools

This file is the human-readable companion to `tools/registry.yaml`. The
registry is authoritative for machine checks; this file explains the local
snapshot and caveats.

Last checked source snapshot: 2026-05-24, Asia/Shanghai.
Imported from:

```text
D:\learning\(co)homology_of_Jordan\codex\local-math-tools.md
```

Do not record licenses, API keys, account details, or credentials here.

## Verified Local Routes

| Tool id | Route | Intended use | Caveat |
| --- | --- | --- | --- |
| `python` | Windows native | default exact runner | prefer exact arithmetic |
| `python-scientific-stack` | Windows native | SymPy, numpy, scipy, networkx | floats are numerical evidence |
| `ipython-jupyter` | Windows native | exploratory notebooks | reusable evidence must move under `experiments/` |
| `matlab` | Windows native batch | numerical checks, visualization | licensed and heavy; not default |
| `maple-cli` | Windows native CLI | symbolic/exact checks | licensed; save scripts and assumptions |
| `wolframscript` | Windows native CLI | symbolic/exact checks | licensed; do not store license data |
| `sagemath-wsl` | WSL `bash -lc` | exact algebra | quote-sensitive route |
| `gap-sage` | Sage interface | GAP through Sage | not standalone GAP |
| `singular-sage` | Sage interface | Singular through Sage | not standalone Singular |
| `gap-wsl` | WSL conda env | direct GAP scripts | not on Windows PATH |
| `singular-wsl` | WSL conda env | direct Singular scripts | not on Windows PATH |
| `maxima` | Windows absolute path | symbolic CAS backup | use absolute path |
| `julia` | Windows native | Julia exact/numerical checks | native OSCAR does not load on Windows |
| `oscar-wsl` | WSL Julia | commutative algebra and AG | startup can be slow |
| `macaulay2-wsl` | WSL `M2-codex` wrapper | commutative algebra and AG | use wrapper, not extracted `M2` |
| `rscript` | Windows absolute path | statistics/plotting | not on current shell PATH |
| `octave` | Windows CLI | MATLAB-like numerical checks | CLI mode only |
| `lean` | Windows elan | Lean formalization | version check is not proof evidence |
| `lake` | Windows elan | Lean project builds | build logs needed for evidence |
| `rocq` | Windows Rocq Platform | Rocq/Coq formalization | prefer `rocq compile` for proof files |
| `isabelle-wsl` | WSL install | Isabelle sessions | needs session files before builds |
| `agda-wsl` | WSL install | Agda type checking | user-local standard library config |
| `ghc-cabal-wsl` | WSL GHCup | Agda backend support | support tool, not math evidence |
| `aristotle-cli` | Windows venv | external Lean assistant | needs user credentials; never store keys |

## Not Configured

| Tool id | Status | Caveat |
| --- | --- | --- |
| `magma-web` | web fallback only | small non-private checks only; not durable local evidence |

## Runner Commands

Dry-run routes without executing tools:

```powershell
python scripts/run_math_tool.py python --mode smoke --dry-run
python scripts/run_wsl_algebra.py sagemath-wsl --mode smoke --dry-run
python scripts/run_windows_cas.py wolframscript --mode smoke --dry-run
python scripts/run_formal_tool.py lean --mode version --dry-run
```

Capture selected smoke metadata under an experiment:

```powershell
python scripts/run_math_tool.py python --mode smoke --output experiments/<EXP-ID>/output/python-smoke.json
```

Default validation checks metadata only. External smoke checks are explicit so
licensed or expensive tools are never run accidentally.
