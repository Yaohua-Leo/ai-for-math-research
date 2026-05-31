---
name: math-commalg
description: Use for commutative algebra and algebraic geometry computation in this workspace, including standalone GAP, Singular, Macaulay2 through WSL, OSCAR through WSL Julia, and Magma web fallback caveats.
---

# Math Commalg

Use this skill for direct GAP, Singular, Macaulay2, OSCAR, or Magma-fallback
workflows.

Workflow:

1. Check `tools/registry.yaml` for the exact tool route and caveats.
2. Prefer WSL wrappers from the registry instead of manually constructing
   PowerShell pipelines.
3. Keep tool-specific scripts under `experiments/<EXP-ID>/input/` or the
   experiment root.
4. Write normalized results to `experiments/<EXP-ID>/output/results.json`.
5. Preserve failed runs as evidence by marking the experiment `failed` instead
   of deleting logs.

Evidence boundary:

- GAP, Singular, Macaulay2, and OSCAR can produce `exact-computation` evidence
  when the script, input, output, command, and environment are captured.
- Magma is `reference-only` here because there is no local configured license or
  reproducible local route.
- OSCAR startup can be slower than small Python/Sage checks; use it when the
  domain library matters.

Runner:

```powershell
python scripts/run_wsl_algebra.py singular-wsl --mode smoke --dry-run
python scripts/run_wsl_algebra.py macaulay2-wsl --mode smoke --output experiments/<EXP-ID>/output/m2-smoke.json
```
