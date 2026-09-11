import numpy as np
from dct.physics.aquifer2d import Aquifer2DParams
from dct.physics.attack_suite import evaluate, salinity_front, alternative_formulation, convergence_tests

def test_evaluate_finite_core():
    p=Aquifer2DParams(nx=24,ny=8,years=1,dt=0.1)
    m=evaluate(p,0,1.0,0.01)
    assert np.isfinite(m["V_D_base"])
    assert np.isfinite(m["V_D_intervention"])

def test_salinity_front_bounds():
    p=Aquifer2DParams(nx=20,ny=6)
    C=np.zeros((6,20))
    C[:,10:]=2.0
    x=salinity_front(C,1.0,p.length)
    assert 0 <= x <= p.length

def test_alternative_formulation_runs():
    p=Aquifer2DParams(nx=24,ny=8,years=1,dt=0.1)
    df=alternative_formulation(p)
    assert len(df)==1
    assert "K_D" in df.columns

def test_convergence_table():
    df=convergence_tests()
    assert len(df)>=3
    assert df["V_D_base"].notna().all()
