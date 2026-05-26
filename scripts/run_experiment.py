"""Run one experiment and capture reproducibility metadata."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = ROOT / "experiments"


def _resolve_experiment(name: str) -> Path:
    path = Path(name)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == "experiments":
        return ROOT / path
    return EXPERIMENTS_DIR / name


def _environment_payload(command: list[str]) -> dict[str, object]:
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "command": command,
        "python": sys.version,
        "platform": platform.platform(),
        "cwd": str(ROOT),
    }


def run_experiment(experiment: Path) -> int:
    experiment = experiment.resolve()
    run_py = experiment / "run.py"
    output_dir = experiment / "output"
    output_dir.mkdir(exist_ok=True)

    if not run_py.exists():
        print(f"FAIL: {run_py.relative_to(ROOT)} does not exist")
        return 1

    command = [sys.executable, str(run_py)]
    environment = _environment_payload(command)
    (output_dir / "environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    (output_dir / "stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (output_dir / "stderr.txt").write_text(completed.stderr, encoding="utf-8")

    print(f"{experiment.relative_to(ROOT)} exited with {completed.returncode}")
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "experiment",
        help="Experiment name or path, for example EXP-0001",
    )
    args = parser.parse_args(argv)
    experiment = _resolve_experiment(args.experiment)
    return run_experiment(experiment)


if __name__ == "__main__":
    raise SystemExit(main())
