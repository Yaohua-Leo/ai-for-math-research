"""Validate experiment ledger metadata without running experiments."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.check_claims import collect_claim_ids
    from scripts.ledger import LedgerError, read_artifact, require_fields
except ModuleNotFoundError:  # pragma: no cover - CLI execution fallback
    from check_claims import collect_claim_ids
    from ledger import LedgerError, read_artifact, require_fields

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = ROOT / "experiments"

REQUIRED_METADATA = (
    "schema_version",
    "id",
    "status",
    "tool",
    "command",
    "inputs",
    "outputs",
    "claims_affected",
    "random_seed",
    "timeout_seconds",
)

REQUIRED_BODY_MARKERS = (
    "## Question",
    "## Hypothesis",
    "## Plan",
    "## Tools",
    "## Inputs",
    "## Expected Output",
    "## Actual Output",
    "## Interpretation",
    "## Claims Affected",
    "## Limitations",
    "## Reproducibility Notes",
)

VALID_STATUSES = {"planned", "runnable", "run", "failed", "obsolete", "blocked"}
EXPERIMENT_ID_RE = re.compile(r"^EXP-\d{4}(?:-[a-z0-9][a-z0-9-]*)?$")


def _require_string_list(metadata: dict[str, Any], field: str) -> list[str]:
    value = metadata.get(field)
    if not isinstance(value, list):
        return [f"metadata field {field} must be a list"]
    if not all(isinstance(item, str) for item in value):
        return [f"metadata field {field} must contain only strings"]
    return []


def _experiment_path_exists(experiment: Path, path_value: str) -> bool:
    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate.exists()
    return (experiment / candidate).exists()


def validate_experiment(
    path: Path,
    *,
    root: Path = ROOT,
    known_claim_ids: set[str] | None = None,
) -> list[str]:
    failures: list[str] = []
    experiment_md = path / "experiment.md"

    if not experiment_md.exists():
        return ["missing experiment.md"]

    try:
        artifact = read_artifact(experiment_md)
    except LedgerError as exc:
        return [str(exc)]

    metadata = artifact.metadata
    failures.extend(require_fields(metadata, REQUIRED_METADATA))

    experiment_id = metadata.get("id")
    if not isinstance(experiment_id, str) or not EXPERIMENT_ID_RE.fullmatch(
        experiment_id
    ):
        failures.append(f"invalid experiment id {experiment_id!r}")
    elif path.name != experiment_id:
        failures.append(
            f"metadata id {experiment_id} does not match directory name {path.name}"
        )

    if metadata.get("schema_version") != 1:
        failures.append("schema_version must be 1")

    status = metadata.get("status")
    if status not in VALID_STATUSES:
        failures.append(
            f"invalid status {status!r}; expected one of {sorted(VALID_STATUSES)}"
        )

    if not isinstance(metadata.get("tool"), str):
        failures.append("metadata field tool must be a string")

    failures.extend(_require_string_list(metadata, "command"))
    failures.extend(_require_string_list(metadata, "inputs"))
    failures.extend(_require_string_list(metadata, "outputs"))
    failures.extend(_require_string_list(metadata, "claims_affected"))

    random_seed = metadata.get("random_seed")
    if random_seed is not None and not isinstance(random_seed, int):
        failures.append("metadata field random_seed must be an integer or null")

    timeout_seconds = metadata.get("timeout_seconds")
    if timeout_seconds is not None and (
        not isinstance(timeout_seconds, int) or timeout_seconds <= 0
    ):
        failures.append("metadata field timeout_seconds must be a positive integer")

    inputs = metadata.get("inputs")
    if isinstance(inputs, list):
        for input_path in inputs:
            if isinstance(input_path, str) and not _experiment_path_exists(
                path, input_path
            ):
                failures.append(f"input path {input_path} does not exist")

    outputs = metadata.get("outputs")
    if status == "run" and isinstance(outputs, list):
        for output_path in outputs:
            if isinstance(output_path, str) and not _experiment_path_exists(
                path, output_path
            ):
                failures.append(f"output path {output_path} does not exist")

    claims_affected = metadata.get("claims_affected")
    if isinstance(claims_affected, list) and known_claim_ids is not None:
        for claim_id in claims_affected:
            if isinstance(claim_id, str) and claim_id not in known_claim_ids:
                failures.append(f"unknown affected claim {claim_id}")

    if status == "run":
        results_json = path / "output" / "results.json"
        if results_json.exists():
            try:
                json.loads(results_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                failures.append(f"output/results.json is invalid JSON: {exc}")
        elif "No machine output:" not in artifact.body:
            failures.append(
                "status is run but output/results.json is missing and "
                "No machine output note is absent"
            )

    failures.extend(
        f"missing body section {marker}"
        for marker in REQUIRED_BODY_MARKERS
        if marker not in artifact.body
    )
    return failures


def main() -> int:
    failures: list[str] = []
    experiment_dirs = sorted(
        path for path in EXPERIMENTS_DIR.glob("EXP-*") if path.is_dir()
    )
    known_claim_ids = collect_claim_ids(ROOT)

    if not experiment_dirs:
        failures.append("no experiment directories found")

    for path in experiment_dirs:
        for failure in validate_experiment(
            path,
            root=ROOT,
            known_claim_ids=known_claim_ids,
        ):
            failures.append(f"{path.relative_to(ROOT)} {failure}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("experiment metadata ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
