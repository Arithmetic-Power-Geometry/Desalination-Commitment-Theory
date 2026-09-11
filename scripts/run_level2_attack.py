from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from dct.physics.aquifer2d import Aquifer2DParams
from dct.physics.attack_suite import *

ROOT=Path(__file__).resolve().parents[1]
TAB=ROOT/"results"/"attack"/"tables"
FIG=ROOT/"results"/"attack"/"figures"
TAB.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True)
p=Aquifer2DParams()

outputs={}
outputs["parameter_space"]=parameter_space_search(p)
outputs["mechanisms"]=mechanism_ablation(p)
outputs["magnitude"]=magnitude_sweep(p)
outputs["timing"]=timing_sweep(p)
outputs["frontier"]=delay_intervention_frontier(p)
outputs["salinity_front"]=salinity_front_analysis(p)
outputs["location"]=location_sweep(p)
outputs["hydraulic"]=hydraulic_sweep(p)
outputs["stress"]=demand_drought_stress(p)
samples,sensitivity=global_sensitivity(p,n=40,seed=11)
outputs["sensitivity_samples"]=samples
outputs["sensitivity"]=sensitivity
outputs["monte_carlo"]=monte_carlo_level2(p,n=40,seed=17)
outputs["kill_tests"]=kill_tests(p)
outputs["convergence"]=convergence_tests()
outputs["alternative"]=alternative_formulation(p)

for name,df in outputs.items():
    df.to_csv(TAB/f"{name}.csv",index=False)

ps=outputs["parameter_space"]
positive=ps[np.isfinite(ps["K_P"]) & (ps["K_P"]>0)]
frac_positive=float((np.isfinite(ps["K_P"]) & (ps["K_P"]>0)).mean())
frac_hidden=float(ps["hidden_commitment"].mean())

ps2=ps[np.isfinite(ps["K_P"])].copy()
ps2["abs_KP"]=ps2["K_P"].abs()
boundary=ps2.sort_values("abs_KP").head(25)
boundary.to_csv(TAB/"kp_boundary_near.csv",index=False)

front=outputs["frontier"]
feas=front[front["full_prevention_found"]]
tstar=float(feas["delay"].max()) if len(feas) else np.nan

plt.figure(figsize=(8,5))
vals=ps[np.isfinite(ps["K_P"])]
plt.hist(vals["K_P"],bins=30)
plt.axvline(0,linewidth=1)
plt.xlabel("K_P")
plt.ylabel("Count")
plt.title("Physical parameter-space preservation multiplier")
plt.tight_layout(); plt.savefig(FIG/"kp_distribution.png",dpi=220); plt.close()

plt.figure(figsize=(8,5))
plt.scatter(vals["recharge"],vals["pumping"],c=vals["K_P"])
plt.colorbar(label="K_P")
plt.xlabel("Recharge strength")
plt.ylabel("Pumping")
plt.title("Preservation regime map")
plt.tight_layout(); plt.savefig(FIG/"kp_regime_map.png",dpi=220); plt.close()

mag=outputs["magnitude"]
plt.figure(figsize=(8,5))
plt.plot(mag["fraction"],mag["V_D_intervention"],marker="o")
plt.xlabel("Intervention fraction")
plt.ylabel("Cumulative replacement")
plt.title("Intervention magnitude response")
plt.tight_layout(); plt.savefig(FIG/"magnitude_response.png",dpi=220); plt.close()

tim=outputs["timing"]
plt.figure(figsize=(8,5))
plt.plot(tim["delay"],tim["V_D_intervention"])
plt.xlabel("Delay")
plt.ylabel("Cumulative replacement")
plt.title("Timing sweep")
plt.tight_layout(); plt.savefig(FIG/"timing_sweep.png",dpi=220); plt.close()

fr=outputs["salinity_front"]
for scen,g in fr.groupby("scenario"):
    plt.plot(g["time"],g["front_x"],marker="o",label=scen)
plt.xlabel("Time"); plt.ylabel("Salinity front position")
plt.title("Salinity-front migration"); plt.legend()
plt.tight_layout(); plt.savefig(FIG/"salinity_front.png",dpi=220); plt.close()

