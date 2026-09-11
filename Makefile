install:
	python -m pip install -e .[dev]

test:
	pytest

results:
	python scripts/run_experiments.py

validate:
	python scripts/validate_artifact.py

reproduce:
	bash reproduce.sh
