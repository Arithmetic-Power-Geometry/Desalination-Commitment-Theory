from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Aquifer2DParams:
    nx: int = 48
    ny: int = 16
    length: float = 8000.0
    width: float = 2400.0
    dt: float = 0.10
    years: float = 20.0
    hydraulic_conductivity: float = 12.0
    porosity: float = 0.30
    longitudinal_dispersion: float = 35.0
    transverse_dispersion: float = 7.0
    molecular_diffusion: float = 0.05
    freshwater_head: float = 1.4
    sea_head: float = 0.0
    sea_salinity: float = 35.0
    freshwater_salinity: float = 0.3
    potable_threshold: float = 1.0
    base_pumping: float = 0.055
    recharge_strength: float = 0.035
    demand0: float = 0.75
    demand_growth: float = 0.007
    supply_scale: float = 1.0

def _grid(p):
    dx = p.length/(p.nx-1)
    dy = p.width/(p.ny-1)
    x = np.linspace(0,p.length,p.nx)
    y = np.linspace(0,p.width,p.ny)
    return x,y,dx,dy

def initial_salinity(p):
    x, y, dx, dy = _grid(p)
    X = np.tile(x[None,:], (p.ny,1))
    center = 0.78*p.length
    width = 0.045*p.length
    f = 1.0/(1.0+np.exp(-(X-center)/width))
    C = p.freshwater_salinity + (p.sea_salinity-p.freshwater_salinity)*f
    C[:,0] = p.freshwater_salinity
    C[:,-1] = p.sea_salinity
    return C

def head_field(p, pumping=0.0, recharge=0.0):
    x, y, dx, dy = _grid(p)
    H = p.freshwater_head + (p.sea_head-p.freshwater_head)*(x[None,:]/p.length)
    H = np.repeat(H,p.ny,axis=0)
    X,Y = np.meshgrid(x,y)
    px, py = 0.62*p.length, 0.5*p.width
    sigma = 0.14*p.length
    cone = np.exp(-((X-px)**2 + 0.6*(Y-py)**2)/(2*sigma**2))
    mound = np.exp(-((X-0.48*p.length)**2 + 0.7*(Y-py)**2)/(2*(0.16*p.length)**2))
    H = H - 4.0*pumping*cone + 3.5*recharge*mound
    H[:,0] = p.freshwater_head
    H[:,-1] = p.sea_head
    return H

def darcy_velocity(H,p):
    x,y,dx,dy = _grid(p)
    dHdy,dHdx = np.gradient(H,dy,dx)
    vx = -(p.hydraulic_conductivity/p.porosity)*dHdx
    vy = -(p.hydraulic_conductivity/p.porosity)*dHdy
    return vx,vy

def transport_step(C,vx,vy,p):
    x,y,dx,dy = _grid(p)
    dCdx_b=(C-np.roll(C,1,axis=1))/dx
    dCdx_f=(np.roll(C,-1,axis=1)-C)/dx
    dCdy_b=(C-np.roll(C,1,axis=0))/dy
    dCdy_f=(np.roll(C,-1,axis=0)-C)/dy
    advx=np.where(vx>=0,vx*dCdx_b,vx*dCdx_f)
    advy=np.where(vy>=0,vy*dCdy_b,vy*dCdy_f)
    d2x=(np.roll(C,-1,axis=1)-2*C+np.roll(C,1,axis=1))/(dx*dx)
    d2y=(np.roll(C,-1,axis=0)-2*C+np.roll(C,1,axis=0))/(dy*dy)
    speed=np.sqrt(vx*vx+vy*vy)
    Dx=p.molecular_diffusion+p.longitudinal_dispersion*speed
    Dy=p.molecular_diffusion+p.transverse_dispersion*speed
    out=C+p.dt*(-advx-advy + Dx*d2x + Dy*d2y)
    out=np.clip(out,p.freshwater_salinity,p.sea_salinity)
    out[:,0]=p.freshwater_salinity
    out[:,-1]=p.sea_salinity
    out[0,:]=out[1,:]
    out[-1,:]=out[-2,:]
    return out

def demand(t,p):
    return p.demand0*np.exp(p.demand_growth*t)

def usable_fraction(C,p):
    inland = C[:,:int(0.78*p.nx)]
    return float(np.mean(inland <= p.potable_threshold))

def simulate_physical(p, intervention_delay=None, intervention_fraction=0.0, pumping_reduction=0.0, store_snapshots=False):
    C=initial_salinity(p)
    n=int(round(p.years/p.dt))+1
    times=np.linspace(0,p.years,n)
    qd=np.zeros(n); u=np.zeros(n); frac=np.zeros(n); meanC=np.zeros(n)
    snapshots={}
    for k,t in enumerate(times):
        active = intervention_delay is not None and t >= intervention_delay
        rech = p.recharge_strength*intervention_fraction if active else 0.0
        pump = max(0.0,p.base_pumping - (pumping_reduction if active else 0.0))
        H=head_field(p,pumping=pump,recharge=rech)
        vx,vy=darcy_velocity(H,p)
        frac[k]=usable_fraction(C,p)
        native = p.supply_scale*frac[k]
        qd[k]=max(0.0,demand(t,p)-native)
        u[k]=rech
        meanC[k]=float(C[:,:int(0.78*p.nx)].mean())
        if store_snapshots and k in {0,n//3,2*n//3,n-1}:
            snapshots[float(t)] = C.copy()
        if k<n-1:
            C=transport_step(C,0.18*vx,0.18*vy,p)
    return {"t":times,"qd":qd,"u":u,"usable_fraction":frac,"mean_salinity":meanC,"snapshots":snapshots}

def integrate(y,t):
    return float(np.trapezoid(y,t))
