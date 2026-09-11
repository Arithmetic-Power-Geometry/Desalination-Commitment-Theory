from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt
from dct.physics.aquifer2d import Aquifer2DParams
from dct.optimization.policy_search import PolicyBounds, unavoidable_future_volume
ROOT=Path(__file__).resolve().parents[1]; TAB=ROOT/'results/optimization/tables'; FIG=ROOT/'results/optimization/figures'; TAB.mkdir(parents=True,exist_ok=True); FIG.mkdir(parents=True,exist_ok=True)
p=Aquifer2DParams(); bounds=PolicyBounds(); summary,policies=unavoidable_future_volume(p,bounds)
pd.DataFrame([summary]).to_csv(TAB/'optimization_summary.csv',index=False); policies.sort_values('V_D').to_csv(TAB/'policy_grid.csv',index=False)
best=policies.groupby('delay',as_index=False)['V_D'].min(); best.to_csv(TAB/'best_by_delay.csv',index=False)
plt.figure(figsize=(8,5)); plt.plot(best['delay'],best['V_D'],marker='o'); plt.xlabel('Intervention delay'); plt.ylabel('Minimum cumulative replacement over tested controls'); plt.title('Best admissible tested policy by delay'); plt.tight_layout(); plt.savefig(FIG/'best_policy_by_delay.png',dpi=220); plt.close()
report=f'''# Admissible-Policy Optimization Report\n\nPolicies evaluated: {summary["n_policies"]}\n\nQ_D(t0): {summary["Q_D_t0"]:.9f}\n\nMinimum cumulative future replacement over tested grid: {summary["V_D_U_grid"]:.9f}\n\nFull prevention found: {summary["full_prevention_found"]}\n\nHidden commitment under tested grid: {summary["hidden_commitment_grid"]}\n\nBest recharge fraction: {summary["best_recharge_fraction"]}\n\nBest pumping reduction: {summary["best_pumping_reduction"]}\n\nBest delay: {summary["best_delay"]}\n\n## Interpretation\n`V_D_U_grid` is a finite-policy-grid upper bound on the true continuous-control infimum, not proof of a universal infimum. The defensible claim is that no policy in the explicitly tested admissible grid eliminated future replacement burden.\n'''
(ROOT/'results/optimization/OPTIMIZATION_REPORT.md').write_text(report)
print(pd.DataFrame([summary]).to_string(index=False))
