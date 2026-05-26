# Case Study: Jordan Quillen As Downstream Project

This framework was motivated by a concrete mathematical research repository
for Jordan algebra Quillen homology and cohomology. The new framework should
not copy that repository's mathematical content.

The reusable parts are workflow ideas:

- claim ledger discipline,
- experiment ledger discipline,
- exact arithmetic preference,
- local tool registry,
- honest experiment status,
- reports and writeup placeholders,
- clear distinction between proof, conjecture, computation, and failure.

Domain-specific content that should remain downstream:

- Jordan algebras,
- Quillen homology,
- Glassman cohomology,
- TKK comparison,
- special examples,
- domain-specific source code,
- paper-specific mathematical exposition.

The intended relationship is:

```text
ai-for-math-research
  -> provides generic workflow

downstream mathematical projects
  -> adapt the workflow for specific research programs
```
