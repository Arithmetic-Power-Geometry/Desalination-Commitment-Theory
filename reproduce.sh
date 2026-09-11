#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e .[dev]
pytest
python scripts/run_experiments.py
python scripts/run_physical_validation.py
python scripts/validate_artifact.py
python scripts/final_print.py
echo "Full two-level reproduction complete."
