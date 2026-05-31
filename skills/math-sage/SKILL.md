---
name: math-sage
description: Use for SageMath-based exact algebra in this workspace, including Sage through WSL, Sage interfaces to GAP or Singular, finite rings, polynomial rings, matrices, homology toy cases, and quote-sensitive Sage one-liners.
---

# Math Sage

Use Sage when Python exact arithmetic is not enough and the task benefits from
Sage's algebra libraries or its interfaces to GAP and Singular.

Workflow:

1. Read `tools/registry.yaml` entries `sagemath-wsl`, `gap-sage`, and
   `singular-sage`.
2. Use the registry runner or the WSL route from the registry; avoid ad hoc
   PowerShell quoting for Sage one-liners.
3. Put `.sage` scripts or generated Python code under the relevant
   `experiments/<EXP-ID>/` directory.
4. Capture stdout/stderr and a machine-readable `output/results.json` when the
   result may affect claims.
5. Keep Sage interface evidence separate from standalone GAP or Singular
   evidence; record the actual route used.

Evidence boundary:

- Exact Sage computations can be `exact-computation` if all inputs and scripts
  are saved.
- Sage-to-GAP or Sage-to-Singular interface output is still evidence from the
  Sage route and should say so in the experiment metadata.

Runner:

```powershell
python scripts/run_wsl_algebra.py sagemath-wsl --mode smoke --dry-run
python scripts/run_wsl_algebra.py gap-sage --mode smoke --output experiments/<EXP-ID>/output/gap-sage-smoke.json
```

Reviewed reference:

- `tools/registry.yaml` records the reviewed SageMath skill source and license.
  This workspace adapts only the idea of a dedicated runner; it does not install
  or vendor the third-party skill.
