# AI for Math Research

A lightweight research workspace for AI-assisted mathematics.

This repository is not a theorem prover, not a proof-search engine, and not a
domain-specific math solver. It is a reproducible research operating system
for LLM-assisted mathematics: plans, claims, experiments, tool routing, exact
computations, verification, and reports.

The guiding principle is:

> Do not constrain how the AI thinks; constrain what evidence it must leave.

## Philosophy

Modern LLMs increasingly do not need rigid task-decomposition harnesses. They
need:

- clear mathematical state,
- explicit assumptions,
- access to well-described tools,
- reproducible experiments,
- visible claim status,
- honest reports.

This repository provides that structure.

## What This Is

- A template for AI-assisted math research projects.
- A claim ledger.
- An experiment ledger.
- A YAML metadata schema for machine-checkable ledger state.
- A tool registry.
- A plan, execute, report workflow.
- A reproducibility discipline.

## What This Is Not

- Not a replacement for mathematical judgment.
- Not a rigid multi-agent orchestration framework.
- Not a universal CAS wrapper.
- Not a proof correctness oracle.
- Not a fixed DAG for research.

## Default Workflow

Every nontrivial research action should leave an artifact.

1. Define the problem in `problem/`.
2. Record assumptions and possible failure modes.
3. Write or update a plan in `plans/`.
4. Create or update affected claims in `claims/`.
5. Run exact, symbolic, numerical, or formal tools as appropriate.
6. Save commands, inputs, outputs, environment notes, and interpretation under
   `experiments/`.
7. Update claim statuses.
8. Write a report in `reports/`.

## Directory Map

```text
ai-for-math-research/
  README.md
  AGENTS.md
  PLAN.md
  Makefile
  pyproject.toml

  problem/
    problem.md
    background.md
    notation.md
    glossary.md

  claims/
    CLAIM-0001-template.md

  plans/
    PLAN-0001-template.md

  experiments/
    EXP-0001-template/
      experiment.md
      run.py
      input/
      output/

  reports/
    REPORT-0001-template.md

  tools/
    tools.md
    local-tools.md
    tool-contracts.md
    registry.yaml
    adapters/

  skills/
    math-python-exact/
    math-sage/
    math-windows-cas/
    math-commalg/
    math-formal-provers/

  scripts/
    ledger.py
    check_claims.py
    check_experiments.py
    check_reports.py
    check_tools.py
    init_project.py
    make_index.py
    run_experiment.py
    run_math_tool.py

  templates/
    claim.md
    experiment.md
    literature-note.md
    plan.md
    report.md

  docs/
    schema.md
    philosophy.md
    workflow.md
    examples.md
    case-study-jordan-quillen.md

  CLAIM_GRAPH.md
  OPEN_GAPS.md
  FAILED_EXPERIMENTS.md
  NEXT_ACTIONS.md
```

Domain-specific projects can add directories such as `theory/`, `src/`,
`formal/`, or `paper/`. The framework keeps the default surface domain-neutral.

## Status Vocabulary

Claims:

- `idea`
- `conjecture`
- `plausible`
- `proof-draft`
- `checked`
- `refuted`
- `blocked`
- `abandoned`

Experiments:

- `planned`
- `runnable`
- `run`
- `failed`
- `obsolete`
- `blocked`

Reports:

- `draft`
- `complete`
- `superseded`
- `blocked`

## Ledger Metadata

Ledger artifacts use YAML frontmatter parsed with `PyYAML` and `safe_load`.
The Markdown body remains the human-readable research record; the YAML layer is
for IDs, status, dependencies, evidence, and reproducibility checks.

Example claim metadata:

```yaml
---
schema_version: 1
id: CLAIM-0001
status: conjecture
type: theorem
depends_on: []
evidence: []
assumptions: []
last_updated: "2026-06-01"
---
```

See `docs/schema.md` for the schema and evidence vocabulary.

## Tool Skills And Registry

External mathematical tools use a hybrid design:

- `tools/registry.yaml` stores local executable facts, routes, status, caveats,
  evidence modes, and reviewed third-party skill references.
- `skills/*/SKILL.md` stores project-specific agent workflows.
- `scripts/run_math_tool.py` and the group wrappers execute only the selected
  registry command and capture metadata.
- Ledger claims and experiments remain tool-neutral by pointing to output JSON,
  logs, hashes, and command metadata.

Third-party open-source skills are reviewed references only. They are not
installed automatically and do not become execution authority for this
workspace.

## Quick Start

Check the template:

```powershell
python scripts/check_claims.py
python scripts/check_experiments.py
python scripts/check_reports.py
python scripts/check_tools.py
python scripts/make_index.py
python -m unittest discover -s tests
```

Run a single experiment:

```powershell
python scripts/run_experiment.py EXP-0001-template
```

Run the complete toy case:

```powershell
python scripts/run_experiment.py EXP-0002-toy-homology
```

Dry-run a local tool route without executing it:

```powershell
python scripts/run_math_tool.py sagemath-wsl --mode smoke --dry-run
```

Initialize a downstream project skeleton:

```powershell
python scripts/init_project.py D:\my-math-project --title "My Math Project"
```

## Design Lineage

This repository abstracts the workflow shape of a concrete mathematical
research repo into a reusable template. It copies the process discipline, not
the mathematical content: claim ledgers, experiment ledgers, exact-computation
preference, tool registries, honest failure records, and reports.
