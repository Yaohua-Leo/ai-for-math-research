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

  scripts/
    check_claims.py
    check_experiments.py
    check_reports.py
    init_project.py
    make_index.py
    run_experiment.py

  templates/
    claim.md
    experiment.md
    literature-note.md
    plan.md
    report.md

  docs/
    philosophy.md
    workflow.md
    examples.md
    case-study-jordan-quillen.md
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

## Quick Start

Check the template:

```powershell
python scripts/check_claims.py
python scripts/check_experiments.py
python scripts/check_reports.py
python scripts/make_index.py
python -m unittest discover -s tests
```

Run a single experiment:

```powershell
python scripts/run_experiment.py EXP-0001-template
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
