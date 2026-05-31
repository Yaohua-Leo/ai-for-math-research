"""Run a registry-defined math tool command."""

from __future__ import annotations

try:
    from scripts.tool_runner import main
except ModuleNotFoundError:  # pragma: no cover - CLI execution fallback
    from tool_runner import main


if __name__ == "__main__":
    raise SystemExit(main())
