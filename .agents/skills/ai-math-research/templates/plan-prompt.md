# Plan Prompt Template

When creating a plan, copy or adapt the root `templates/plan.md` file and keep:

- YAML frontmatter with `schema_version`, `id`, `status`, `claims`,
  `experiments`, and `last_updated`.
- A precise goal.
- Fixed assumptions.
- Affected claims and experiments.
- Tool plan with exact or symbolic tools preferred.
- Failure modes.
- Exit criteria that mention reports, claims, and experiment evidence.

Use `status: draft` unless the plan is already complete for its stated scope.

