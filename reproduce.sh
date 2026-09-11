#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e .[dev]
pytest
python scripts/run_experiments.py
python scripts/validate_artifact.py
python scripts/final_print.py
echo "Reproduction complete."
