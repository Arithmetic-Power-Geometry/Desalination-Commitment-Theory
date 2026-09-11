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
attack1=ROOT/'results'/'attack'/'tables'/'attack_summary.csv'
attack2=ROOT/'results'/'physical'/'attack_tables'/'preservation_regime_summary.csv'
if attack1.exists():
    print(pd.read_csv(attack1).to_string(index=False))
elif attack2.exists():
    print(pd.read_csv(attack2).to_string(index=False))

print('\nLEVEL 3 — HIDDEN COMMITMENT FORMAL NOVELTY ATTACK')
nov=ROOT/'results'/'novelty'/'tables'/'novelty_attack_summary.csv'
if nov.exists():
    print(pd.read_csv(nov).to_string(index=False))
report=ROOT/'results'/'novelty'/'NOVELTY_ATTACK_REPORT.md'
if report.exists():
    print('\n'+report.read_text())
