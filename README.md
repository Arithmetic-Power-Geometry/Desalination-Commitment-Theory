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

### Level 2 — 2-D groundwater/salinity physical benchmark
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

The present Level 2 benchmark gives a scientifically important **mixed result**:

- hidden commitment survives (`Q_D(t0)=0` with positive future replacement burden)
- baseline cumulative future replacement = `0.532194`
- immediate tested intervention does not reduce that burden in the current physical parameterization
- `K_D = 0.0`
- `K_P = -0.7` for the stated direct fraction
- no finite `t_star` is found under the tested intervention

This negative preservation result is intentionally retained. It is a falsification outcome, not tuned away. It means the full amplification/window claim is supported by the Level 1 controlled benchmark but is **not yet supported by the current Level 2 physical benchmark**.

## Software validation stack

- reduced-model theorem checks
- controlled nonlinear simulation
- physically motivated 2-D groundwater/salinity simulation
- baseline vs intervention counterfactuals
- delayed-intervention experiments
- dose-response sweeps
- preservation decomposition
- multi-source/shared-resource simulation
- sensitivity and stress analysis
- uncertainty analysis
- model ablation and kill tests
- reproducible figures and CSV tables
- automated tests and GitHub Actions

## Reproduce

```bash
python -m pip install -r requirements.txt
bash reproduce.sh
```

The full workflow runs tests, Level 1 experiments, Level 2 physical validation, artifact validation, and final print.

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

### Level 2
- `results/physical/tables/physical_summary.csv`
- `results/physical/tables/physical_delay_frontier.csv`
- `results/physical/tables/physical_dose_response.csv`
- `results/physical/tables/physical_stress_tests.csv`
- `results/physical/figures/physical_commitment_trajectories.png`
- `results/physical/figures/physical_delay_frontier.png`
- `results/physical/figures/baseline_final_salinity.png`
- `results/physical/figures/intervention_final_salinity.png`
- `results/physical/PHYSICAL_REPORT.md`

## Scientific caution

This artifact is a computational testbed. Numerical outputs are generated from explicit model assumptions and are **not empirical measurements of any named location**. "Unavoidable" means unavoidable only under the stated model, constraints, admissible intervention set, and planning horizon.

The Level 2 model is physically motivated but is not a calibrated field model. Its role is to test whether the proposed commitment/preservation/window construct survives explicit spatial flow and salinity-transport assumptions.

## License

Apache License 2.0.

Copyright (C) 2026 Mohammad Amir Khusru Akhtar.
