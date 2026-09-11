from dct.model import ModelParams, simulate, cumulative_desalination
from dct.control import constant_after
from dct.metrics import avoidance_multiplier, preservation_multiplier

def test_baseline_nonnegative():
    p=ModelParams()
    s=simulate(p, constant_after(p.horizon+1,0))
    assert s["qd"].min() >= 0
    assert cumulative_desalination(s) >= 0

def test_intervention_not_worse():
    p=ModelParams()
    b=simulate(p, constant_after(p.horizon+1,0))
    i=simulate(p, constant_after(0,p.intervention_cap))
    assert cumulative_desalination(i) <= cumulative_desalination(b) + 1e-10

def test_multiplier_identity():
    p=ModelParams()
    b=simulate(p, constant_after(p.horizon+1,0))
    i=simulate(p, constant_after(0,p.intervention_cap))
    kd=avoidance_multiplier(b,i)
    kp=preservation_multiplier(b,i,p.direct_fraction)
    assert abs(kd - (p.direct_fraction + kp)) < 1e-12
