---
name: matlab-skills
description: Use as a repo-scoped wrapper for MATLAB and Octave workflow references while routing execution through tools/registry.yaml and the Windows CAS runner.
---

# MATLAB Skills Wrapper

This is a wrapper-only repo skill. The upstream MATLAB agent skills playground
was reviewed for symbolic and numerical workflow patterns, but this repository
does not vendor it because the GitHub license endpoint reports `NOASSERTION`
and MATLAB remains a licensed local tool.

## Source Reference

- Repository: `https://github.com/matlab/agent-skills-playground`
- Reviewed path: `skills/matlab-symbolic-math/SKILL.md`
- Reviewed SHA: `2cb65f175a9839470cf3ad53221a82db87e298bc`
- License status: `repo-license-noassertion`

## Repo Workflow

1. Read `tools/registry.yaml` entries `matlab` and `octave` before selecting a
   route.
2. Use `scripts/run_windows_cas.py matlab --mode smoke --dry-run`,
   `scripts/run_windows_cas.py octave --mode smoke --dry-run`, or an
   experiment-local batch command.
3. Store `.m` files, inputs, outputs, stdout/stderr, hashes, and command
   metadata under `experiments/<EXP-ID>/`.
4. Treat most MATLAB or Octave floating-point output as `numerical-evidence`;
   exact symbolic output needs saved assumptions and reproducible commands.
5. Never store license files, credentials, activation data, or private account
   details in this repository.
