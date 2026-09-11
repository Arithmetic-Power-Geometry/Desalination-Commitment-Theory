from pathlib import Path
import pandas as pd
from dct.novelty.hidden_commitment import separability_witnesses, overlap_matrix

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "results" / "novelty" / "tables"
TAB.mkdir(parents=True, exist_ok=True)

sep = separability_witnesses()
ov = overlap_matrix()
sep.to_csv(TAB / "separability_witnesses.csv", index=False)
ov.to_csv(TAB / "framework_overlap_matrix.csv", index=False)

checks = {
    "HDC_without_present_viability_loss": bool(((sep.hidden_commitment) & (~sep.present_viability_loss)).any()),
    "tipping_not_equivalent_to_HDC": bool(((sep.tipping_point) & (~sep.hidden_commitment)).any()),
    "real_options_not_equivalent_to_HDC": bool(((sep.real_option_signal) & (~sep.hidden_commitment)).any()),
    "robust_failure_not_equivalent_to_HDC": bool(((sep.robust_control_failure) & (~sep.hidden_commitment)).any()),
    "visible_deficit_excluded": bool(((sep.present_requirement > 0) & (~sep.hidden_commitment)).any()),
}
summary = pd.DataFrame([checks])
summary["all_separability_checks_pass"] = summary.all(axis=1)
summary.to_csv(TAB / "novelty_attack_summary.csv", index=False)

report = """# Hidden Desalination Commitment — Formal Novelty Attack

## Object under attack
`Q_D(t0)=0` and `V_D^U(t0,T)>0`.

## What this software can test
It can test whether this predicate is definitionally identical to simplified representatives of established decision objects.

## What this software cannot prove
It cannot certify publication novelty or prove absence of prior art.

## Formal separability result
The included witness cases establish that, at the predicate level:
- HDC can hold while present feasibility remains intact.
- adaptation tipping can occur without HDC.
- positive real-option value can occur without HDC.
- robust-control failure can occur without HDC.
- visible present deficit is excluded by definition.

## Remaining vulnerability
Viability theory and backward reachability are general enough to encode future failure sets. HDC may therefore be interpretable as a domain-specific slice or annotation of those frameworks. The potentially distinctive part is the conjunction of:
1. zero present replacement requirement,
2. positive minimum unavoidable future replacement volume,
3. explicit burden magnitude rather than only binary failure membership.

## Defensible status
FORMALLY SEPARABLE FROM THE SIMPLIFIED COMPARISON SIGNALS; NOT NOVELTY-CERTIFIED.
"""
(ROOT / "results" / "novelty" / "NOVELTY_ATTACK_REPORT.md").write_text(report)
print(summary.to_string(index=False))
