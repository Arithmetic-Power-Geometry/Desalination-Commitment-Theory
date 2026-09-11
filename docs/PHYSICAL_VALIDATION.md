# Physical Validation Layer

The project now uses two validation levels.

## Level 1 — controlled nonlinear benchmark

Purpose: verify the commitment/preservation/window construct in a compact mathematical model.

## Level 2 — 2-D groundwater/salinity benchmark

Purpose: test whether the same construct survives explicit spatial physics rather than only a one-state degradation equation.

The Level 2 benchmark includes:

- a two-dimensional aquifer grid,
- hydraulic-head gradients,
- Darcy-like groundwater flow,
- pumping-induced head depression,
- recharge-induced head support,
- advection-dispersion salinity transport,
- a potable salinity threshold,
- demand growth,
- preventive recharge and pumping-reduction interventions.

## Required physical tests

1. `Q_D(t0)=0` at the initial state.
2. Positive cumulative future replacement burden under the baseline.
3. Compare immediate intervention with the same physical baseline.
4. Compute `K_D` from counterfactual cumulative replacement volumes.
5. Compute `K_P=K_D-eta` under the stated accounting boundary.
6. Search for a finite latest full-prevention time `t_star`.
7. Run dose-response and delay-frontier sweeps.
8. Run stress tests over demand growth and pumping.
9. Retain negative outcomes rather than tuning parameters to force the theory.

## Current physical result

The present generic benchmark supports hidden commitment but does not support preservation amplification under the tested intervention parameterization:

- `Q_D(t0)=0`
- baseline cumulative future replacement > 0
- immediate intervention does not reduce cumulative replacement in this configuration
- `K_D=0`
- `K_P<0`
- no finite `t_star` is detected

This is a valid falsification result. It shows that the full theoretical phenomenon does not follow automatically from any groundwater/salinity model; stronger physical conditions or alternative intervention structures must be identified and tested explicitly.

## Scientific boundary

The Level 2 model is physically motivated but is not a calibrated field model. Its outputs must not be interpreted as empirical measurements.
