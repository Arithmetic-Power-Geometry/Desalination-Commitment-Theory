from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
summary = pd.read_csv(ROOT/'results'/'tables'/'summary.csv')
required = ['Q_D_t0','V_D_baseline','V_D_immediate','K_D','K_P','hidden_commitment']
missing = [c for c in required if c not in summary.columns]
if missing:
    raise SystemExit(f'Missing columns: {missing}')
if not (ROOT/'results'/'figures'/'commitment_trajectories.png').exists():
    raise SystemExit('Missing commitment figure')
if not (ROOT/'results'/'REPORT.md').exists():
    raise SystemExit('Missing report')
print('Artifact validation passed.')
phys = ROOT/'results'/'physical'/'tables'/'physical_summary.csv'
if not phys.exists():
    raise SystemExit('Missing physical summary')
p = pd.read_csv(phys)
for c in ['Q_D_t0','V_D_baseline','V_D_immediate','K_D','K_P','hidden_commitment']:
    if c not in p.columns:
        raise SystemExit(f'Missing physical column: {c}')
if not (ROOT/'results'/'physical'/'figures'/'physical_commitment_trajectories.png').exists():
    raise SystemExit('Missing physical commitment figure')
if not (ROOT/'results'/'physical'/'PHYSICAL_REPORT.md').exists():
    raise SystemExit('Missing physical report')
print('Physical validation artifact passed.')
