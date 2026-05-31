"""Initialize a lightweight downstream AI math research project."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "templates"


def _write_if_missing(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding="utf-8")


def _template_text(src_name: str, replacements: dict[str, str]) -> str:
    text = (TEMPLATES_DIR / src_name).read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def init_project(target: Path, title: str) -> None:
    target.mkdir(parents=True, exist_ok=True)

    for dirname in ("problem", "claims", "plans", "reports", "tools", "scripts"):
        (target / dirname).mkdir(exist_ok=True)
    for dirname in (
        "experiments/EXP-0001-template/input",
        "experiments/EXP-0001-template/output",
    ):
        (target / dirname).mkdir(parents=True, exist_ok=True)

    _write_if_missing(
        target / "README.md",
        f"# {title}\n\nAI-assisted mathematical research workspace.\n",
    )
    _write_if_missing(
        target / "AGENTS.md",
        "# AGENTS.md\n\nFollow the AI for Math Research workflow discipline.\n",
    )
    _write_if_missing(
        target / "PLAN.md",
        "# Project Plan\n\nState the research phases and verification gates.\n",
    )

    today = date.today().isoformat()
    copies = {
        "claim.md": (
            "claims/CLAIM-0001-template.md",
            {
                "CLAIM-0000": "CLAIM-0001-template",
                "YYYY-MM-DD": today,
            },
        ),
        "plan.md": (
            "plans/PLAN-0001-template.md",
            {
                "PLAN-0000": "PLAN-0001-template",
                "YYYY-MM-DD": today,
            },
        ),
        "experiment.md": (
            "experiments/EXP-0001-template/experiment.md",
            {
                "EXP-0000": "EXP-0001-template",
                "YYYY-MM-DD": today,
            },
        ),
        "report.md": (
            "reports/REPORT-0001-template.md",
            {
                "REPORT-0000": "REPORT-0001-template",
                "YYYY-MM-DD": today,
            },
        ),
    }
    for src_name, (dest_name, replacements) in copies.items():
        _write_if_missing(
            target / dest_name,
            _template_text(src_name, replacements),
        )

    _write_if_missing(
        target / "problem/problem.md",
        "# Problem\n\nState the mathematical problem.\n",
    )
    _write_if_missing(
        target / "tools/tools.md",
        "# Tools\n\nRecord available tools and caveats.\n",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Target project directory")
    parser.add_argument("--title", default="AI Math Research Project")
    args = parser.parse_args(argv)

    init_project(Path(args.target), args.title)
    print(f"initialized {Path(args.target).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
