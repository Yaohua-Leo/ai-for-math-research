# Artifact Workflow

Use this reference when a task changes research state.

## Main Loop

1. Read the current problem statement, top-level plan, index, tool registry, and
   affected artifacts.
2. State the mathematical goal, assumptions, and likely failure modes.
3. Write or update a plan in `plans/`.
4. Create or update affected claims in `claims/`.
5. Create or update an experiment directory under `experiments/` if computation
   is needed.
6. Run only the selected computation or tool route, and record reproducibility
   metadata.
7. Update affected claims conservatively.
8. Write or update a report in `reports/`.
9. Refresh generated indexes and run validation.

## Artifact Rule

Every nontrivial research action must leave an artifact:

- Planning belongs in `plans/`.
- Mathematical assertions belong in `claims/`.
- Computations belong in `experiments/`.
- Synthesis belongs in `reports/`.
- Tool knowledge belongs in `tools/`.

Keep YAML frontmatter small and factual. Put mathematical discussion in the
Markdown body.

## Tool Use

Check `tools/tools.md`, `tools/local-tools.md`, and `tools/registry.yaml`
before relying on a local or external mathematical tool. Use dry-run routes
before executing licensed, expensive, WSL, CAS, or formal-tool checks unless
the user explicitly requested the run.

