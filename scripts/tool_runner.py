"""Run registry-defined math tool smoke checks with captured metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import locale
import platform
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "tools" / "registry.yaml"


class ToolRunnerError(ValueError):
    """Raised when registry data cannot produce a safe command."""


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _decode_output(data: str | bytes | None) -> str:
    if data is None:
        return ""
    if isinstance(data, str):
        return data

    sample = data[:80]
    encodings = ["utf-8"]
    if sample.count(b"\x00") >= max(1, len(sample) // 8):
        encodings.insert(0, "utf-16le")
    preferred = locale.getpreferredencoding(False)
    if preferred not in encodings:
        encodings.append(preferred)

    for encoding in encodings:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _relative(path: Path, root: Path = ROOT) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ToolRunnerError(f"{path}: invalid YAML: {exc}") from exc

    if not isinstance(data, dict):
        raise ToolRunnerError(f"{path}: registry must be a mapping")
    return data


def tools_by_id(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tools = registry.get("tools")
    if not isinstance(tools, list):
        raise ToolRunnerError("registry field tools must be a list")

    by_id: dict[str, dict[str, Any]] = {}
    for tool in tools:
        if not isinstance(tool, dict):
            raise ToolRunnerError("each registry tool must be a mapping")
        tool_id = tool.get("id")
        if not isinstance(tool_id, str):
            raise ToolRunnerError("each registry tool needs a string id")
        if tool_id in by_id:
            raise ToolRunnerError(f"duplicate tool id {tool_id}")
        by_id[tool_id] = tool
    return by_id


def group_tool_ids(registry: dict[str, Any], group_ids: set[str]) -> set[str]:
    groups = registry.get("groups", [])
    if not isinstance(groups, list):
        raise ToolRunnerError("registry field groups must be a list")

    allowed: set[str] = set()
    for group in groups:
        if not isinstance(group, dict):
            raise ToolRunnerError("each registry group must be a mapping")
        group_id = group.get("id")
        if group_id not in group_ids:
            continue
        tool_ids = group.get("tool_ids")
        if not isinstance(tool_ids, list) or not all(
            isinstance(tool_id, str) for tool_id in tool_ids
        ):
            raise ToolRunnerError(f"group {group_id} must have string tool_ids")
        allowed.update(tool_ids)
    return allowed


def _string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ToolRunnerError(f"{field} must be a list of strings")
    if not value:
        raise ToolRunnerError(f"{field} must not be empty")
    return value


def command_spec(tool: dict[str, Any], mode: str) -> dict[str, Any]:
    if mode == "version":
        command = tool.get("version_command")
        if command is None:
            command = tool.get("command")
        return {"command": _string_list(command, "version command"), "stdin": None}

    if mode == "smoke":
        smoke = tool.get("smoke")
        if not isinstance(smoke, dict):
            raise ToolRunnerError(f"tool {tool.get('id')} has no smoke command")
        return {
            "command": _string_list(smoke.get("command"), "smoke command"),
            "stdin": smoke.get("stdin"),
            "expected_stdout_contains": smoke.get("expected_stdout_contains"),
            "timeout_seconds": smoke.get("timeout_seconds"),
        }

    raise ToolRunnerError(f"unknown mode {mode}")


def _write_run_artifacts(
    output: Path,
    payload: dict[str, Any],
    stdout: str,
    stderr: str,
) -> dict[str, Any]:
    output.parent.mkdir(parents=True, exist_ok=True)
    stdout_path = output.with_suffix(".stdout.txt")
    stderr_path = output.with_suffix(".stderr.txt")
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    payload["stdout_path"] = _relative(stdout_path)
    payload["stderr_path"] = _relative(stderr_path)
    payload["stdout_sha256"] = _sha256_text(stdout)
    payload["stderr_sha256"] = _sha256_text(stderr)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def run_tool(
    tool_id: str,
    *,
    mode: str,
    registry_path: Path = DEFAULT_REGISTRY,
    dry_run: bool = False,
    allow_unverified: bool = False,
    output: Path | None = None,
    timeout_seconds: int | None = None,
    allowed_groups: set[str] | None = None,
) -> dict[str, Any]:
    registry = load_registry(registry_path)
    tools = tools_by_id(registry)
    tool = tools.get(tool_id)
    if tool is None:
        raise ToolRunnerError(f"unknown tool {tool_id}")

    if allowed_groups:
        allowed_tools = group_tool_ids(registry, allowed_groups)
        if tool_id not in allowed_tools:
            allowed = ", ".join(sorted(allowed_groups))
            raise ToolRunnerError(
                f"tool {tool_id} is not in runner group(s): {allowed}"
            )

    if tool.get("status") != "verified" and not dry_run and not allow_unverified:
        raise ToolRunnerError(
            f"tool {tool_id} status is {tool.get('status')!r}; use dry-run or allow "
            "unverified before executing"
        )

    spec = command_spec(tool, mode)
    command = spec["command"]
    stdin = spec.get("stdin")
    if stdin is not None and not isinstance(stdin, str):
        raise ToolRunnerError("stdin must be a string when present")

    smoke_timeout = spec.get("timeout_seconds")
    if timeout_seconds is None and isinstance(smoke_timeout, int):
        timeout_seconds = smoke_timeout
    if timeout_seconds is None:
        timeout_seconds = 30

    payload: dict[str, Any] = {
        "schema_version": 1,
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "tool_id": tool_id,
        "mode": mode,
        "dry_run": dry_run,
        "status": tool.get("status"),
        "route": tool.get("route"),
        "command": command,
        "stdin_sha256": _sha256_text(stdin) if stdin else None,
        "cwd": str(ROOT),
        "platform": platform.platform(),
        "python": {"version": sys.version, "executable": sys.executable},
        "timeout_seconds": timeout_seconds,
    }

    if dry_run:
        payload["would_run"] = True
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        return payload

    start = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            input=stdin.encode("utf-8") if stdin is not None else None,
            cwd=ROOT,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
        timed_out = False
        stdout = _decode_output(completed.stdout)
        stderr = _decode_output(completed.stderr)
        exit_code = completed.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = _decode_output(exc.stdout)
        stderr = _decode_output(exc.stderr) or "tool smoke check timed out\n"
        exit_code = 124

    expected = spec.get("expected_stdout_contains")
    passed = exit_code == 0
    if isinstance(expected, str):
        passed = passed and expected in stdout

    payload.update(
        {
            "duration_seconds": round(time.monotonic() - start, 6),
            "exit_code": exit_code,
            "timed_out": timed_out,
            "expected_stdout_contains": expected,
            "passed": passed,
            "stdout_sha256": _sha256_text(stdout),
            "stderr_sha256": _sha256_text(stderr),
        }
    )

    if output:
        _write_run_artifacts(output, payload, stdout, stderr)
    else:
        payload["stdout"] = stdout
        payload["stderr"] = stderr

    return payload


def build_parser(description: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description or __doc__)
    parser.add_argument("tool", help="Tool id from tools/registry.yaml")
    parser.add_argument("--mode", choices=("version", "smoke"), default="smoke")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-unverified", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--timeout-seconds", type=int)
    return parser


def main(
    argv: list[str] | None = None,
    *,
    allowed_groups: set[str] | None = None,
    description: str | None = None,
) -> int:
    parser = build_parser(description)
    args = parser.parse_args(argv)
    try:
        payload = run_tool(
            args.tool,
            mode=args.mode,
            registry_path=args.registry,
            dry_run=args.dry_run,
            allow_unverified=args.allow_unverified,
            output=args.output,
            timeout_seconds=args.timeout_seconds,
            allowed_groups=allowed_groups,
        )
    except ToolRunnerError as exc:
        print(f"FAIL: {exc}")
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("passed", True) else 1
