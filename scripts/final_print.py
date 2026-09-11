from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
print('DESALINATION COMMITMENT THEORY — FINAL COMPUTATIONAL SUMMARY')
print('\nLEVEL 1 — CONTROLLED NONLINEAR BENCHMARK')
print(pd.read_csv(ROOT/'results'/'tables'/'summary.csv').to_string(index=False))
print('\nLEVEL 2 — 2-D GROUNDWATER/SALINITY PHYSICAL BENCHMARK')
print(pd.read_csv(ROOT/'results'/'physical'/'tables'/'physical_summary.csv').to_string(index=False))
print('\nLEVEL 1 REPORT\n')
print((ROOT/'results'/'REPORT.md').read_text())
print('\nLEVEL 2 REPORT\n')
print((ROOT/'results'/'physical'/'PHYSICAL_REPORT.md').read_text())
