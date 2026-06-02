# Experiment Prompt Template

When creating or updating an experiment, copy or adapt the root
`templates/experiment.md` file and keep:

- YAML frontmatter with `schema_version`, `id`, `status`, `tool`, `command`,
  `inputs`, `outputs`, `claims_affected`, `random_seed`, and
  `timeout_seconds`.
- A clear question and hypothesis.
- A reproducible plan.
- Tool names and versions when known.
- Expected and actual output sections.
- Interpretation that states what the output does and does not support.
- Limitations and reproducibility notes.

Use `status: planned` until command and inputs are ready. Use `status: run` only
after outputs exist and are recorded.

