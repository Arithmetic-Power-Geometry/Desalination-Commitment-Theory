# Software Test Matrix

| Test | Output | Pass / interpretation |
|---|---|---|
| Present requirement | Q_D(t0) | Establish whether present desalination is zero |
| Baseline future | V_D_baseline | Positive value establishes future replacement burden |
| Immediate intervention | V_D_immediate | Must not exceed baseline |
| Hidden commitment | boolean | Q_D(t0)=0 and V_D_baseline>0 |
| Avoidance multiplier | K_D | Counterfactual avoided desalination per intervention volume |
| Preservation multiplier | K_P | Positive value indicates benefit beyond direct substitution |
| Delay sweep | delay_frontier.csv | Tests closing prevention window |
| Dose sweep | dose_response.csv | Tests nonlinear response |
| Uncertainty | uncertainty.csv | Tests robustness |
| Multi-source | multisource.csv | Tests shared-resource commitment |
| Kill: no degradation | pytest | Commitment must vanish |
| Kill: no recovery | pytest | Preservation effect must vanish |
| Reproduction | reproduce.sh | Tests full artifact deterministically |