cv=outputs["convergence"]
plt.figure(figsize=(8,5))
plt.plot(range(len(cv)),cv["V_D_base"],marker="o",label="baseline")
plt.plot(range(len(cv)),cv["V_D_intervention"],marker="o",label="intervention")
plt.xticks(range(len(cv)),[f'{int(r["nx"])}x{int(r["ny"])},dt={r["dt"]}' for _,r in cv.iterrows()],rotation=25)
plt.ylabel("Cumulative replacement"); plt.title("Grid/time convergence")
plt.legend(); plt.tight_layout(); plt.savefig(FIG/"convergence.png",dpi=220); plt.close()

top=sensitivity.sort_values("abs_spearman",ascending=False).head(15)
plt.figure(figsize=(9,5))
labels=(top["target"]+":"+top["feature"]).tolist()
plt.barh(range(len(top)),top["abs_spearman"])
plt.yticks(range(len(top)),labels)
plt.xlabel("|Spearman rho|"); plt.title("Global sensitivity ranking")
plt.tight_layout(); plt.savefig(FIG/"global_sensitivity.png",dpi=220); plt.close()

mc=outputs["monte_carlo"]
mc_valid=mc[np.isfinite(mc["K_P"])]
mc_kp_pos=float((mc_valid["K_P"]>0).mean()) if len(mc_valid) else np.nan
mc_hidden=float(mc["hidden_commitment"].mean())

summary=pd.DataFrame([{
    "parameter_sets":len(ps),
    "fraction_hidden_commitment":frac_hidden,
    "fraction_KP_positive":frac_positive,
    "positive_KP_cases":len(positive),
    "boundary_cases_saved":len(boundary),
    "finite_t_star":tstar,
    "monte_carlo_n":len(mc),
    "mc_fraction_hidden":mc_hidden,
    "mc_fraction_KP_positive":mc_kp_pos,
    "full_prevention_delay_points":len(feas),
}])
summary.to_csv(TAB/"attack_summary.csv",index=False)

best = positive.sort_values("K_P",ascending=False).head(10) if len(positive) else ps.head(0).copy()
best.to_csv(TAB/"positive_kp_cases.csv",index=False)

mc_kp_pos_display = f"{mc_kp_pos:.4f}" if np.isfinite(mc_kp_pos) else "NaN"
report=f"""# Complete Level-2 Physical Attack Report

This report summarizes a broad, location-neutral computational attack on the physical benchmark.

## Coverage

1. Physical parameter-space search
2. Recharge-only vs pumping-reduction-only vs combined ablation
3. Intervention-magnitude sweep
4. Intervention-timing sweep
5. Salinity-front analysis
6. Pumping/recharge regime sweep
7. Hydraulic parameter sweep
8. Demand/head stress
9. Global sensitivity
10. Level-2 Monte Carlo uncertainty
11. Kill tests
12. Grid/time convergence
13. Alternative physical formulation
14. Delay-intervention full-prevention frontier

## Main aggregate results

- Parameter sets tested: {len(ps)}
- Fraction with hidden commitment: {frac_hidden:.4f}
- Cases with K_P > 0: {len(positive)}
- Fraction with K_P > 0: {frac_positive:.4f}
- Finite t* from tested full-prevention frontier: {tstar}
- Monte Carlo samples: {len(mc)}
- Monte Carlo hidden-commitment fraction: {mc_hidden:.4f}
- Monte Carlo K_P > 0 fraction: {mc_kp_pos_display}

## Scientific rule

No parameter set is selected merely because it produces a desired conclusion. The full tested parameter space is retained.
Positive, negative, and boundary-near cases are all exported. Numerical outputs are generic model results rather than
empirical measurements.

## Boundary analysis

`kp_boundary_near.csv` contains the parameter combinations closest to K_P = 0. This is the primary dataset for studying
the transition between ordinary substitution and preservation amplification.

## Full-prevention frontier

`frontier.csv` reports the minimum tested intervention fraction required for zero cumulative replacement at each delay.
If no tested intervention achieves zero replacement, the corresponding entry remains missing rather than being forced.
"""
(ROOT/"results"/"attack"/"ATTACK_REPORT.md").write_text(report)
print(summary.to_string(index=False))
print("Level-2 attack suite complete.")
