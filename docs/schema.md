# Ledger Schema

Ledger artifacts are Markdown files with required YAML frontmatter. The
frontmatter is parsed with `yaml.safe_load`; arbitrary Python object tags are
not supported.

## Common Fields

- `schema_version`: currently `1`.
- `id`: stable artifact ID matching the file or directory stem.
- `status`: one of the vocabulary values for that artifact type.
- `last_updated`: quoted ISO date string, for example `"2026-06-01"`.

## Claims

Required claim metadata:

```yaml
schema_version: 1
id: CLAIM-0001
status: conjecture
type: theorem
depends_on: []
evidence: []
assumptions: []
last_updated: "2026-06-01"
```

Allowed evidence types:

- `human-proof`
- `formal-check`
- `exact-computation`
- `finite-experiment`
- `numerical-evidence`
- `literature-reference`
- `counterexample`

A `checked` claim must have strong evidence: `human-proof`, `formal-check`, or
`exact-computation` with `fully_verifiable: true`.

## Experiments

Required experiment metadata:

```yaml
schema_version: 1
id: EXP-0001
status: runnable
tool: python
command:
  - python
  - scripts/run_experiment.py
  - EXP-0001
inputs: []
outputs:
  - output/results.json
claims_affected: []
random_seed: null
timeout_seconds: 30
```

For `status: run`, every listed output path must exist and
`output/results.json` must be valid JSON unless the body explicitly says
`No machine output:`.

## Plans And Reports

Plans and reports use the same small metadata shape:

```yaml
schema_version: 1
id: PLAN-0001
status: draft
claims: []
experiments: []
last_updated: "2026-06-01"
```

Reports use report status values: `draft`, `complete`, `superseded`, or
`blocked`.

## Tool Registry

The tool registry lives at `tools/registry.yaml`. It is not a ledger artifact,
but it is validated by `scripts/check_tools.py`.

Required fields for each `verified` tool:

- `id`
- `status`
- `command`
- `route`
- `evidence_mode`
- `reproducibility_caveat`

Allowed evidence modes:

- `exact-computation`
- `finite-experiment`
- `numerical-evidence`
- `formal-check`
- `not-evidence`
- `reference-only`

The registry can also list project skills, runner adapters, tool groups, and
reviewed open-source skills.

## Repo-Scoped Skill Sources

Repo-scoped Codex skills live under `.agents/skills/`. Their provenance manifest
lives at `.agents/skills/SOURCES.yaml` and is validated by
`scripts/check_tools.py`.

Required manifest fields for each skill:

- `id`
- `installed_path`
- `install_mode`
- `source_url`
- `source_path`
- `source_sha`
- `license`
- `license_status`

Allowed install modes:

- `local-project`
- `repo-scoped-vendored`
- `repo-scoped-wrapper`

Vendored third-party skills require a verified license status. Wrapper-only
skills may record unclear license or unresolved source-path status, but their
upstream contents are not vendored and they must route execution through
`tools/registry.yaml`, `scripts/run_*`, and experiment ledger artifacts.
