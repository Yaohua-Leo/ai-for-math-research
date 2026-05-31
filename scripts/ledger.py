"""Shared helpers for YAML-frontmatter research ledger artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class LedgerError(ValueError):
    """Raised when a ledger artifact cannot be parsed safely."""


@dataclass(frozen=True)
class LedgerArtifact:
    path: Path
    metadata: dict[str, Any]
    body: str


def parse_frontmatter(text: str, path: Path) -> LedgerArtifact:
    """Parse a Markdown file with required YAML frontmatter."""

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise LedgerError(f"{path}: missing YAML frontmatter")

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        raise LedgerError(f"{path}: missing closing YAML frontmatter marker")

    yaml_text = "".join(lines[1:closing_index])
    try:
        metadata = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        raise LedgerError(f"{path}: invalid YAML frontmatter: {exc}") from exc

    if not isinstance(metadata, dict):
        raise LedgerError(f"{path}: YAML frontmatter must be a mapping")

    body = "".join(lines[closing_index + 1 :])
    return LedgerArtifact(path=path, metadata=metadata, body=body)


def read_artifact(path: Path) -> LedgerArtifact:
    return parse_frontmatter(path.read_text(encoding="utf-8"), path)


def display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def require_fields(metadata: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    return [
        f"missing metadata field {field}"
        for field in fields
        if field not in metadata
    ]


def require_string_list(metadata: dict[str, Any], field: str) -> list[str]:
    value = metadata.get(field)
    if not isinstance(value, list):
        return [f"metadata field {field} must be a list"]
    if not all(isinstance(item, str) for item in value):
        return [f"metadata field {field} must contain only strings"]
    return []


def metadata_path_exists(path_value: str, root: Path) -> bool:
    return (root / path_value).exists()
