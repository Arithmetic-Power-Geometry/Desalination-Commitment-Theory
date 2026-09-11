#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e .[dev]
pytest
python scripts/run_experiments.py
python scripts/run_physical_validation.py
python scripts/run_level2_attack.py
python scripts/validate_artifact.py
python scripts/final_print.py
echo "Complete reproduction including Level-2 attack finished."
