from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dct.model import ModelParams, simulate, cumulative_desalination, cumulative_intervention
from dct.control import constant_after, latest_full_prevention_time, minimum_rate_for_full_prevention
from dct.metrics import present_requirement, hidden_commitment, avoidance_multiplier, preservation_multiplier, cost_of_delay
from dct.uncertainty import monte_carlo
from dct.multisource import unavoidable_replacement

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "results" / "tables"
FIG = ROOT / "results" / "figures"
TAB.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

p = ModelParams()
baseline = simulate(p, constant_after(p.horizon + 1, 0.0))
immediate = simulate(p, constant_after(0.0, p.intervention_cap))
v0 = cumulative_desalination(baseline)
vi = cumulative_desalination(immediate)
kd = avoidance_multiplier(baseline, immediate)
kp = preservation_multiplier(baseline, immediate, p.direct_fraction)
tstar = latest_full_prevention_time(p, p.intervention_cap)
min_rate = minimum_rate_for_full_prevention(p, delay=0.0)

summary = pd.DataFrame([{
    "Q_D_t0": present_requirement(baseline),
    "V_D_baseline": v0,
    "V_D_immediate": vi,
    "V_I_immediate": cumulative_intervention(immediate),
    "hidden_commitment": hidden_commitment(baseline),
    "K_D": kd,
    "K_P": kp,
    "t_star": np.nan if tstar is None else tstar,
    "minimum_rate_full_prevention": np.nan if min_rate is None else min_rate,
}])
summary.to_csv(TAB/"summary.csv", index=False)

delays = np.linspace(0, p.horizon, 61)
delay_rows = []
for d in delays:
    s = simulate(p, constant_after(float(d), p.intervention_cap))
    delay_rows.append({
        "delay": d,
        "V_D": cumulative_desalination(s),
        "cost_of_delay": cost_of_delay(immediate, s),
        "V_I": cumulative_intervention(s),
    })
delay_df = pd.DataFrame(delay_rows)
delay_df.to_csv(TAB/"delay_frontier.csv", index=False)

rates = np.linspace(0.0, p.intervention_cap, 51)
dose_rows = []
for r in rates:
    s = simulate(p, constant_after(0, float(r)))
    vint = cumulative_intervention(s)
    av = v0 - cumulative_desalination(s)
    kd_r = np.nan if vint <= 0 else av/vint
    kp_r = np.nan if vint <= 0 else kd_r - p.direct_fraction
    dose_rows.append({"rate": r, "V_I": vint, "avoided_desalination": av, "K_D": kd_r, "K_P": kp_r})
dose_df = pd.DataFrame(dose_rows)
dose_df.to_csv(TAB/"dose_response.csv", index=False)

mc = monte_carlo(p, n=500, seed=7)
unc = pd.DataFrame({
    "hidden_commitment": mc[:,0].astype(bool),
    "K_D": mc[:,1].astype(float),
    "K_P": mc[:,2].astype(float),
})
unc.to_csv(TAB/"uncertainty.csv", index=False)

multi = pd.DataFrame([{
    "demand": 1.0,
    "source_capacities": "[0.42,0.38,0.35]",
    "required_interventions": "[0.08,0.07,0.06]",
    "shared_capacity": 0.12,
    "unavoidable_replacement": unavoidable_replacement(
        1.0,[0.42,0.38,0.35],[0.08,0.07,0.06],0.12,[0.12,0.12,0.12]
    )
}])
multi.to_csv(TAB/"multisource.csv", index=False)

plt.figure(figsize=(8,5))
plt.plot(baseline["t"], baseline["qd"], label="baseline")
plt.plot(immediate["t"], immediate["qd"], label="immediate intervention")
for d in [5,10,15]:
    s = simulate(p, constant_after(d, p.intervention_cap))
    plt.plot(s["t"], s["qd"], label=f"delay={d:g}")
plt.xlabel("Time")
plt.ylabel("Desalination requirement")
plt.title("Hidden commitment and delayed intervention")
plt.legend()
plt.tight_layout()
plt.savefig(FIG/"commitment_trajectories.png", dpi=220)
plt.close()

plt.figure(figsize=(8,5))
plt.plot(delay_df["delay"], delay_df["V_D"])
plt.xlabel("Intervention delay")
plt.ylabel("Cumulative desalination")
plt.title("Delay–commitment frontier")
plt.tight_layout()
plt.savefig(FIG/"delay_frontier.png", dpi=220)
plt.close()

valid = dose_df.dropna()
plt.figure(figsize=(8,5))
plt.plot(valid["V_I"], valid["K_D"], label="K_D")
plt.plot(valid["V_I"], valid["K_P"], label="K_P")
plt.axhline(0, linewidth=1)
plt.xlabel("Cumulative intervention")
plt.ylabel("Multiplier")
plt.title("Dose response of avoidance and preservation")
plt.legend()
plt.tight_layout()
plt.savefig(FIG/"dose_response.png", dpi=220)
plt.close()

report = f"""# Computational Report

This report is generated automatically by `scripts/run_experiments.py`.

## Headline outputs

- Present desalination requirement, Q_D(t0): {summary.Q_D_t0.iloc[0]:.6f}
- Baseline cumulative desalination: {v0:.6f}
- Immediate-intervention cumulative desalination: {vi:.6f}
- Hidden commitment detected: {bool(summary.hidden_commitment.iloc[0])}
- K_D: {kd:.6f}
- K_P: {kp:.6f}
- Latest full-prevention time t*: {tstar}
- Minimum constant intervention rate for full prevention: {min_rate}

## Uncertainty summary

- Monte Carlo samples: {len(unc)}
- Fraction with hidden commitment: {unc.hidden_commitment.mean():.3f}
- Fraction with K_P > 0: {(unc.K_P > 0).mean():.3f}
- Median K_D: {unc.K_D.median():.6f}
- Median K_P: {unc.K_P.median():.6f}

## Interpretation

These values come from a generic computational test system. They are not empirical measurements of a named water system. The purpose is to test internal consistency, falsifiability, robustness, and reproducibility of the proposed quantities.
"""
(ROOT/"results"/"REPORT.md").write_text(report)

print(summary.to_string(index=False))
print()
print("Generated:")
for path in sorted((ROOT/"results").rglob("*")):
    if path.is_file():
        print(path.relative_to(ROOT))
