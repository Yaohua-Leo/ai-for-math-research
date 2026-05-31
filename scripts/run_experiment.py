"""Run one experiment and capture reproducibility metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

try:
    from scripts.ledger import LedgerError, read_artifact
except ModuleNotFoundError:  # pragma: no cover - CLI execution fallback
    from ledger import LedgerError, read_artifact

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = ROOT / "experiments"


def _resolve_experiment(name: str, root: Path = ROOT) -> Path:
    path = Path(name)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] == "experiments":
        return root / path
    return root / "experiments" / name


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _git_commit(root: Path) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _hash_tree(
    base: Path,
    key_root: Path,
    *,
    skip: set[Path] | None = None,
) -> dict[str, str]:
    if not base.exists():
        return {}
    skip = {path.resolve() for path in (skip or set())}
    files = (
        [base]
        if base.is_file()
        else sorted(path for path in base.rglob("*") if path.is_file())
    )
    hashes: dict[str, str] = {}
    for path in files:
        if path.resolve() in skip:
            continue
        hashes[_relative(path, key_root)] = _hash_file(path)
    return hashes


def _experiment_metadata(experiment: Path) -> dict[str, Any]:
    experiment_md = experiment / "experiment.md"
    if not experiment_md.exists():
        return {}
    try:
        return read_artifact(experiment_md).metadata
    except LedgerError:
        return {}


def _timeout(metadata: dict[str, Any]) -> int | None:
    timeout_seconds = metadata.get("timeout_seconds")
    if isinstance(timeout_seconds, int) and timeout_seconds > 0:
        return timeout_seconds
    return None


def _reproduction_command(experiment: Path, root: Path) -> str:
    experiment_name = experiment.name
    try:
        experiment.relative_to(root / "experiments")
    except ValueError:
        experiment_name = _relative(experiment, root)
    return f"python scripts/run_experiment.py {experiment_name}"


def _metadata_payload(
    *,
    command: list[str],
    completed: subprocess.CompletedProcess[str] | None,
    timed_out: bool,
    experiment: Path,
    root: Path,
    stdout_path: Path,
    stderr_path: Path,
    input_hashes: dict[str, str],
    output_hashes: dict[str, str],
) -> dict[str, Any]:
    exit_code = 124 if timed_out else completed.returncode if completed else 1
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "command": command,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "git_commit": _git_commit(root),
        "python": {
            "version": sys.version,
            "executable": sys.executable,
        },
        "platform": platform.platform(),
        "cwd": str(root),
        "experiment": _relative(experiment, root),
        "stdout_path": _relative(stdout_path, root),
        "stderr_path": _relative(stderr_path, root),
        "input_hashes": input_hashes,
        "output_hashes": output_hashes,
        "reproduction_command": _reproduction_command(experiment, root),
        "dependencies": {
            "PyYAML": yaml.__version__,
        },
    }


def run_experiment(experiment: Path, *, root: Path = ROOT) -> int:
    root = root.resolve()
    experiment = experiment.resolve()
    run_py = experiment / "run.py"
    output_dir = experiment / "output"
    output_dir.mkdir(exist_ok=True)

    if not run_py.exists():
        print(f"FAIL: {_relative(run_py, root)} does not exist")
        return 1

    metadata = _experiment_metadata(experiment)
    timeout_seconds = _timeout(metadata)
    command = [sys.executable, str(run_py)]
    stdout_path = output_dir / "stdout.txt"
    stderr_path = output_dir / "stderr.txt"
    environment_path = output_dir / "environment.json"
    run_metadata_path = output_dir / "run-metadata.json"
    input_hashes = _hash_tree(experiment / "input", experiment)

    timed_out = False
    completed: subprocess.CompletedProcess[str] | None = None
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout_path.write_text(exc.stdout or "", encoding="utf-8")
        stderr_path.write_text(exc.stderr or "experiment timed out\n", encoding="utf-8")

    output_hashes = _hash_tree(
        output_dir,
        experiment,
        skip={run_metadata_path, environment_path},
    )
    payload = _metadata_payload(
        command=command,
        completed=completed,
        timed_out=timed_out,
        experiment=experiment,
        root=root,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        input_hashes=input_hashes,
        output_hashes=output_hashes,
    )
    environment_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    run_metadata_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"{_relative(experiment, root)} exited with {payload['exit_code']}")
    return int(payload["exit_code"])


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
