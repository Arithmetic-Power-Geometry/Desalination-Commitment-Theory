from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
summary = pd.read_csv(ROOT/'results'/'tables'/'summary.csv')
print('DESALINATION COMMITMENT THEORY — FINAL COMPUTATIONAL SUMMARY')
print(summary.to_string(index=False))
print()
print((ROOT/'results'/'REPORT.md').read_text())
