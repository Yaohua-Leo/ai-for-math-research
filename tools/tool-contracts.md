# Tool Contracts

Tool contracts describe when a class of tool is appropriate. They do not force
a fixed pipeline.

## Exact Linear Algebra

Preferred:

1. Python `fractions` or exact integer arithmetic.
2. SymPy.
3. Sage, Maple, or Wolfram Language.

Do not use floating point unless the experiment is explicitly numerical.

## Commutative Algebra

Preferred:

1. Sage.
2. Singular.
3. Macaulay2.
4. OSCAR.

Record input scripts and output files under the experiment directory.

## Finite Groups And Representations

Preferred:

1. GAP.
2. Sage GAP interface.

Record group definitions, library identifiers, and package assumptions.

## Numerical Experiments

Numerical experiments must state:

- precision,
- random seeds,
- stopping criteria,
- whether results are heuristic.

Numerical evidence does not prove a theorem by itself.

## Formal Proof

Preferred:

1. Lean for mathlib-adjacent reusable facts.
2. Rocq or Coq for constructive or type-theoretic developments.
3. Isabelle for structured classical proofs.
4. Agda for dependent type experiments.

Formal output should identify the theorem name, source file, command, and tool
version.
