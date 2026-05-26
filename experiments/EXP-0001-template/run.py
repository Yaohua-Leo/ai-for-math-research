"""Template experiment.

This experiment intentionally proves nothing mathematical. It exists to show
how an experiment can write structured output for the ledger.
"""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    experiment_dir = Path(__file__).resolve().parent
    output_dir = experiment_dir / "output"
    output_dir.mkdir(exist_ok=True)
    result = {
        "experiment": "EXP-0001-template",
        "status": "template-run",
        "mathematical_claims_supported": [],
        "message": "Template experiment completed; no mathematical claim made.",
    }
    (output_dir / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("template experiment completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
