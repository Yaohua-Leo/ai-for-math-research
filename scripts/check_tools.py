"""Validate the machine-readable math tool registry."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

try:
    from scripts.ledger import LedgerError, parse_frontmatter
    from scripts.tool_runner import DEFAULT_REGISTRY, ToolRunnerError, load_registry
except ModuleNotFoundError:  # pragma: no cover - CLI execution fallback
    from ledger import LedgerError, parse_frontmatter
    from tool_runner import DEFAULT_REGISTRY, ToolRunnerError, load_registry

ROOT = Path(__file__).resolve().parents[1]

VALID_TOOL_STATUSES = {"verified", "optional", "planned", "not-configured"}
VALID_EVIDENCE_MODES = {
    "exact-computation",
    "finite-experiment",
    "numerical-evidence",
    "formal-check",
    "not-evidence",
    "reference-only",
}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def _as_list(value: Any, field: str, failures: list[str]) -> list[Any]:
    if not isinstance(value, list):
        failures.append(f"{field} must be a list")
        return []
    return value


def _string_list(value: Any, field: str, failures: list[str]) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        failures.append(f"{field} must be a list of strings")


def _path_exists(path_value: Any, field: str, failures: list[str]) -> None:
    if not isinstance(path_value, str):
        failures.append(f"{field} must be a string path")
        return
    if not (ROOT / path_value).exists():
        failures.append(f"{field} path does not exist: {path_value}")


def _validate_skill(path_value: str, expected_id: str, failures: list[str]) -> None:
    path = ROOT / path_value
    if not path.exists():
        failures.append(f"skill path does not exist: {path_value}")
        return
    try:
        artifact = parse_frontmatter(path.read_text(encoding="utf-8"), path)
    except LedgerError as exc:
        failures.append(str(exc))
        return

    metadata = artifact.metadata
    name = metadata.get("name")
    description = metadata.get("description")
    if name != expected_id:
        failures.append(
            f"skill {path_value} name {name!r} does not match {expected_id}"
        )
    if not isinstance(description, str) or not description.strip():
        failures.append(f"skill {path_value} needs a non-empty description")


def validate_registry(path: Path = DEFAULT_REGISTRY) -> list[str]:
    failures: list[str] = []
    try:
        registry = load_registry(path)
    except (ToolRunnerError, OSError, yaml.YAMLError) as exc:
        return [str(exc)]

    if registry.get("schema_version") != 1:
        failures.append("schema_version must be 1")

    tools = _as_list(registry.get("tools"), "tools", failures)
    tool_ids: set[str] = set()
    for index, tool in enumerate(tools):
        prefix = f"tools[{index}]"
        if not isinstance(tool, dict):
            failures.append(f"{prefix} must be a mapping")
            continue

        tool_id = tool.get("id")
        if not isinstance(tool_id, str) or not ID_RE.fullmatch(tool_id):
            failures.append(f"{prefix}.id must be lowercase hyphen id")
        elif tool_id in tool_ids:
            failures.append(f"duplicate tool id {tool_id}")
        elif tool_id:
            tool_ids.add(tool_id)

        status = tool.get("status")
        if status not in VALID_TOOL_STATUSES:
            failures.append(f"{prefix}.status invalid: {status!r}")

        evidence_mode = tool.get("evidence_mode")
        if evidence_mode not in VALID_EVIDENCE_MODES:
            failures.append(f"{prefix}.evidence_mode invalid: {evidence_mode!r}")

        if status == "verified":
            if not tool.get("command"):
                failures.append(f"{prefix}.command is required for verified tools")
            if not isinstance(tool.get("route"), str) or not tool.get("route"):
                failures.append(f"{prefix}.route is required for verified tools")
            caveat = tool.get("reproducibility_caveat")
            if not isinstance(caveat, str) or not caveat:
                failures.append(
                    f"{prefix}.reproducibility_caveat is required for verified tools"
                )

        if "command" in tool:
            _string_list(tool.get("command"), f"{prefix}.command", failures)
        if "version_command" in tool:
            _string_list(
                tool.get("version_command"),
                f"{prefix}.version_command",
                failures,
            )

        smoke = tool.get("smoke")
        if smoke is not None:
            if not isinstance(smoke, dict):
                failures.append(f"{prefix}.smoke must be a mapping")
            else:
                _string_list(smoke.get("command"), f"{prefix}.smoke.command", failures)

    groups = _as_list(registry.get("groups", []), "groups", failures)
    for index, group in enumerate(groups):
        prefix = f"groups[{index}]"
        if not isinstance(group, dict):
            failures.append(f"{prefix} must be a mapping")
            continue
        group_id = group.get("id")
        if not isinstance(group_id, str) or not ID_RE.fullmatch(group_id):
            failures.append(f"{prefix}.id must be lowercase hyphen id")
        tool_id_values = group.get("tool_ids")
        _string_list(tool_id_values, f"{prefix}.tool_ids", failures)
        if isinstance(tool_id_values, list):
            for tool_id in tool_id_values:
                if isinstance(tool_id, str) and tool_id not in tool_ids:
                    failures.append(f"{prefix}.tool_ids unknown tool {tool_id}")

    project_skills = _as_list(
        registry.get("project_skills", []),
        "project_skills",
        failures,
    )
    for index, skill in enumerate(project_skills):
        prefix = f"project_skills[{index}]"
        if not isinstance(skill, dict):
            failures.append(f"{prefix} must be a mapping")
            continue
        skill_id = skill.get("id")
        path_value = skill.get("path")
        if not isinstance(skill_id, str) or not ID_RE.fullmatch(skill_id):
            failures.append(f"{prefix}.id must be lowercase hyphen id")
            continue
        if isinstance(path_value, str):
            _validate_skill(path_value, skill_id, failures)
        else:
            failures.append(f"{prefix}.path must be a string")

        tool_id_values = skill.get("tool_ids", [])
        _string_list(tool_id_values, f"{prefix}.tool_ids", failures)
        if isinstance(tool_id_values, list):
            for tool_id in tool_id_values:
                if isinstance(tool_id, str) and tool_id not in tool_ids:
                    failures.append(f"{prefix}.tool_ids unknown tool {tool_id}")

    adapters = _as_list(registry.get("adapters", []), "adapters", failures)
    for index, adapter in enumerate(adapters):
        prefix = f"adapters[{index}]"
        if not isinstance(adapter, dict):
            failures.append(f"{prefix} must be a mapping")
            continue
        if adapter.get("status") in {"available", "implemented"} and "path" in adapter:
            _path_exists(adapter.get("path"), f"{prefix}.path", failures)

    reviewed = _as_list(
        registry.get("reviewed_open_source_skills", []),
        "reviewed_open_source_skills",
        failures,
    )
    for index, skill in enumerate(reviewed):
        prefix = f"reviewed_open_source_skills[{index}]"
        if not isinstance(skill, dict):
            failures.append(f"{prefix} must be a mapping")
            continue
        for field in ("id", "source_url", "license", "reuse_policy"):
            if not isinstance(skill.get(field), str) or not skill.get(field):
                failures.append(f"{prefix}.{field} must be a non-empty string")

    return failures


def main() -> int:
    failures = validate_registry()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("tool registry ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
