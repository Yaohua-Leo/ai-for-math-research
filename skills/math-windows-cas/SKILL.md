---
name: math-windows-cas
description: Use for Windows-native CAS and numerical tools in this workspace, including Maple CLI, WolframScript, MATLAB batch mode, Maxima, Julia, Rscript, and Octave, while respecting license and reproducibility caveats.
---

# Math Windows CAS

Use this skill when a task needs a Windows-native symbolic, numerical, or
statistical route listed in `tools/registry.yaml`.

Workflow:

1. Pick the smallest adequate tool from the registry.
2. Prefer command-line or batch mode; do not start GUI sessions for
   reproducible evidence.
3. Before execution, check whether the tool is marked `licensed` or `expensive`.
4. Save scripts, inputs, and outputs under `experiments/<EXP-ID>/`.
5. For claim evidence, distinguish exact symbolic output from numerical output.

Evidence boundary:

- Maple, WolframScript, and Maxima may produce `exact-computation` evidence when
  scripts and assumptions are saved.
- MATLAB, R, Octave, numpy/scipy, and floating-point Julia output is usually
  `numerical-evidence`.
- Licensed tools can support local research records but should not become hidden
  requirements for default validation.

Runner:

```powershell
python scripts/run_windows_cas.py maple-cli --mode smoke --dry-run
python scripts/run_windows_cas.py wolframscript --mode smoke --output experiments/<EXP-ID>/output/wolfram-smoke.json
```

Reviewed reference:

- `tools/registry.yaml` records the reviewed MATLAB skill source and license.
  This workspace uses its own registry routes and does not install third-party
  skills automatically.
