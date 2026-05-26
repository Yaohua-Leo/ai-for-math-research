# Project Plan

This repository is a lightweight research operating system for AI-assisted
mathematics. It should stay low-control and high-accountability.

## Phase 1: Template, Not Engine

Goal: provide the durable structure that makes an AI math research project
auditable.

Deliverables:

- `README.md` with philosophy and workflow.
- `AGENTS.md` with strict agent rules.
- `problem/` documentation stubs.
- `claims/` claim ledger template.
- `plans/` plan template.
- `experiments/` experiment ledger template.
- `reports/` report template.
- `tools/` tool registry and tool contracts.
- Standard-library Python validation scripts.
- `INDEX.md` generated from current artifacts.

## Phase 2: Toy Case Study

Goal: demonstrate the artifact chain without making the framework
domain-specific.

Candidate:

```text
finite-dimensional chain complex homology toy example
```

Artifact chain:

```text
CLAIM-0001
PLAN-0001
EXP-0001
output/results.json
REPORT-0001
```

The point is reproducibility, not mathematical novelty.

## Phase 3: Downstream Validation

Goal: validate the template against a real downstream mathematical project
without copying its domain content.

Deliverable:

```text
docs/case-study-jordan-quillen.md
```

The case study should explain how the downstream project uses claim ledgers,
experiment ledgers, exact arithmetic preference, local tool registries, honest
experiment status, and report placeholders.

## Constraints

- Keep the default framework domain-neutral.
- Do not add a heavy orchestration harness.
- Do not add new runtime dependencies unless a concrete need appears.
- Do not make all experiments run by default.
- Treat failed experiments as useful research artifacts.
