import numpy as np
from dct.physics.aquifer2d import Aquifer2DParams, initial_salinity, head_field, darcy_velocity, simulate_physical, integrate

def test_initial_boundaries():
    p=Aquifer2DParams(nx=30,ny=10,years=0.2,dt=0.02)
    C=initial_salinity(p)
    assert np.allclose(C[:,0],p.freshwater_salinity)
    assert np.allclose(C[:,-1],p.sea_salinity)

def test_head_and_velocity_finite():
    p=Aquifer2DParams(nx=30,ny=10,years=0.2,dt=0.02)
    H=head_field(p,pumping=p.base_pumping,recharge=0)
    vx,vy=darcy_velocity(H,p)
    assert np.isfinite(H).all() and np.isfinite(vx).all() and np.isfinite(vy).all()

def test_physical_intervention_not_worse():
    p=Aquifer2DParams(nx=40,ny=12,years=3,dt=0.05)
    b=simulate_physical(p,None,0,0)
    i=simulate_physical(p,0,1.0,0.018)
    assert integrate(i['qd'],i['t']) <= integrate(b['qd'],b['t']) + 1e-9
