from dataclasses import dataclass
import itertools, numpy as np, pandas as pd
from dct.physics.aquifer2d import Aquifer2DParams, simulate_physical, integrate

@dataclass(frozen=True)
class PolicyBounds:
    recharge_fractions: tuple=(0.0,0.5,1.0,1.5,2.0)
    pumping_reductions: tuple=(0.0,0.009,0.018,0.027,0.036)
    start_delays: tuple=(0.0,2.0,5.0,10.0)
    max_recharge_fraction: float=2.0
    max_pumping_reduction: float=0.036

def evaluate_policy(p, recharge_fraction, pumping_reduction, delay):
    if recharge_fraction==0.0 and pumping_reduction==0.0:
        s=simulate_physical(p,None,0.0,0.0)
    else:
        s=simulate_physical(p,float(delay),float(recharge_fraction),float(pumping_reduction))
    return integrate(s["qd"],s["t"])

def admissible_policy_search(p=None,bounds=None):
    p=p or Aquifer2DParams(); bounds=bounds or PolicyBounds(); rows=[]
    for rf,pr,d in itertools.product(bounds.recharge_fractions,bounds.pumping_reductions,bounds.start_delays):
        if rf>bounds.max_recharge_fraction or pr>bounds.max_pumping_reduction: continue
        rows.append(dict(recharge_fraction=rf,pumping_reduction=pr,delay=d,V_D=evaluate_policy(p,rf,pr,d)))
    df=pd.DataFrame(rows); best=df.loc[df["V_D"].idxmin()].copy()
    return df,best

def unavoidable_future_volume(p=None,bounds=None,tol=1e-10):
    p=p or Aquifer2DParams(); df,best=admissible_policy_search(p,bounds)
    q0=simulate_physical(p,None,0.0,0.0)["qd"][0]; vu=float(best["V_D"])
    return {"Q_D_t0":float(q0),"V_D_U_grid":vu,"hidden_commitment_grid":bool(q0<=tol and vu>tol),"full_prevention_found":bool(vu<=tol),"best_recharge_fraction":float(best["recharge_fraction"]),"best_pumping_reduction":float(best["pumping_reduction"]),"best_delay":float(best["delay"]),"n_policies":len(df)},df
