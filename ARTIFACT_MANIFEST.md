# Artifact Manifest

## Core package
- `src/dct/model.py` — nonlinear dynamic water-system proxy
- `src/dct/metrics.py` — commitment, avoidance, preservation, delay metrics
- `src/dct/control.py` — preventive intervention and timing searches
- `src/dct/multisource.py` — shared-resource multi-source tests
- `src/dct/uncertainty.py` — Monte Carlo robustness

## Experiments
- `scripts/run_experiments.py`
- `scripts/validate_artifact.py`
- `scripts/final_print.py`

## Reproducibility
- `reproduce.sh`
- `Makefile`
- `.github/workflows/reproducibility.yml`
- `tests/`

## Generated outputs
- `results/REPORT.md`
- `results/tables/*.csv`
- `results/figures/*.png`

All numerical outputs are synthetic/model-generated unless explicitly replaced by external empirical data in future work.
