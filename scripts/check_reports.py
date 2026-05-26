"""Validate research report metadata."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"

REQUIRED_MARKERS = (
    "Status:",
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


def _status_from_text(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("Status:"):
            return line.removeprefix("Status:").strip()
    return None


def validate_report(path: Path) -> list[str]:
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
