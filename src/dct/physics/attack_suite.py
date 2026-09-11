from dataclasses import replace
import numpy as np
import pandas as pd
from .aquifer2d import Aquifer2DParams, simulate_physical, integrate

ETA_DEFAULT = 0.70

def evaluate(p, delay=0.0, intervention_fraction=1.0, pumping_reduction=0.018, eta=ETA_DEFAULT):
    base = simulate_physical(p, None, 0.0, 0.0)
    inter = simulate_physical(p, delay, intervention_fraction, pumping_reduction)
    v0 = integrate(base["qd"], base["t"])
    vi = integrate(inter["qd"], inter["t"])
    vint = integrate(inter["u"], inter["t"])
    kd = np.nan if vint <= 0 else (v0 - vi) / vint
    kp = np.nan if not np.isfinite(kd) else kd - eta
    return {
        "Q_D_t0": float(base["qd"][0]),
        "V_D_base": v0,
        "V_D_intervention": vi,
        "V_I": vint,
        "K_D": kd,
        "K_P": kp,
        "hidden_commitment": bool(base["qd"][0] <= 1e-12 and v0 > 1e-8),
        "base_final_usable": float(base["usable_fraction"][-1]),
        "int_final_usable": float(inter["usable_fraction"][-1]),
        "base_mean_salinity": float(base["mean_salinity"][-1]),
        "int_mean_salinity": float(inter["mean_salinity"][-1]),
    }

def parameter_space_search(base=None):
    p0=base or Aquifer2DParams()
    rows=[]
    Ks=[6.0,20.0]
    por=[0.22,0.38]
    DL=[15.0,70.0]
    pumping=[0.035,0.075]
    recharge=[0.02,0.07]
    growth=[0.003,0.012]
    for K in Ks:
      for ph in por:
       for dl in DL:
        for q in pumping:
         for r in recharge:
          for g in growth:
            p=replace(p0,hydraulic_conductivity=K,porosity=ph,
                      longitudinal_dispersion=dl,transverse_dispersion=max(3.0,dl/5),
                      base_pumping=q,recharge_strength=r,demand_growth=g)
            m=evaluate(p,0.0,1.0,min(0.03,q*0.45))
            rows.append({"K":K,"porosity":ph,"D_L":dl,"pumping":q,"recharge":r,
                         "demand_growth":g,**m})
    return pd.DataFrame(rows)

def mechanism_ablation(p=None):
    p=p or Aquifer2DParams()
    specs=[
        ("recharge_only",1.0,0.0),
        ("pumping_reduction_only",0.0,0.018),
        ("combined",1.0,0.018),
        ("no_intervention",0.0,0.0),
    ]
    rows=[]
    for name,rf,pr in specs:
        m=evaluate(p,0.0,rf,pr)
        rows.append({"mechanism":name,**m})
    return pd.DataFrame(rows)

def magnitude_sweep(p=None):
    p=p or Aquifer2DParams()
    rows=[]
    for f in np.linspace(0.0,2.0,11):
        m=evaluate(p,0.0,float(f),0.018*min(f,1.5))
        rows.append({"fraction":float(f),**m})
    return pd.DataFrame(rows)

def timing_sweep(p=None, fraction=1.0, pumping_reduction=0.018):
    p=p or Aquifer2DParams()
    rows=[]
    for delay in np.linspace(0,p.years,11):
        m=evaluate(p,float(delay),fraction,pumping_reduction)
        rows.append({"delay":float(delay),**m})
    return pd.DataFrame(rows)

def delay_intervention_frontier(p=None, tol=1e-6):
    p=p or Aquifer2DParams()
    rows=[]
    for delay in np.linspace(0,p.years,11):
        best=np.nan
        best_v=np.nan
        for f in np.linspace(0.0,3.0,16):
            inter=simulate_physical(p,float(delay),float(f),0.018*min(float(f),2.0))
            vd=integrate(inter["qd"],inter["t"])
            if vd <= tol:
                best=float(f)
                best_v=integrate(inter["u"],inter["t"])
                break
        rows.append({"delay":float(delay),"min_fraction_full_prevention":best,
                     "V_I_star":best_v,"full_prevention_found":bool(np.isfinite(best))})
    return pd.DataFrame(rows)

def salinity_front(C, threshold, length):
    ny,nx=C.shape
    xs=np.linspace(0,length,nx)
    loc=[]
    for row in C:
        ids=np.where(row>=threshold)[0]
        loc.append(xs[ids[0]] if len(ids) else length)
    return float(np.mean(loc))

def salinity_front_analysis(p=None):
    p=p or Aquifer2DParams()
    rows=[]
    for delay in [None,0.0,2.0,5.0,10.0]:
        sim=simulate_physical(p,delay,0.0 if delay is None else 1.0,
                              0.0 if delay is None else 0.018,store_snapshots=True)
        for t,C in sim["snapshots"].items():
            rows.append({"scenario":"baseline" if delay is None else f"delay_{delay:g}",
                         "time":t,"front_x":salinity_front(C,p.potable_threshold,p.length)})
    return pd.DataFrame(rows)

def location_sweep(p=None):
    p=p or Aquifer2DParams()
    rows=[]
    for q in [0.03,0.045,0.06,0.075]:
        for r in [0.015,0.03,0.05,0.075]:
            pp=replace(p,base_pumping=q,recharge_strength=r)
            m=evaluate(pp,0,1.0,min(0.03,q*0.4))
            rows.append({"pumping_proxy":q,"recharge_proxy":r,**m})
    return pd.DataFrame(rows)

