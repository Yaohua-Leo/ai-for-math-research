"""Validate claim files for required research metadata."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

try:
    from scripts.ledger import (
        LedgerError,
        read_artifact,
        require_fields,
        require_string_list,
    )
except ModuleNotFoundError:  # pragma: no cover - CLI execution fallback
    from ledger import LedgerError, read_artifact, require_fields, require_string_list

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims"

REQUIRED_METADATA = (
    "schema_version",
    "id",
    "status",
    "type",
    "depends_on",
    "evidence",
    "assumptions",
    "last_updated",
)

REQUIRED_BODY_MARKERS = (
    "## Statement",
    "## Assumptions",
    "## Proof Sketch",
    "## Known Gaps",
    "## References",
    "## Computational Evidence",
    "## Formalization Status",
    "## Verification Notes",
)

VALID_STATUSES = {
    "idea",
    "conjecture",
    "plausible",
    "proof-draft",
    "checked",
    "refuted",
    "blocked",
    "abandoned",
}

VALID_EVIDENCE_TYPES = {
    "human-proof",
    "formal-check",
    "exact-computation",
    "finite-experiment",
    "numerical-evidence",
    "literature-reference",
    "counterexample",
}

STRONG_EVIDENCE_TYPES = {"human-proof", "formal-check"}

CLAIM_ID_RE = re.compile(r"^CLAIM-\d{4}(?:-[a-z0-9][a-z0-9-]*)?$")


def collect_claim_ids(root: Path = ROOT) -> set[str]:
    claim_ids: set[str] = set()
    for path in sorted((root / "claims").glob("CLAIM-*.md")):
        try:
            metadata = read_artifact(path).metadata
        except (LedgerError, OSError):
            continue
        claim_id = metadata.get("id")
        if isinstance(claim_id, str):
            claim_ids.add(claim_id)
    return claim_ids


def _is_date_like(value: Any) -> bool:
    return isinstance(value, str | date)


def _validate_evidence(
    metadata: dict[str, Any],
    root: Path,
) -> tuple[list[str], bool]:
    failures: list[str] = []
    evidence = metadata.get("evidence")
    if not isinstance(evidence, list):
        return ["metadata field evidence must be a list"], False

    has_strong_evidence = False
    for index, entry in enumerate(evidence, start=1):
        if not isinstance(entry, dict):
            failures.append(f"evidence item {index} must be a mapping")
            continue

        evidence_type = entry.get("type")
        if evidence_type not in VALID_EVIDENCE_TYPES:
            failures.append(
                f"evidence item {index} has invalid type {evidence_type!r}; "
                f"expected one of {sorted(VALID_EVIDENCE_TYPES)}"
            )
        elif evidence_type in STRONG_EVIDENCE_TYPES or (
            evidence_type == "exact-computation"
            and entry.get("fully_verifiable") is True
        ):
            has_strong_evidence = True

        evidence_path = entry.get("path")
        if evidence_path is None:
            continue
        if not isinstance(evidence_path, str):
            failures.append(f"evidence item {index} path must be a string")
            continue
        if not (root / evidence_path).exists():
            failures.append(f"evidence path {evidence_path} does not exist")

    return failures, has_strong_evidence


def validate_claim(
    path: Path,
    *,
    root: Path = ROOT,
    known_claim_ids: set[str] | None = None,
) -> list[str]:
    try:
        artifact = read_artifact(path)
    except LedgerError as exc:
        return [str(exc)]

    metadata = artifact.metadata
    failures = require_fields(metadata, REQUIRED_METADATA)

    claim_id = metadata.get("id")
    if not isinstance(claim_id, str) or not CLAIM_ID_RE.fullmatch(claim_id):
        failures.append(f"invalid claim id {claim_id!r}")
    elif path.stem != claim_id:
        failures.append(f"metadata id {claim_id} does not match file stem {path.stem}")

    if metadata.get("schema_version") != 1:
        failures.append("schema_version must be 1")

    status = metadata.get("status")
    if status not in VALID_STATUSES:
        failures.append(
            f"invalid status {status!r}; expected one of {sorted(VALID_STATUSES)}"
        )

    if not isinstance(metadata.get("type"), str):
        failures.append("metadata field type must be a string")

    failures.extend(require_string_list(metadata, "depends_on"))
    failures.extend(require_string_list(metadata, "assumptions"))

    if not _is_date_like(metadata.get("last_updated")):
        failures.append("metadata field last_updated must be a string or date")

    dependencies = metadata.get("depends_on")
    if isinstance(dependencies, list) and known_claim_ids is not None:
        for dependency in dependencies:
            if not isinstance(dependency, str):
                continue
            if dependency == claim_id:
                failures.append("claim cannot depend on itself")
            elif dependency not in known_claim_ids:
                failures.append(f"unknown dependency {dependency}")

    evidence_failures, has_strong_evidence = _validate_evidence(metadata, root)
    failures.extend(evidence_failures)
    if status == "checked" and not has_strong_evidence:
        failures.append("checked claim requires strong evidence")

    failures.extend(
        f"missing body section {marker}"
        for marker in REQUIRED_BODY_MARKERS
        if marker not in artifact.body
    )
    return failures


def main() -> int:
    failures: list[str] = []
    claim_files = sorted(CLAIMS_DIR.glob("CLAIM-*.md"))
    known_claim_ids = collect_claim_ids(ROOT)

    if not claim_files:
        failures.append("no claim files found")

    for path in claim_files:
        for failure in validate_claim(
            path,
            root=ROOT,
            known_claim_ids=known_claim_ids,
        ):
            failures.append(f"{path.relative_to(ROOT)} {failure}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("claim metadata ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
