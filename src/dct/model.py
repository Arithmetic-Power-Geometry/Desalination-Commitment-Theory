from dataclasses import dataclass
from typing import Callable
import numpy as np

@dataclass(frozen=True)
class ModelParams:
    horizon: float = 30.0
    dt: float = 0.05
    x0: float = 0.20
    degradation_rate: float = 0.055
    recovery_rate: float = 0.42
    nonlinearity: float = 0.10
    freshwater_base: float = 1.25
    freshwater_sensitivity: float = 0.95
    demand0: float = 1.0
    demand_growth: float = 0.006
    direct_fraction: float = 0.70
    intervention_cap: float = 0.20

def demand(t: float, p: ModelParams) -> float:
    return p.demand0 * np.exp(p.demand_growth * t)

def native_supply(x: float, p: ModelParams) -> float:
    return max(0.0, p.freshwater_base - p.freshwater_sensitivity * x)

def degradation_rhs(x: float, u: float, p: ModelParams) -> float:
    u_eff = np.clip(u, 0.0, p.intervention_cap)
    return p.degradation_rate * x + p.nonlinearity * x*x - p.recovery_rate * u_eff

def simulate(p: ModelParams, control: Callable[[float, float], float]):
    n = int(round(p.horizon / p.dt)) + 1
    t = np.linspace(0.0, p.horizon, n)
    x = np.zeros(n)
    qd = np.zeros(n)
    u = np.zeros(n)
    x[0] = p.x0
    for k in range(n):
        u[k] = np.clip(control(float(t[k]), float(x[k])), 0.0, p.intervention_cap)
        qf = native_supply(float(x[k]), p)
        qd[k] = max(0.0, demand(float(t[k]), p) - qf)
        if k < n - 1:
            dx = degradation_rhs(float(x[k]), float(u[k]), p)
            x[k+1] = max(0.0, x[k] + p.dt * dx)
    return {"t": t, "x": x, "qd": qd, "u": u}

def trapz(y, x):
    return float(np.trapezoid(y, x))

def cumulative_desalination(sim):
    return trapz(sim["qd"], sim["t"])

def cumulative_intervention(sim):
    return trapz(sim["u"], sim["t"])
