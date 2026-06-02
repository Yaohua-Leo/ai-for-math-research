---
name: do-lang-r
description: Use as a repo-scoped wrapper for R workflow references while routing Rscript execution through tools/registry.yaml and experiment metadata.
---

# Do Lang R Wrapper

This is a wrapper-only repo skill. The upstream R skill path exists, but no
license file was confirmed for the checked repository/path, so its contents are
not vendored here.

## Source Reference

- Repository: `https://github.com/yejune/do-focus`
- Reviewed path: `.claude/skills/do-lang-r/SKILL.md`
- Reviewed SHA: `c0632dfb9bf85c9ecc545abbe27e71b3781cdfcd`
- License status: `missing-license-file`

## Repo Workflow

1. Read `tools/registry.yaml` entry `rscript` before selecting R.
2. Use `scripts/run_windows_cas.py rscript --mode smoke --dry-run`, or an
   experiment-local `Rscript` command with saved inputs and outputs.
3. Store R scripts, data inputs, output files, logs, hashes, and command
   metadata under `experiments/<EXP-ID>/`.
4. Treat statistical or floating-point R output as `numerical-evidence` unless
   the result is exact and fully reproducible.
5. Do not promote R output to theorem status without independent proof or
   fully verifiable exact-computation evidence.
