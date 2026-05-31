from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import check_claims, check_experiments, check_reports, init_project


class ValidationTests(unittest.TestCase):
    def test_template_claim_is_valid(self) -> None:
        path = Path("claims/CLAIM-0001-template.md")
        self.assertEqual(check_claims.validate_claim(path), [])

    def test_template_experiment_is_valid(self) -> None:
        path = Path("experiments/EXP-0001-template")
        self.assertEqual(check_experiments.validate_experiment(path), [])

    def test_template_report_is_valid(self) -> None:
        path = Path("reports/REPORT-0001-template.md")
        self.assertEqual(check_reports.validate_report(path), [])

    def test_init_project_creates_core_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            init_project.init_project(target, "Sample")
            self.assertTrue((target / "README.md").exists())
            self.assertTrue((target / "claims/CLAIM-0001-template.md").exists())
            self.assertTrue(
                (target / "experiments/EXP-0001-template/experiment.md").exists()
            )
            claim_ids = check_claims.collect_claim_ids(target)
            self.assertEqual(
                check_claims.validate_claim(
                    target / "claims/CLAIM-0001-template.md",
                    root=target,
                    known_claim_ids=claim_ids,
                ),
                [],
            )
            self.assertEqual(
                check_experiments.validate_experiment(
                    target / "experiments/EXP-0001-template",
                    root=target,
                    known_claim_ids=claim_ids,
                ),
                [],
            )
            self.assertEqual(
                check_reports.validate_report(
                    target / "reports/REPORT-0001-template.md"
                ),
                [],
            )

    def test_toy_case_artifact_chain_is_valid(self) -> None:
        claim_ids = check_claims.collect_claim_ids()
        self.assertIn("CLAIM-0002-toy-homology", claim_ids)
        self.assertEqual(
            check_claims.validate_claim(
                Path("claims/CLAIM-0002-toy-homology.md"),
                known_claim_ids=claim_ids,
            ),
            [],
        )
        self.assertEqual(
            check_experiments.validate_experiment(
                Path("experiments/EXP-0002-toy-homology"),
                known_claim_ids=claim_ids,
            ),
            [],
        )
        self.assertEqual(
            check_reports.validate_report(Path("reports/REPORT-0002-toy-homology.md")),
            [],
        )


if __name__ == "__main__":
    unittest.main()
