---
name: math-formal-provers
description: Use for formal proof tooling in this workspace, including Lean/Lake, Rocq or Coq Platform, Isabelle through WSL, Agda through WSL, GHC/Cabal support checks, and Aristotle CLI, with strict separation between version checks and formal evidence.
---

# Math Formal Provers

Use this skill when a claim needs formalization or when a formal tool route must
be checked before creating proof artifacts.

Workflow:

1. Read the relevant formal tool entry in `tools/registry.yaml`.
2. Run version or smoke checks through `scripts/run_formal_tool.py`.
3. Place proof sources under a dedicated formal directory or experiment
   directory before using them as evidence.
4. Capture build logs and exact commands; a version check is not evidence for a
   mathematical claim.
5. Update claim evidence only when the formal file has been checked by the
   corresponding compiler/build command.

Evidence boundary:

- Lean, Rocq, Isabelle, and Agda build success can be `formal-check` evidence
  only for the checked proof files.
- Lake, GHC, and Cabal checks are support evidence unless they build proof
  sources.
- Aristotle requires user-level credentials; never store keys in the repository.

Runner:

```powershell
python scripts/run_formal_tool.py lean --mode version --dry-run
python scripts/run_formal_tool.py rocq --mode smoke --output experiments/<EXP-ID>/output/rocq-smoke.json
```

Reviewed references:

- `tools/registry.yaml` records reviewed Lean, Rocq, Agda, and R-related skill
  sources and license metadata. They are references only unless separately
  installed and reviewed.
