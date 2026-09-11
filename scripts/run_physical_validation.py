from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from dct.physics.aquifer2d import Aquifer2DParams, simulate_physical, integrate
from dct.physics.metrics2d import latest_full_prevention_time_physical

ROOT=Path(__file__).resolve().parents[1]
TAB=ROOT/'results'/'physical'/'tables'
FIG=ROOT/'results'/'physical'/'figures'
TAB.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True)

p=Aquifer2DParams()
base=simulate_physical(p,None,0.0,0.0,store_snapshots=True)
now=simulate_physical(p,0.0,1.0,0.018,store_snapshots=True)

v0=integrate(base['qd'],base['t'])
vi=integrate(now['qd'],now['t'])
vint=integrate(now['u'],now['t'])
kd=(v0-vi)/vint if vint>0 else np.nan
eta=0.70
kp=kd-eta if np.isfinite(kd) else np.nan
tstar,frontier=latest_full_prevention_time_physical(p,1.0,0.018,tol=1e-5)

summary=pd.DataFrame([{
    'Q_D_t0':base['qd'][0],
    'V_D_baseline':v0,
    'V_D_immediate':vi,
    'V_I_immediate':vint,
    'hidden_commitment':bool(base['qd'][0] <= 1e-12 and v0 > 1e-8),
    'K_D':kd,'eta':eta,'K_P':kp,
    't_star':np.nan if tstar is None else tstar,
    'baseline_final_usable_fraction':base['usable_fraction'][-1],
    'intervention_final_usable_fraction':now['usable_fraction'][-1],
    'baseline_final_mean_salinity':base['mean_salinity'][-1],
    'intervention_final_mean_salinity':now['mean_salinity'][-1],
}])
summary.to_csv(TAB/'physical_summary.csv',index=False)

front=pd.DataFrame(frontier,columns=['delay','V_D'])
front.to_csv(TAB/'physical_delay_frontier.csv',index=False)

rows=[]
for f in np.linspace(0,1.2,7):
    s=simulate_physical(p,0.0,float(f),0.018*min(f,1.0))
    vd=integrate(s['qd'],s['t']); vintf=integrate(s['u'],s['t'])
    kdf=np.nan if vintf<=0 else (v0-vd)/vintf
    rows.append({'intervention_fraction':f,'V_D':vd,'V_I':vintf,'K_D':kdf,'K_P':np.nan if not np.isfinite(kdf) else kdf-eta})
pd.DataFrame(rows).to_csv(TAB/'physical_dose_response.csv',index=False)

stress=[]
for dg in [0.003,0.010]:
    for pump in [0.045,0.070]:
        pp=Aquifer2DParams(demand_growth=dg,base_pumping=pump)
        b=simulate_physical(pp,None,0,0); i=simulate_physical(pp,0,1.0,0.018)
        vb,vi2=integrate(b['qd'],b['t']),integrate(i['qd'],i['t'])
        vin=integrate(i['u'],i['t']); kd2=np.nan if vin<=0 else (vb-vi2)/vin
        stress.append({'demand_growth':dg,'base_pumping':pump,'V_D_base':vb,'V_D_intervention':vi2,
                       'K_D':kd2,'K_P':np.nan if not np.isfinite(kd2) else kd2-eta,
                       'hidden_commitment':bool(b['qd'][0]<=1e-12 and vb>1e-8)})
pd.DataFrame(stress).to_csv(TAB/'physical_stress_tests.csv',index=False)

plt.figure(figsize=(8,5)); plt.plot(base['t'],base['qd'],label='baseline'); plt.plot(now['t'],now['qd'],label='immediate intervention')
for d in [2,5,10]:
    s=simulate_physical(p,d,1.0,0.018); plt.plot(s['t'],s['qd'],label=f'delay={d}')
plt.xlabel('Time'); plt.ylabel('Replacement requirement'); plt.title('Physical-model commitment trajectories'); plt.legend(); plt.tight_layout(); plt.savefig(FIG/'physical_commitment_trajectories.png',dpi=220); plt.close()

plt.figure(figsize=(8,5)); plt.plot(front['delay'],front['V_D']); plt.xlabel('Intervention delay'); plt.ylabel('Cumulative replacement requirement'); plt.title('Physical-model delay frontier'); plt.tight_layout(); plt.savefig(FIG/'physical_delay_frontier.png',dpi=220); plt.close()

for name,sim in [('baseline',base),('intervention',now)]:
    end_t=sorted(sim['snapshots'])[-1]; arr=sim['snapshots'][end_t]
    plt.figure(figsize=(9,3.2)); plt.imshow(arr,origin='lower',aspect='auto'); plt.colorbar(label='Salinity'); plt.xlabel('Cross-shore grid'); plt.ylabel('Alongshore grid'); plt.title(f'{name.capitalize()} final salinity field'); plt.tight_layout(); plt.savefig(FIG/f'{name}_final_salinity.png',dpi=220); plt.close()

report=f'''# Level 2 Physical Validation Report

This layer uses a location-neutral 2-D aquifer grid with hydraulic-head-driven Darcy-like flow, pumping/recharge perturbations, advection-dispersion salinity transport, a potable salinity threshold, and demand growth.

## Headline computational outputs

- Q_D(t0): {summary.Q_D_t0.iloc[0]:.6f}
- Baseline cumulative replacement: {v0:.6f}
- Immediate-intervention cumulative replacement: {vi:.6f}
- Hidden commitment detected: {bool(summary.hidden_commitment.iloc[0])}
- K_D: {kd:.6f}
- K_P (eta={eta:.2f}): {kp:.6f}
- Latest full-prevention time t*: {tstar}
- Baseline final usable fraction: {base['usable_fraction'][-1]:.6f}
- Intervention final usable fraction: {now['usable_fraction'][-1]:.6f}

## Interpretation

These are software-generated outputs from a generic physical benchmark, not empirical observations. The current benchmark retains hidden commitment but does not produce positive preservation amplification or a finite full-prevention time under the tested intervention. This negative result is retained as a falsification outcome rather than tuned away.
'''
(ROOT/'results'/'physical'/'PHYSICAL_REPORT.md').write_text(report)
print(summary.to_string(index=False))
print('Generated physical validation outputs.')
