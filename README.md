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

## Software validation stack

- reduced-model theorem checks
- dynamic physical proxy simulation
- baseline vs intervention counterfactuals
- delayed intervention experiments
- dose-response sweeps
- preservation decomposition
- multi-source/shared-resource simulation
- sensitivity analysis
- uncertainty analysis
- stress tests
- ablation tests
- falsification / kill tests
- reproducible figures and CSV tables
- automated tests and GitHub Actions

## Reproduce

```bash
python -m pip install -r requirements.txt
bash reproduce.sh
```

Generated outputs are written to:

- `results/tables/summary.csv`
- `results/tables/delay_frontier.csv`
- `results/tables/dose_response.csv`
- `results/tables/uncertainty.csv`
- `results/figures/commitment_trajectories.png`
- `results/figures/delay_frontier.png`
- `results/figures/dose_response.png`
- `results/REPORT.md`

## Current synthetic benchmark result

The included generic benchmark currently yields:

- `Q_D(t0) = 0`
- positive baseline cumulative future desalination
- zero cumulative desalination under immediate maximum intervention
- `K_D = 3.243718`
- `K_P = 2.543718`
- `t_star = 2.5` model-time units
- minimum constant intervention rate for full prevention = `0.039`

These numbers are generated from an explicit synthetic model and are **not empirical measurements of any named location**.

## Scientific caution

This artifact is a computational testbed. Numerical outputs are generated from explicit model assumptions and are **not empirical measurements of any named location**. "Unavoidable" always means unavoidable under the stated model, constraints, admissible intervention set, and planning horizon.

## License

Apache License 2.0.

Copyright (C) 2026 Mohammad Amir Khusru Akhtar.
