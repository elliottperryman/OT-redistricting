"""
Algorithms for solving redistricting by optimal transport
"""

## Standard imports
import numpy as np
import numba as nb # compile sinkhorn for speed
from shapely.geometry import Point
from geopandas import GeoSeries

from State import State
from District import District
from misc import rand_guess, sample_rand

"""
    The next section is a little confusing. sinkhorn runs the
    Sinkhorn algorithm for cost C, entropy epsilon, densities
    a and b, and for MAX_ITER iterations at most

   base _sinkhorn is numba compiled, so it only contains deterministic
        functions. u_v_gen generates normal vectors as inputs
        and sinkhorn proper wraps it up
    cost calculates the cost of the transport plan
    compile runs the functions so that numba creates an efficient
    function without overwriting the names C, a, and b
"""
def u_v_gen(C):
    return np.random.normal(size=C.shape[0]), np.random.normal(size=C.shape[1])
@nb.njit
def base_sinkhorn(C, ϵ, a, b, u, v, MAX_ITER):
    K = np.exp(-C/ϵ)
    for i in range(MAX_ITER):
        u_ = a / (K @ v)
        v_ = b / (u_ @ K)
        if np.linalg.norm(u_-u) + np.linalg.norm(v_-v) < 1e-14 and i > 100:
            break
        u = u_
        v = v_
    return np.diag(u) @ K @ np.diag(v)

def _sinkhorn(C, a, b, u, v, MAX_ITER):
    ϵ = 1e-5
    for i in range(30):
        res = base_sinkhorn(C, ϵ, a, b, u, v, MAX_ITER=MAX_ITER)
        if np.isnan(res).any():
            print('ϵ of '+str(ϵ)+' too small. Doubling..')
            ϵ *= 2
        else:
            print('ϵ of '+str(ϵ)+' worked')
            return res
    else:
        raise RuntimeError('Still returning nan from sinkhorn')


def sinkhorn(C, a, b, MAX_ITER=10_000):
    return _sinkhorn(C, a, b, *u_v_gen(C), MAX_ITER)
def cost(C,res):
    return np.sum(C*res)
def compile():
    C = np.random.random((4,2))
    a, b = np.ones(4)/2, np.ones(2)
    cost(C,sinkhorn(C, a, b))
compile()


def solve_discrete(state: State, centers=None) -> District:
    """
    solve the discrete optimal transport problem
        * df is the dataframe with cols 'pop' and 'geometry'
        * state_geometry is obvious
        * K is number of centers
        * centers are the optional centers
    returns:
        * the sinkhorn results, the agglomerated result, the approximated cost 
    """

    if centers is None:
        centers = sample_rand(state.df, state.num_districts)
    K = state.num_districts
    centroids = state.df.centroid # .to_crs(crs=3857).centroid.to_crs(4269)
    # calculate cost matrix
    # C = np.array([centroids.to_crs(3857).distance(p) for p in centers]).T
    C = np.array([centroids.distance(p) for p in centers]).T
    C /= np.max(C)
    # fill in densities
    a, b = state.df['pop'].values, np.ones(K)/K
    # solve sinkhorn
    res = sinkhorn(C, a, b)
    # calculate centroids weighted by population or not!
    x, y = centroids.x.values, centroids.y.values
    # normFactor = (df['pop'].values.reshape(-1,1)*res).sum(0)
    # center_x = np.sum((x * df['pop'].values).reshape(-1,1) * res / normFactor, 0)
    # center_y = np.sum((y * df['pop'].values).reshape(-1,1) * res / normFactor, 0)
    center_x = np.array([np.mean(x[res.argmax(1)==i]) for i in range(K)])
    center_y = np.array([np.mean(y[res.argmax(1)==i]) for i in range(K)])
    centers = GeoSeries([Point([a,b]) for a,b in zip(center_x,center_y)])
    # centers.set_crs(4269)
    district = District(state, res, centers)
    return district
