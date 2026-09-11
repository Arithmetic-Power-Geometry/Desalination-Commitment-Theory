# Desalination Commitment Theory

A reproducible computational framework for detecting **hidden future desalination commitment**, quantifying **preservation amplification**, and identifying **closing intervention windows** in water systems.

The artifact is location-neutral and built for software-only theoretical/computational validation.

## Core questions

1. Can present desalination requirement be zero while unavoidable future desalination is positive?
2. Can preventive intervention eliminate or reduce that commitment?
3. Can intervention preserve additional native freshwater beyond direct volumetric substitution?
4. Is there a latest time after which full prevention is no longer feasible?
5. How much extra preventive intervention is required to compensate for delay?

## Core quantities

- Present desalination requirement: `Q_D(t0)`
- Cumulative unavoidable future desalination: `V_D^U`
- Desalination avoidance multiplier: `K_D`
- Preservation multiplier: `K_P`
- Latest full-prevention time: `t_star`
- Cost of delay: `C_D`
- Minimum preventive intervention: `V_I_star`
- Timing-volume frontier: `V_I_star(tau)`

## Two-level validation architecture

### Level 1 — Controlled nonlinear benchmark
Tests the mathematical construct in a compact nonlinear dynamical system.

Current controlled benchmark output:

- `Q_D(t0) = 0`
- positive cumulative future replacement burden
- zero cumulative replacement under immediate maximum intervention
- `K_D = 3.243718`
- `K_P = 2.543718`
- `t_star = 2.5` model-time units
- minimum constant intervention rate for full prevention = `0.039`

### Level 2A — 2-D groundwater/salinity physical benchmark
Tests whether the same construct survives explicit spatial dynamics using:

- 2-D aquifer grid
- hydraulic-head field
- Darcy-like groundwater flow
- pumping depression
- recharge mound
- advection-dispersion salinity transport
- potable salinity threshold
- demand growth
- recharge and pumping-reduction interventions

The base Level 2 benchmark gives a scientifically important **mixed result**:

- hidden commitment survives (`Q_D(t0)=0` with positive future replacement burden)
- baseline cumulative future replacement = `0.532194`
- immediate tested intervention does not reduce that burden in the current physical parameterization
- `K_D = 0.0`
- `K_P = -0.7` for the stated direct fraction
- no finite `t_star` is found under the tested intervention

This negative preservation result is intentionally retained. It is a falsification outcome, not tuned away.

## Level 2B — Complete physical attack suite

The repository now executes the full location-neutral software attack requested for the physical layer. The tested suite includes:

1. physical parameter-space search for the preservation-amplification region,
2. recharge-only / pumping-reduction-only / combined mechanism ablation,
3. intervention-magnitude sweep,
4. intervention-timing sweep,
5. salinity-front migration analysis,
6. pumping/recharge regime sweep,
7. hydraulic parameter sweep,
8. demand/head stress tests,
9. global sensitivity analysis,
10. Level-2 Monte Carlo uncertainty,
11. kill tests,
12. grid/time convergence,
13. alternative physical formulation,
14. delay-intervention full-prevention frontier.

The attack retains **all** tested regimes rather than selecting parameter sets merely because they support the desired conclusion.

### Current complete Level-2 attack result

- Parameter sets tested: `64`
- Hidden commitment present in parameter-space grid: `100%`
- `K_P > 0` cases in tested grid: `0`
- Fraction with `K_P > 0`: `0.0`
- Finite `t_star` found in the tested delay-intervention frontier: **no**
- Full-prevention delay points found: `0`
- Monte Carlo samples: `40`
- Monte Carlo hidden-commitment fraction: `97.5%`
- Monte Carlo `K_P > 0` fraction: `0.0`

Therefore the current physical evidence supports **hidden commitment as the robust component**, while preservation amplification and a finite full-prevention window are not supported by the present physical benchmark family.

This is a valid falsification result and is kept explicitly in the artifact.

## Software validation stack

- reduced-model theorem checks
- controlled nonlinear simulation
- physically motivated 2-D groundwater/salinity simulation
- baseline vs intervention counterfactuals
- delayed-intervention experiments
- dose-response sweeps
- preservation decomposition
- multi-source/shared-resource simulation
- physical parameter-space mapping
- global sensitivity and uncertainty
- stress and kill tests
- grid/time convergence
- alternative physical formulation
- delay-intervention frontier search
- reproducible figures and CSV tables
- automated tests and GitHub Actions

## Reproduce

```bash
python -m pip install -r requirements.txt
bash reproduce.sh
```

The full workflow runs tests, Level 1 experiments, Level 2 base physical validation, the complete Level-2 attack suite, artifact validation, and final print.

## Main generated outputs

### Level 1
- `results/tables/summary.csv`
- `results/tables/delay_frontier.csv`
- `results/tables/dose_response.csv`
- `results/tables/uncertainty.csv`
- `results/figures/commitment_trajectories.png`
- `results/figures/delay_frontier.png`
- `results/figures/dose_response.png`
- `results/REPORT.md`

### Level 2 base physical benchmark
- `results/physical/tables/physical_summary.csv`
- `results/physical/tables/physical_delay_frontier.csv`
- `results/physical/tables/physical_dose_response.csv`
- `results/physical/tables/physical_stress_tests.csv`
- `results/physical/figures/physical_commitment_trajectories.png`
- `results/physical/figures/physical_delay_frontier.png`
- `results/physical/figures/baseline_final_salinity.png`
- `results/physical/figures/intervention_final_salinity.png`
- `results/physical/PHYSICAL_REPORT.md`

### Level 2 complete attack
- `results/attack/tables/attack_summary.csv`
- `results/attack/tables/parameter_space.csv`
- `results/attack/tables/positive_kp_cases.csv`
- `results/attack/tables/kp_boundary_near.csv`
- `results/attack/tables/mechanisms.csv`
- `results/attack/tables/magnitude.csv`
- `results/attack/tables/timing.csv`
- `results/attack/tables/frontier.csv`
- `results/attack/tables/salinity_front.csv`
- `results/attack/tables/location.csv`
- `results/attack/tables/hydraulic.csv`
- `results/attack/tables/stress.csv`
- `results/attack/tables/sensitivity.csv`
- `results/attack/tables/monte_carlo.csv`
- `results/attack/tables/kill_tests.csv`
- `results/attack/tables/convergence.csv`
- `results/attack/tables/alternative.csv`
- `results/attack/figures/kp_distribution.png`
- `results/attack/figures/kp_regime_map.png`
- `results/attack/figures/magnitude_response.png`
- `results/attack/figures/timing_sweep.png`
- `results/attack/figures/salinity_front.png`
- `results/attack/figures/convergence.png`
- `results/attack/figures/global_sensitivity.png`
- `results/attack/ATTACK_REPORT.md`

## Scientific caution

This artifact is a computational testbed. Numerical outputs are generated from explicit model assumptions and are **not empirical measurements of any named location**. "Unavoidable" means unavoidable only under the stated model, constraints, admissible intervention set, and planning horizon.

The Level 2 model is physically motivated but is not a calibrated field model. Its role is to test whether the proposed commitment/preservation/window construct survives explicit spatial flow and salinity-transport assumptions.

A negative result is a valid scientific result and is never overwritten by goal-directed parameter tuning.

## License

Apache License 2.0.

Copyright (C) 2026 Mohammad Amir Khusru Akhtar.
