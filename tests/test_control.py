from dct.model import ModelParams
from dct.control import latest_full_prevention_time, minimum_rate_for_full_prevention

def test_searches_execute():
    p=ModelParams()
    t=latest_full_prevention_time(p,p.intervention_cap,grid=31)
    r=minimum_rate_for_full_prevention(p,grid=31)
    assert t is None or 0 <= t <= p.horizon
    assert r is None or 0 <= r <= p.intervention_cap
