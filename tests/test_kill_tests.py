from dataclasses import replace
from dct.model import ModelParams, simulate, cumulative_desalination
from dct.control import constant_after
from dct.metrics import preservation_multiplier

def test_no_degradation_kills_commitment():
    p=replace(ModelParams(), degradation_rate=0.0, nonlinearity=0.0, demand_growth=0.0, x0=0.0)
    b=simulate(p, constant_after(p.horizon+1,0))
    assert cumulative_desalination(b) == 0.0

def test_zero_recovery_removes_preservation_effect():
    p=replace(ModelParams(), recovery_rate=0.0)
    b=simulate(p, constant_after(p.horizon+1,0))
    i=simulate(p, constant_after(0,p.intervention_cap))
    kp=preservation_multiplier(b,i,p.direct_fraction)
    assert kp <= 0.0