def hydraulic_sweep(p=None):
    p=p or Aquifer2DParams()
    rows=[]
    for K in [5,20,35]:
      for phi in [0.2,0.4]:
       for dl in [10,80]:
        pp=replace(p,hydraulic_conductivity=K,porosity=phi,
                   longitudinal_dispersion=dl,transverse_dispersion=max(2,dl/5))
        m=evaluate(pp,0,1.0,0.018)
        rows.append({"K":K,"porosity":phi,"D_L":dl,**m})
    return pd.DataFrame(rows)

def demand_drought_stress(p=None):
    p=p or Aquifer2DParams()
    rows=[]
    for dg in [0.0,0.01,0.02]:
      for head in [0.8,1.4,1.8]:
        pp=replace(p,demand_growth=dg,freshwater_head=head)
        m=evaluate(pp,0,1.0,0.018)
        rows.append({"demand_growth":dg,"freshwater_head":head,**m})
    return pd.DataFrame(rows)

def global_sensitivity(p=None, n=160, seed=11):
    p=p or Aquifer2DParams()
    rng=np.random.default_rng(seed)
    rows=[]
    for _ in range(n):
        pp=replace(
            p,
            hydraulic_conductivity=float(rng.uniform(5,30)),
            porosity=float(rng.uniform(0.2,0.4)),
            longitudinal_dispersion=float(rng.uniform(10,80)),
            transverse_dispersion=float(rng.uniform(2,20)),
            base_pumping=float(rng.uniform(0.03,0.08)),
            recharge_strength=float(rng.uniform(0.015,0.08)),
            demand_growth=float(rng.uniform(0.0,0.02)),
            freshwater_head=float(rng.uniform(0.8,1.8))
        )
        m=evaluate(pp,0,1.0,min(0.03,pp.base_pumping*0.4))
        rows.append({
            "K":pp.hydraulic_conductivity,"porosity":pp.porosity,
            "D_L":pp.longitudinal_dispersion,"D_T":pp.transverse_dispersion,
            "pumping":pp.base_pumping,"recharge":pp.recharge_strength,
            "demand_growth":pp.demand_growth,"freshwater_head":pp.freshwater_head,**m})
    df=pd.DataFrame(rows)
    target_cols=["V_D_base","K_D","K_P"]
    feature_cols=["K","porosity","D_L","D_T","pumping","recharge","demand_growth","freshwater_head"]
    cor=[]
    for target in target_cols:
        for feat in feature_cols:
            valid=df[[feat,target]].replace([np.inf,-np.inf],np.nan).dropna()
            rho=valid[feat].corr(valid[target],method="spearman") if len(valid)>2 else np.nan
            cor.append({"target":target,"feature":feat,"spearman":rho,"abs_spearman":abs(rho) if np.isfinite(rho) else np.nan})
    return df,pd.DataFrame(cor)

def monte_carlo_level2(p=None, n=120, seed=17):
    df,_=global_sensitivity(p,n=n,seed=seed)
    return df

def kill_tests(p=None):
    p=p or Aquifer2DParams()
    specs=[
        ("no_demand_growth",replace(p,demand_growth=0.0)),
        ("low_pumping",replace(p,base_pumping=0.01)),
        ("high_inland_head",replace(p,freshwater_head=2.5)),
        ("zero_recharge_effect",replace(p,recharge_strength=0.0)),
        ("low_dispersion",replace(p,longitudinal_dispersion=2.0,transverse_dispersion=1.0)),
    ]
    rows=[]
    for name,pp in specs:
        m=evaluate(pp,0,1.0,0.018)
        rows.append({"kill_case":name,**m})
    return pd.DataFrame(rows)

def convergence_tests():
    rows=[]
    settings=[
        (28,10,0.20),
        (36,12,0.15),
        (48,16,0.10),
        (60,20,0.08),
    ]
    for nx,ny,dt in settings:
        p=Aquifer2DParams(nx=nx,ny=ny,dt=dt,years=10)
        m=evaluate(p,0,1.0,0.018)
        rows.append({"nx":nx,"ny":ny,"dt":dt,**m})
    return pd.DataFrame(rows)

def alternative_formulation(p=None):
    p=p or Aquifer2DParams()
    base=simulate_physical(p,None,0,0)
    inter=simulate_physical(p,0,1.0,0.018)
    def smooth_volume(sim):
        sal=np.asarray(sim["mean_salinity"])
        penalty=1/(1+np.exp(-4*(sal-p.potable_threshold)))
        native=p.supply_scale*(1-penalty)
        dem=p.demand0*np.exp(p.demand_growth*np.asarray(sim["t"]))
        qd=np.maximum(0,dem-native)
        return integrate(qd,sim["t"])
    v0=smooth_volume(base); vi=smooth_volume(inter)
    vint=integrate(inter["u"],inter["t"])
    kd=np.nan if vint<=0 else (v0-vi)/vint
    kp=np.nan if not np.isfinite(kd) else kd-ETA_DEFAULT
    return pd.DataFrame([{"formulation":"smooth_salinity_penalty","V_D_base":v0,
                          "V_D_intervention":vi,"V_I":vint,"K_D":kd,"K_P":kp}])
