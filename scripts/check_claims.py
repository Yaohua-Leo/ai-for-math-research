"""Validate claim files for required research metadata."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "claims"

REQUIRED_MARKERS = (
    "Status:",
    "Statement:",
    "Assumptions:",
    "Dependencies:",
    "Proof sketch:",
    "Known gaps:",
    "References:",
    "Computational evidence:",
    "Formalization status:",
    "Verification notes:",
    "Last updated:",
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


def _status_from_text(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("Status:"):
            return line.removeprefix("Status:").strip()
    return None


def validate_claim(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    failures = [
        f"missing {marker}" for marker in REQUIRED_MARKERS if marker not in text
    ]
    status = _status_from_text(text)
    if status not in VALID_STATUSES:
        failures.append(
            f"invalid status {status!r}; expected one of {sorted(VALID_STATUSES)}"
        )
    return failures


def main() -> int:
    failures: list[str] = []
    claim_files = sorted(CLAIMS_DIR.glob("CLAIM-*.md"))

    if not claim_files:
        failures.append("no claim files found")

    for path in claim_files:
        for failure in validate_claim(path):
            failures.append(f"{path.relative_to(ROOT)} {failure}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("claim metadata ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
