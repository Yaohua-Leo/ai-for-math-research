---
name: sagemath-skill
description: Use as a repo-scoped wrapper for SageMath workflow references while routing Sage execution through the WSL registry runner.
---

# SageMath Skill Wrapper

This is a wrapper-only repo skill. The reviewed SageMath listing points to a
source path that was not resolvable during installation, so no upstream skill
content is vendored here.

## Source Reference

- Listing: `https://eliteai.tools/agent-skills/sagemath`
- Candidate repository:
  `https://github.com/majiayu000/claude-skill-registry/tree/main/skills/other/other/sagemath`
- Candidate path status: `404-not-found`
- Repository license status: `verified-repo-license-mit`
- Install status: `wrapper-only-unresolved-source-path`

## Repo Workflow

1. Read `tools/registry.yaml` entries `sagemath-wsl`, `gap-sage`, and
   `singular-sage` before selecting a route.
2. Use `scripts/run_wsl_algebra.py sagemath-wsl --mode smoke --dry-run`, or an
   experiment-local Sage command with saved inputs and outputs.
3. Store `.sage` files, generated scripts, logs, hashes, and command metadata
   under `experiments/<EXP-ID>/`.
4. Exact Sage computations can be `exact-computation` evidence only when all
   inputs, commands, assumptions, and outputs are recorded.
5. Do not treat this wrapper or any Sage output as a theorem proof by itself.
