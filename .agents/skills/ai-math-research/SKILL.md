---
name: ai-math-research
description: "Use for AI-assisted mathematics research in this repository: planning, claim ledger work, experiment design or recording, report writing, tool registry use, and verification of the claim/experiment/report evidence chain."
---

# AI Math Research

Use this skill when working in this repository on nontrivial mathematical
research tasks, research workflow tasks, claim management, experiment planning
or execution, report synthesis, or local math tool selection.

This skill is for Codex IDE/CLI/App workflows. It does not provide an OpenAI API
backend, Agents SDK runtime, Codex MCP runtime, HTTP service, or chat shell.

## Required Context

Before changing research state, read the smallest relevant set of:

- `problem/problem.md`, plus `problem/background.md`, `problem/notation.md`, or
  `problem/glossary.md` when the task depends on them.
- `PLAN.md` and `INDEX.md`.
- Affected files under `claims/`, `plans/`, `experiments/`, and `reports/`.
- `tools/tools.md` and `tools/registry.yaml` before selecting nontrivial tools.
- Reference files in this skill only when needed:
  - `references/workflow.md` for artifact flow.
  - `references/status-vocabulary.md` for status choices.
  - `references/safety-rules.md` for proof and evidence boundaries.

## Hard Boundaries

- Do not fabricate mathematical results or references.
- Do not silently change assumptions.
- Do not turn computational evidence into a theorem.
- Do not mark a claim as `checked` unless a proof or verification is present
  and checked against the stated assumptions.
- Do not delete failed experiments. Mark them `failed`, `obsolete`, or
  `blocked` and preserve the evidence.
- Do not store API keys, credentials, license data, private account data, or
  Codex auth files in this repository.

## Artifact Placement

Put every substantive research action in the ledger:

- Research plans go in `plans/`.
- Mathematical assertions go in `claims/`.
- Computations and reproducibility records go in `experiments/`.
- Synthesis and status reports go in `reports/`.
- Tool facts and caveats go in `tools/`.

Use the templates in `templates/` when creating new artifacts. Prefer copying
the matching root template from `templates/` first; use this skill's
`templates/` as prompt guidance for what to preserve.

## Default Workflow

1. Restate the mathematical goal and fixed assumptions.
2. Identify affected claims, plans, experiments, reports, and tools.
3. List failure modes, especially assumption drift and evidence overstatement.
4. Update or create a plan before running new experiments.
5. Prefer exact, symbolic, rational, or formal tooling before numerical checks.
6. Record commands, inputs, outputs, environment, hashes, and interpretation.
7. Update affected claim evidence/status conservatively.
8. Write or update a report that separates proved, experimentally supported,
   conjectural, refuted, and blocked material.
9. Run the repository verification checks before claiming the workspace is
   healthy.

## Verification

For routine changes, run the affected checks. Before claiming the workspace is
healthy, run:

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
