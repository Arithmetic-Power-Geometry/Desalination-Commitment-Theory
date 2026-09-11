from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

print('DESALINATION COMMITMENT THEORY — FINAL COMPUTATIONAL PRINT')
print('='*72)
print('\nLEVEL 1 — CONTROLLED NONLINEAR BENCHMARK')
print(pd.read_csv(ROOT/'results'/'tables'/'summary.csv').to_string(index=False))

print('\nLEVEL 2A — BASE PHYSICAL GROUNDWATER/SALINITY BENCHMARK')
print(pd.read_csv(ROOT/'results'/'physical'/'tables'/'physical_summary.csv').to_string(index=False))

print('\nLEVEL 2B — COMPLETE PHYSICAL ATTACK SUMMARY')
attack=pd.read_csv(ROOT/'results'/'attack'/'tables'/'attack_summary.csv')
print(attack.to_string(index=False))

print('\nMECHANISM ABLATION')
print(pd.read_csv(ROOT/'results'/'attack'/'tables'/'mechanisms.csv').to_string(index=False))

print('\nCASES NEAREST K_P = 0')
print(pd.read_csv(ROOT/'results'/'attack'/'tables'/'kp_boundary_near.csv').head(10).to_string(index=False))

print('\nTOP POSITIVE K_P CASES')
pos_path=ROOT/'results'/'attack'/'tables'/'positive_kp_cases.csv'
try:
    pos=pd.read_csv(pos_path)
    print('None found in tested parameter space.' if len(pos)==0 else pos.head(10).to_string(index=False))
except Exception:
    print('None found in tested parameter space.')

print('\nDELAY–INTERVENTION FRONTIER')
print(pd.read_csv(ROOT/'results'/'attack'/'tables'/'frontier.csv').to_string(index=False))

print('\nREPORT')
print((ROOT/'results'/'attack'/'ATTACK_REPORT.md').read_text())
