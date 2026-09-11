import numpy as np
from .aquifer2d import integrate, simulate_physical

def physical_summary(p, delay=None, intervention_fraction=1.0, pumping_reduction=0.0):
    base = simulate_physical(p, None, 0.0, 0.0)
    inter = simulate_physical(p, delay, intervention_fraction, pumping_reduction)
    v0 = integrate(base['qd'], base['t'])
    vi = integrate(inter['qd'], inter['t'])
    vint = integrate(inter['u'], inter['t'])
    kd = np.nan if vint <= 0 else (v0-vi)/vint
    return base,inter,v0,vi,vint,kd

def latest_full_prevention_time_physical(p, intervention_fraction=1.0, pumping_reduction=0.0, tol=1e-6, delay_grid=None):
    if delay_grid is None:
        delay_grid = np.linspace(0,p.years,31)
    best=None
    vals=[]
    for d in delay_grid:
        s=simulate_physical(p,float(d),intervention_fraction,pumping_reduction)
        vd=integrate(s['qd'],s['t'])
        vals.append((float(d),vd))
        if vd <= tol:
            best=float(d)
    return best,vals
