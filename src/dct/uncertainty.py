from dataclasses import replace
import numpy as np
from .model import simulate
from .control import constant_after
from .metrics import hidden_commitment, avoidance_multiplier, preservation_multiplier

def monte_carlo(base_params, n=500, seed=7, intervention_rate=None):
    rng = np.random.default_rng(seed)
    rate = intervention_rate if intervention_rate is not None else base_params.intervention_cap
    rows = []
    for _ in range(n):
        p = replace(
            base_params,
            degradation_rate=max(0.001, rng.normal(base_params.degradation_rate, 0.008)),
            recovery_rate=max(0.05, rng.normal(base_params.recovery_rate, 0.05)),
            nonlinearity=max(0.0, rng.normal(base_params.nonlinearity, 0.025)),
            freshwater_sensitivity=max(0.1, rng.normal(base_params.freshwater_sensitivity, 0.08)),
            demand_growth=max(0.0, rng.normal(base_params.demand_growth, 0.0025)),
            x0=max(0.0, rng.normal(base_params.x0, 0.025)),
        )
        b = simulate(p, constant_after(p.horizon + 1, 0))
        i = simulate(p, constant_after(0, rate))
        kd = avoidance_multiplier(b, i)
        kp = preservation_multiplier(b, i, p.direct_fraction)
        rows.append((hidden_commitment(b), kd, kp))
    return np.array(rows, dtype=object)
