"""Validate research report metadata."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    from scripts.ledger import LedgerError, read_artifact, require_fields
except ModuleNotFoundError:  # pragma: no cover - CLI execution fallback
    from ledger import LedgerError, read_artifact, require_fields

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"

REQUIRED_METADATA = (
    "schema_version",
    "id",
    "status",
    "claims",
    "experiments",
    "last_updated",
)

REQUIRED_BODY_MARKERS = (
    "## Goal",
    "## Proved",
    "## Supported By Computation",
    "## Conjectural",
    "## Failed Or Refuted",
    "## Blocked",
    "## Next Steps",
    "## Artifacts",
)

VALID_STATUSES = {"draft", "complete", "superseded", "blocked"}
REPORT_ID_RE = re.compile(r"^REPORT-\d{4}(?:-[a-z0-9][a-z0-9-]*)?$")


def _require_string_list(metadata: dict[str, Any], field: str) -> list[str]:
    value = metadata.get(field)
    if not isinstance(value, list):
        return [f"metadata field {field} must be a list"]
    if not all(isinstance(item, str) for item in value):
        return [f"metadata field {field} must contain only strings"]
    return []


def validate_report(path: Path) -> list[str]:
    try:
        artifact = read_artifact(path)
    except LedgerError as exc:
        return [str(exc)]

    metadata = artifact.metadata
    failures = require_fields(metadata, REQUIRED_METADATA)

    report_id = metadata.get("id")
    if not isinstance(report_id, str) or not REPORT_ID_RE.fullmatch(report_id):
        failures.append(f"invalid report id {report_id!r}")
    elif path.stem != report_id:
        failures.append(f"metadata id {report_id} does not match file stem {path.stem}")

    if metadata.get("schema_version") != 1:
        failures.append("schema_version must be 1")

    status = metadata.get("status")
    if status not in VALID_STATUSES:
        failures.append(
            f"invalid status {status!r}; expected one of {sorted(VALID_STATUSES)}"
        )

    failures.extend(_require_string_list(metadata, "claims"))
    failures.extend(_require_string_list(metadata, "experiments"))

    failures.extend(
        f"missing body section {marker}"
        for marker in REQUIRED_BODY_MARKERS
        if marker not in artifact.body
    )
    return failures


def main() -> int:
    failures: list[str] = []
    report_files = sorted(REPORTS_DIR.glob("REPORT-*.md"))

    if not report_files:
        failures.append("no report files found")

    for path in report_files:
        for failure in validate_report(path):
            failures.append(f"{path.relative_to(ROOT)} {failure}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("report metadata ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
