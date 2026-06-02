# Tools

This directory is the capability registry for AI-assisted mathematical work.

The registry should tell an agent:

1. which tools are available,
2. what each tool is good for,
3. what caveats apply,
4. how output must be recorded.

Do not hardcode a research strategy here. The point is to support autonomous
tool choice while requiring reproducible evidence.

Machine-readable tool and adapter metadata lives in:

- `tools/registry.yaml`
- `tools/adapters/python-exact-runner.yaml`
- `tools/adapters/registry-tool-runner.yaml`
- `tools/adapters/wsl-algebra-runner.yaml`
- `tools/adapters/windows-cas-runner.yaml`
- `tools/adapters/formal-tool-runner.yaml`

Repo-scoped skill instructions live in `.agents/skills/`. They are workflow
guidance for agents; they do not replace experiments, outputs, registry routes,
or claim evidence. Skill provenance is recorded in
`.agents/skills/SOURCES.yaml`.

Use dry-run before executing external tools:

```powershell
python scripts/run_math_tool.py sagemath-wsl --mode smoke --dry-run
```

Default validation checks registry shape but does not run expensive or licensed
tools.
