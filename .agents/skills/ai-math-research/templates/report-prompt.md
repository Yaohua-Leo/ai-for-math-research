# Report Prompt Template

When creating or updating a report, copy or adapt the root
`templates/report.md` file and keep:

- YAML frontmatter with `schema_version`, `id`, `status`, `claims`,
  `experiments`, and `last_updated`.
- Separate sections for:
  - Proved
  - Supported By Computation
  - Conjectural
  - Failed Or Refuted
  - Blocked
  - Next Steps
  - Artifacts

Do not blur proof status. If evidence is only computational or bounded, place it
under `Supported By Computation`, not `Proved`.

