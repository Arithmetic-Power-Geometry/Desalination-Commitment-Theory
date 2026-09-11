from .model import simulate, cumulative_desalination

def constant_after(delay, rate):
    def policy(t, x):
        return rate if t >= delay else 0.0
    return policy

def pulse_after(delay, rate, duration):
    def policy(t, x):
        return rate if (delay <= t <= delay + duration) else 0.0
    return policy

def latest_full_prevention_time(params, rate, tol=1e-5, grid=121):
    best = None
    for j in range(grid):
        delay = params.horizon * j / (grid - 1)
        sim = simulate(params, constant_after(delay, rate))
        if cumulative_desalination(sim) <= tol:
            best = delay
    return best

def minimum_rate_for_full_prevention(params, delay=0.0, tol=1e-5, grid=201):
    best = None
    for j in range(grid):
        rate = params.intervention_cap * j / (grid - 1)
        sim = simulate(params, constant_after(delay, rate))
        if cumulative_desalination(sim) <= tol:
            best = rate
            break
    return best
