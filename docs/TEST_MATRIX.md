# Software Test Matrix

## Level 1 — Controlled nonlinear benchmark

| Test | Output | Pass / interpretation |
|---|---|---|
| Present requirement | `Q_D(t0)` | Establish whether present desalination is zero |
| Baseline future | `V_D_baseline` | Positive value establishes future replacement burden |
| Immediate intervention | `V_D_immediate` | Must not exceed baseline |
| Hidden commitment | boolean | `Q_D(t0)=0` and `V_D_baseline>0` |
| Avoidance multiplier | `K_D` | Counterfactual avoided desalination per intervention volume |
| Preservation multiplier | `K_P` | Positive value indicates benefit beyond direct substitution |
| Delay sweep | `delay_frontier.csv` | Tests closing prevention window |
| Dose sweep | `dose_response.csv` | Tests nonlinear response |
| Uncertainty | `uncertainty.csv` | Tests robustness |
| Multi-source | `multisource.csv` | Tests shared-resource commitment |
| Kill: no degradation | pytest | Commitment must vanish |
| Kill: no recovery | pytest | Preservation effect must vanish |
| Reproduction | `reproduce.sh` | Tests full artifact deterministically |

## Level 2A — Physical groundwater/salinity benchmark

| Test | Output | Interpretation |
|---|---|---|
| Initial salinity boundary | pytest | Inland fresh / coastal saline boundaries are enforced |
| Hydraulic field finite | pytest | Head and velocities contain no NaN/Inf |
| Intervention monotonicity | pytest | Intervention does not increase replacement burden |
| Physical hidden commitment | `physical_summary.csv` | Tests `Q_D(t0)=0` with positive future burden |
| Physical preservation | `physical_summary.csv` | Tests whether `K_P>0` survives explicit transport |
| Physical window | `physical_delay_frontier.csv` | Tests whether a finite `t_star` exists |
| Dose response | `physical_dose_response.csv` | Tests intervention magnitude dependence |
| Stress test | `physical_stress_tests.csv` | Tests demand/pumping perturbations |
| Salinity fields | PNG figures | Inspects spatial transport behavior |

A negative result is valid: the base physical benchmark detects hidden commitment but does not yield positive preservation amplification under the tested parameterization.

## Level 2B — Complete physical attack suite

| Priority | Test | Artifact | Scientific question |
|---:|---|---|---|
| 1 | Physical parameter-space search | `results/attack/tables/parameter_space.csv` | Does any tested physically admissible regime produce `K_P>0`? |
| 2 | Recharge vs pumping-reduction ablation | `mechanisms.csv` | Which mechanism contributes preservation? |
| 3 | Intervention magnitude sweep | `magnitude.csv` | Is there a prevention threshold or dose response? |
| 4 | Intervention timing sweep | `timing.csv` | Does a genuine closing window emerge? |
| 5 | Salinity-front analysis | `salinity_front.csv` | Does intervention delay saline-front migration? |
| 6 | Pumping/recharge regime sweep | `location.csv` | How does intervention effectiveness vary across forcing regimes? |
| 7 | Hydraulic parameter sweep | `hydraulic.csv` | Sensitivity to `K`, porosity and dispersion |
| 8 | Demand/head stress | `stress.csv` | Does hidden commitment survive stress? |
| 9 | Global sensitivity | `sensitivity.csv` | Which parameters control `V_D`, `K_D`, `K_P`? |
| 10 | Level-2 Monte Carlo | `monte_carlo.csv` | Frequency of hidden commitment and `K_P>0` |
| 11 | Kill tests | `kill_tests.csv` | Can the claimed phenomenon be deliberately destroyed? |
| 12 | Grid/time convergence | `convergence.csv` | Are results discretization artifacts? |
| 13 | Alternative physical formulation | `alternative.csv` | Does conclusion depend on hard threshold mapping? |
| 14 | Delay-intervention frontier | `frontier.csv` | Does a tested `V_I^*(tau)` and finite `t_star` exist? |

Additional boundary outputs:
- `positive_kp_cases.csv` — all tested `K_P>0` cases;
- `kp_boundary_near.csv` — tested cases closest to `K_P=0`;
- `attack_summary.csv` — aggregate results;
- `ATTACK_REPORT.md` — generated interpretation.

The suite is explicitly non-goal-directed: positive, negative and boundary cases are retained.
