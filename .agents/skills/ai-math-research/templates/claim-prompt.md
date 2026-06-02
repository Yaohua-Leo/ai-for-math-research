# Claim Prompt Template

When creating or updating a claim, copy or adapt the root `templates/claim.md`
file and keep:

- YAML frontmatter with `schema_version`, `id`, `status`, `type`,
  `depends_on`, `evidence`, `assumptions`, and `last_updated`.
- A precise statement.
- Explicit assumptions.
- Proof sketch or a clear statement that no proof has been supplied.
- Known gaps.
- References, or `None yet`.
- Computational evidence paths, or `None yet`.
- Formalization status.
- Verification notes.

Default new claims to `idea` or `conjecture`; do not use `checked` without
proof or checked verification.

