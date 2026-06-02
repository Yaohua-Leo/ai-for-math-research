# Codex Workflow

This repository includes a repo-scoped Codex skill at:

```text
.agents/skills/ai-math-research/SKILL.md
```

Codex can use this skill from the IDE extension, Codex CLI, or Codex app when
working in this repository. It is a workflow guide for Codex, not an independent
LLM runtime.

Tool-calling skills and reviewed third-party skills also live under
`.agents/skills/`. Their provenance is recorded in
`.agents/skills/SOURCES.yaml`; executable routes remain in
`tools/registry.yaml`.

## What The Skill Does

The skill teaches Codex to work with this repository as a mathematical research
ledger:

- Read `problem/`, `PLAN.md`, `INDEX.md`, affected artifacts, and the tool
  registry before changing research state.
- Put plans in `plans/`, mathematical assertions in `claims/`, computations in
  `experiments/`, reports in `reports/`, and tool facts in `tools/`.
- Preserve failed experiments and blocked work as useful evidence.
- Keep proof, computation, conjecture, refutation, and blocked status separate.

## What The Skill Does Not Do

The skill does not add:

- an OpenAI API backend,
- an Agents SDK runtime,
- a Codex MCP backend,
- `ai-math-agent chat`,
- an HTTP service,
- a web UI.

Model selection, authentication, permissions, sandboxing, and billing remain
handled by the Codex product surface you are using.

## How To Use It

Open the repository in VS Code, Cursor, Windsurf, Codex CLI, or the Codex app.
Ask Codex research-workflow questions directly, for example:

```text
根据当前 problem 和 claims，写一个下一步研究计划。
```

```text
为这个 conjecture 设计一个可复现实验，但不要运行。
```

```text
检查所有 reports 有没有把计算证据说成 theorem。
```

```text
运行默认验证脚本并解释失败项。
```

To force the skill, mention it explicitly:

```text
$ai-math-research
```

Restart Codex after installing or changing repo-scoped skills so the updated
skill metadata is discovered.

## Verification

After Codex changes research artifacts, run the standard checks:

```powershell
python scripts/check_claims.py
python scripts/check_experiments.py
python scripts/check_reports.py
python scripts/check_tools.py
python scripts/make_index.py
python -m unittest discover -s tests
```

If `ruff` is available, also run:

```powershell
python -m ruff check .
```
