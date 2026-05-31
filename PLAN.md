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

Implemented candidate:

```text
finite-dimensional chain complex homology toy example
```

Artifact chain:

```text
CLAIM-0002-toy-homology
PLAN-0002-toy-homology
EXP-0002-toy-homology
output/results.json
REPORT-0002-toy-homology
```

The point is reproducibility, not mathematical novelty.

## Phase 2.5: Machine-Readable Ledger

Goal: make ledger state useful to tools without sacrificing readable Markdown.

Deliverables:

- YAML frontmatter parsed with `PyYAML` and `yaml.safe_load`.
- Claim dependency and evidence validation.
- Reproducibility metadata from `scripts/run_experiment.py`.
- Generated research dashboards: `INDEX.md`, `CLAIM_GRAPH.md`,
  `OPEN_GAPS.md`, `FAILED_EXPERIMENTS.md`, and `NEXT_ACTIONS.md`.
- Initial Python exact-runner adapter metadata under `tools/`.

## Phase 2.6: External Math Tool Skills And Registry

Goal: make local external tool use explicit without turning this repository into
a universal CAS wrapper.

Deliverables:

- Project skills for Python exact computation, Sage, Windows CAS/numerical
  tools, commutative algebra tools, and formal proof assistants.
- `tools/registry.yaml` entries for local routes copied from the Jordan
  workspace tool snapshot.
- Group-limited runner scripts for registry-defined WSL algebra, Windows CAS,
  and formal-tool checks.
- Registry validation through `scripts/check_tools.py`.
- Tests that cover registry validation, dry-run routing, exact Python smoke
  metadata, and an opt-in WSL external smoke check.

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
- Do not run licensed or expensive external tools by default.
- Treat failed experiments as useful research artifacts.
