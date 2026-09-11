from dct.physics.aquifer2d import Aquifer2DParams
from dct.optimization.policy_search import PolicyBounds,admissible_policy_search,unavoidable_future_volume

def test_policy_grid_runs():
    p=Aquifer2DParams(nx=20,ny=6,years=1,dt=0.2); b=PolicyBounds(recharge_fractions=(0,1),pumping_reductions=(0,0.01),start_delays=(0,))
    df,best=admissible_policy_search(p,b); assert len(df)==4; assert best['V_D']>=0

def test_unavoidable_summary_fields():
    p=Aquifer2DParams(nx=20,ny=6,years=1,dt=0.2); b=PolicyBounds(recharge_fractions=(0,1),pumping_reductions=(0,0.01),start_delays=(0,))
    s,_=unavoidable_future_volume(p,b); assert 'V_D_U_grid' in s; assert 'hidden_commitment_grid' in s
