---
name: agda-claude-skills
description: Use as a repo-scoped wrapper for Agda workflow references when working with Agda through the math tool registry; do not vendor upstream Agda Claude skills until license status is confirmed.
---

# Agda Claude Skills Wrapper

This is a wrapper-only repo skill. The upstream Agda Claude skill directories
were reviewed as useful workflow references, but the upstream license was not
detected, so their contents are not vendored here.

## Source Reference

- Repository: `https://github.com/input-output-hk/agda-claude-skills`
- Reviewed paths: `agda-find-reproducer/SKILL.md`,
  `agda-typecheck-profile/SKILL.md`
- Reviewed SHAs: `1e2a942990adc293023b04d062baa2f553924a82`,
  `d9893a1c3e879406e1c7370c7cf4e56132f08f0d`
- License status: `missing-license-file`

## Repo Workflow

1. Read `tools/registry.yaml` entry `agda-wsl` before selecting Agda.
2. Use `scripts/run_formal_tool.py agda-wsl --mode version --dry-run` for route
   inspection, or an experiment-local command for real proof checks.
3. Store Agda files, library config notes, build logs, hashes, and command
   metadata under `experiments/<EXP-ID>/`.
4. Treat Agda success as `formal-check` evidence only for the checked files.
5. Do not promote any Agda result to `checked` claim status unless the claim
   evidence points to the reproducible proof artifact and assumptions.
