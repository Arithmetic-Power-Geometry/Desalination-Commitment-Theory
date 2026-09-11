import numpy as np
from .model import cumulative_desalination, cumulative_intervention

def present_requirement(sim, tol=1e-12):
    return float(sim["qd"][0])

def committed_volume(sim):
    return cumulative_desalination(sim)

def avoidance_multiplier(base_sim, intervention_sim):
    v0 = cumulative_desalination(base_sim)
    vi = cumulative_desalination(intervention_sim)
    vint = cumulative_intervention(intervention_sim)
    if vint <= 0:
        return np.nan
    return (v0 - vi) / vint

def preservation_multiplier(base_sim, intervention_sim, eta):
    kd = avoidance_multiplier(base_sim, intervention_sim)
    return kd - eta

def cost_of_delay(immediate_sim, delayed_sim):
    return cumulative_desalination(delayed_sim) - cumulative_desalination(immediate_sim)

def hidden_commitment(base_sim, tol=1e-10):
    return present_requirement(base_sim) <= tol and committed_volume(base_sim) > tol
