.PHONY: test lint claims experiments reports index check run-template

test:
	python -m unittest discover -s tests

lint:
	python -m ruff check .

claims:
	python scripts/check_claims.py

experiments:
	python scripts/check_experiments.py

reports:
	python scripts/check_reports.py

index:
	python scripts/make_index.py

check: claims experiments reports test

run-template:
	python scripts/run_experiment.py EXP-0001-template
