"""Validate experiment ledger metadata without running experiments."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = ROOT / "experiments"

REQUIRED_MARKERS = (
    "Status:",
    "Question:",
    "Hypothesis:",
    "Plan:",
    "Tools:",
    "Inputs:",
    "Run command:",
    "Expected output:",
    "Actual output:",
    "Interpretation:",
    "Claims affected:",
    "Limitations:",
    "Reproducibility notes:",
)

VALID_STATUSES = {"planned", "runnable", "run", "failed", "obsolete", "blocked"}


def _status_from_text(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("Status:"):
            return line.removeprefix("Status:").strip()
    return None


def _has_no_machine_output_note(text: str) -> bool:
    return "No machine output:" in text


def validate_experiment(path: Path) -> list[str]:
    failures: list[str] = []
    experiment_md = path / "experiment.md"

    if not experiment_md.exists():
        return ["missing experiment.md"]

    text = experiment_md.read_text(encoding="utf-8")
    failures.extend(
        f"experiment.md missing {marker}"
        for marker in REQUIRED_MARKERS
        if marker not in text
    )

    status = _status_from_text(text)
    if status not in VALID_STATUSES:
        failures.append(
            f"invalid status {status!r}; expected one of {sorted(VALID_STATUSES)}"
        )

    if status == "run":
        results_json = path / "output" / "results.json"
        if results_json.exists():
            try:
                json.loads(results_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                failures.append(f"output/results.json is invalid JSON: {exc}")
        elif not _has_no_machine_output_note(text):
            failures.append(
                "status is run but output/results.json is missing and "
                "No machine output note is absent"
            )

    return failures


def main() -> int:
    failures: list[str] = []
    experiment_dirs = sorted(
        path for path in EXPERIMENTS_DIR.glob("EXP-*") if path.is_dir()
    )

    if not experiment_dirs:
        failures.append("no experiment directories found")

    for path in experiment_dirs:
        for failure in validate_experiment(path):
            failures.append(f"{path.relative_to(ROOT)} {failure}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("experiment metadata ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
