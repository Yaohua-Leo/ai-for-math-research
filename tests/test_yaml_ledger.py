from __future__ import annotations

import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts import check_claims, ledger, run_experiment


def _claim_text(frontmatter: str = "") -> str:
    frontmatter = textwrap.dedent(frontmatter)
    header = (
        textwrap.dedent(
            """\
            ---
            schema_version: 1
            id: CLAIM-0001
            status: checked
            type: theorem
            depends_on: []
            evidence:
              - type: exact-computation
                path: experiments/EXP-0001/output/results.json
                fully_verifiable: true
            assumptions: []
            last_updated: "2026-06-01"
            """
        )
        + frontmatter
        + "---\n"
    )
    body = textwrap.dedent(
        """\
        # CLAIM-0001: Toy Claim

        ## Statement

        A checked toy statement.

        ## Assumptions

        - None.

        ## Proof Sketch

        Verified by the exact computation listed in the evidence.

        ## Known Gaps

        - None.

        ## References

        - None.

        ## Computational Evidence

        - `experiments/EXP-0001/output/results.json`

        ## Formalization Status

        Not formalized.

        ## Verification Notes

        Exact finite computation is fully reproducible.
        """
    )
    return header + body


class FrontmatterTests(unittest.TestCase):
    def test_parse_yaml_frontmatter(self) -> None:
        artifact = ledger.parse_frontmatter(
            "---\nid: CLAIM-0001\nstatus: idea\n---\n# Body\n",
            Path("CLAIM-0001.md"),
        )

        self.assertEqual(artifact.metadata["id"], "CLAIM-0001")
        self.assertEqual(artifact.body, "# Body\n")

    def test_missing_frontmatter_fails(self) -> None:
        with self.assertRaisesRegex(ledger.LedgerError, "missing YAML frontmatter"):
            ledger.parse_frontmatter("# Body\n", Path("CLAIM-0001.md"))

    def test_invalid_yaml_fails(self) -> None:
        with self.assertRaisesRegex(ledger.LedgerError, "invalid YAML frontmatter"):
            ledger.parse_frontmatter("---\n: bad\n---\n# Body\n", Path("bad.md"))

    def test_non_mapping_yaml_fails(self) -> None:
        with self.assertRaisesRegex(ledger.LedgerError, "must be a mapping"):
            ledger.parse_frontmatter("---\n- item\n---\n# Body\n", Path("bad.md"))


class ClaimValidatorTests(unittest.TestCase):
    def test_checked_claim_accepts_fully_verifiable_exact_computation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "experiments/EXP-0001/output/results.json"
            evidence.parent.mkdir(parents=True)
            evidence.write_text('{"ok": true}\n', encoding="utf-8")
            claim = root / "claims/CLAIM-0001.md"
            claim.parent.mkdir()
            claim.write_text(_claim_text(), encoding="utf-8")

            failures = check_claims.validate_claim(
                claim,
                root=root,
                known_claim_ids={"CLAIM-0001"},
            )

        self.assertEqual(failures, [])

    def test_unknown_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "experiments/EXP-0001/output/results.json"
            evidence.parent.mkdir(parents=True)
            evidence.write_text('{"ok": true}\n', encoding="utf-8")
            claim = root / "claims/CLAIM-0001.md"
            claim.parent.mkdir()
            claim.write_text(
                _claim_text("depends_on:\n  - CLAIM-9999\n"),
                encoding="utf-8",
            )

            failures = check_claims.validate_claim(
                claim,
                root=root,
                known_claim_ids={"CLAIM-0001"},
            )

        self.assertIn("unknown dependency CLAIM-9999", failures)

    def test_missing_evidence_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            claim = root / "claims/CLAIM-0001.md"
            claim.parent.mkdir()
            claim.write_text(_claim_text(), encoding="utf-8")

            failures = check_claims.validate_claim(
                claim,
                root=root,
                known_claim_ids={"CLAIM-0001"},
            )

        self.assertIn(
            "evidence path experiments/EXP-0001/output/results.json does not exist",
            failures,
        )

    def test_checked_claim_requires_strong_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            claim = root / "claims/CLAIM-0001.md"
            claim.parent.mkdir()
            claim.write_text(
                _claim_text(
                    "evidence:\n"
                    "  - type: numerical-evidence\n"
                    "    path: experiments/EXP-0001/output/results.json\n"
                ),
                encoding="utf-8",
            )

            failures = check_claims.validate_claim(
                claim,
                root=root,
                known_claim_ids={"CLAIM-0001"},
            )

        self.assertIn("checked claim requires strong evidence", failures)


class ExperimentRunnerMetadataTests(unittest.TestCase):
    def test_run_experiment_writes_reproducibility_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            experiment = root / "experiments/EXP-0999-runner"
            output = experiment / "output"
            output.mkdir(parents=True)
            (experiment / "experiment.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    schema_version: 1
                    id: EXP-0999-runner
                    status: runnable
                    tool: python
                    command:
                      - python
                      - run.py
                    inputs: []
                    outputs:
                      - output/results.json
                    claims_affected: []
                    random_seed: null
                    timeout_seconds: 30
                    ---
                    # EXP-0999: Runner Test
                    """
                ),
                encoding="utf-8",
            )
            (experiment / "run.py").write_text(
                "from pathlib import Path\n"
                "Path(__file__).with_name('output').joinpath('results.json')"
                ".write_text('{\"ok\": true}\\n', encoding='utf-8')\n",
                encoding="utf-8",
            )

            exit_code = run_experiment.run_experiment(experiment, root=root)
            metadata = json.loads((output / "run-metadata.json").read_text())

        self.assertEqual(exit_code, 0)
        self.assertEqual(metadata["exit_code"], 0)
        self.assertIn("git_commit", metadata)
        self.assertIn("python", metadata)
        self.assertEqual(
            metadata["reproduction_command"],
            "python scripts/run_experiment.py EXP-0999-runner",
        )
        self.assertIn("output/results.json", metadata["output_hashes"])
