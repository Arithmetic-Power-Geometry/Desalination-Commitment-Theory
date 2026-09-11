#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e .[dev]
pytest
python scripts/run_experiments.py
python scripts/run_physical_validation.py
python scripts/run_full_physical_attack.py
python scripts/run_novelty_attack.py
python scripts/validate_artifact.py
python scripts/final_print.py
echo "Complete reproduction including physical and HDC novelty attacks finished."
