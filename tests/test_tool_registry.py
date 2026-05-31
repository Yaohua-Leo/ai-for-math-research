from __future__ import annotations

import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts import check_tools, tool_runner


def _temporary_registry(text: str) -> Path:
    root = Path(tempfile.mkdtemp())
    path = root / "registry.yaml"
    path.write_text(textwrap.dedent(text), encoding="utf-8")
    return path


class ToolRegistryTests(unittest.TestCase):
    def test_current_registry_is_valid(self) -> None:
        self.assertEqual(check_tools.validate_registry(), [])

    def test_dry_run_for_wsl_algebra_does_not_execute_tool(self) -> None:
        payload = tool_runner.run_tool(
            "sagemath-wsl",
            mode="smoke",
            dry_run=True,
            allowed_groups={"wsl-algebra"},
        )

        self.assertTrue(payload["dry_run"])
        self.assertEqual(payload["tool_id"], "sagemath-wsl")
        self.assertEqual(payload["command"][0], "wsl.exe")

    def test_exact_python_smoke_records_metadata(self) -> None:
        registry = _temporary_registry(
            f"""\
            schema_version: 1
            tools:
              - id: exact-python
                status: verified
                route: native
                command:
                  - {sys.executable}
                evidence_mode: exact-computation
                reproducibility_caveat: temporary test registry
                smoke:
                  command:
                    - {sys.executable}
                    - -c
                    - print(2+2)
                  expected_stdout_contains: "4"
            """
        )
        output = registry.parent / "exact-python.json"

        payload = tool_runner.run_tool(
            "exact-python",
            mode="smoke",
            registry_path=registry,
            output=output,
        )

        self.assertTrue(payload["passed"])
        self.assertEqual(payload["exit_code"], 0)
        self.assertTrue(output.exists())
        self.assertTrue(output.with_suffix(".stdout.txt").exists())
        self.assertIn("stdout_sha256", payload)

    def test_formal_version_check_shape_records_metadata(self) -> None:
        registry = _temporary_registry(
            f"""\
            schema_version: 1
            tools:
              - id: formal-python-version
                status: verified
                route: native
                command:
                  - {sys.executable}
                version_command:
                  - {sys.executable}
                  - --version
                evidence_mode: formal-check
                reproducibility_caveat: temporary formal-tool version check
            """
        )

        payload = tool_runner.run_tool(
            "formal-python-version",
            mode="version",
            registry_path=registry,
        )

        self.assertEqual(payload["exit_code"], 0)
        self.assertIn("Python", payload["stdout"])

    @unittest.skipUnless(
        os.environ.get("AI_MATH_RUN_EXTERNAL_SMOKE") == "1",
        "external WSL smoke checks are opt-in",
    )
    def test_optional_wsl_sage_smoke(self) -> None:
        payload = tool_runner.run_tool(
            "sagemath-wsl",
            mode="smoke",
            allowed_groups={"wsl-algebra"},
            timeout_seconds=90,
        )

        self.assertTrue(payload["passed"])


if __name__ == "__main__":
    unittest.main()
