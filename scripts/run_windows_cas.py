"""Run smoke checks for Windows-native CAS and numerical tools."""

from __future__ import annotations

try:
    from scripts.tool_runner import main
except ModuleNotFoundError:  # pragma: no cover - CLI execution fallback
    from tool_runner import main


if __name__ == "__main__":
    raise SystemExit(
        main(
            allowed_groups={"windows-cas"},
            description=__doc__,
        )
    )
