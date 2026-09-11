# Artifact Manifest

## Core package
- `src/dct/model.py` — nonlinear dynamic water-system proxy
- `src/dct/metrics.py` — commitment, avoidance, preservation, delay metrics
- `src/dct/control.py` — preventive intervention and timing searches
- `src/dct/multisource.py` — shared-resource multi-source tests
- `src/dct/uncertainty.py` — Monte Carlo robustness

## Level 2 physical package
- `src/dct/physics/aquifer2d.py` — 2-D hydraulic-head / Darcy-like flow / advection-dispersion salinity benchmark
- `src/dct/physics/metrics2d.py` — physical-model summary and prevention-window search
- `src/dct/physics/attack_suite.py` — complete parameter, mechanism, timing, uncertainty, convergence, and alternative-formulation attack suite

## Experiment runners
- `scripts/run_experiments.py` — Level 1 controlled benchmark
- `scripts/run_physical_validation.py` — Level 2 base physical benchmark
- `scripts/run_level2_attack.py` — complete Level 2 physical attack
- `scripts/validate_artifact.py` — checks required generated outputs
- `scripts/final_print.py` — prints Level 1, Level 2A and Level 2B results

## Reproducibility
- `reproduce.sh`
- `Makefile`
- `.github/workflows/reproducibility.yml`
- `tests/`

## Generated outputs
- `results/REPORT.md`
- `results/tables/*.csv`
- `results/figures/*.png`
- `results/physical/`
- `results/attack/`

## Complete Level-2 attack coverage
1. Physical parameter-space search
2. Recharge-only / pumping-reduction-only / combined ablation
3. Intervention-magnitude sweep
4. Intervention-timing sweep
5. Salinity-front analysis
6. Pumping/recharge regime sweep
7. Hydraulic parameter sweep
8. Demand/head stress
9. Global sensitivity
10. Level-2 Monte Carlo uncertainty
11. Kill tests
12. Grid/time convergence
13. Alternative physical formulation
14. Delay-intervention full-prevention frontier

The current Level 2 attack preserves hidden commitment but does not support `K_P>0` or a finite full-prevention window in the tested benchmark family. This negative result is intentionally retained as a falsification outcome.

All numerical outputs are synthetic/model-generated unless explicitly replaced by external empirical data in future work.
