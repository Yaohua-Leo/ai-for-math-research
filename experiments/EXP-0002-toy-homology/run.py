"""Compute homology dimensions for a one-arrow chain complex over Q."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def rank(matrix: list[list[int]]) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return 0

    pivot_row = 0
    column_count = len(rows[0])
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column] != 0),
            None,
        )
        if pivot is None:
            continue

        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]

        for row_index, row in enumerate(rows):
            if row_index == pivot_row:
                continue
            factor = row[column]
            if factor == 0:
                continue
            rows[row_index] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(row, rows[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def main() -> int:
    experiment_dir = Path(__file__).resolve().parent
    output_dir = experiment_dir / "output"
    output_dir.mkdir(exist_ok=True)

    d1 = [[1]]
    rank_d1 = rank(d1)
    chain_dimensions = {"C1": 1, "C0": 1}
    homology_dimensions = {
        "H1": chain_dimensions["C1"] - rank_d1,
        "H0": chain_dimensions["C0"] - rank_d1,
    }
    result = {
        "experiment": "EXP-0002-toy-homology",
        "status": "success",
        "field": "Q",
        "differentials": {"d1": d1},
        "ranks": {"d1": rank_d1},
        "homology_dimensions": homology_dimensions,
        "exact_arithmetic": True,
        "mathematical_claims_supported": ["CLAIM-0002-toy-homology"],
    }
    (output_dir / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("toy homology experiment completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
