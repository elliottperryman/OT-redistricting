"""
Algorithms for solving redistricting by optimal transport
"""

## Standard imports
import numpy as np
import numba as nb # compile sinkhorn for speed
from shapely.geometry import Point

from State import State
from District import District
from misc import rand_guess

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
        if np.linalg.norm(u_-u) + np.linalg.norm(v_-v) < 1e-14 and i > 50:
            break
        u = u_
        v = v_
    return np.diag(u) @ K @ np.diag(v)

def _sinkhorn(C, a, b, u, v, MAX_ITER):
    ϵ = 1e-3
    for i in range(10):
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


def _solve_discrete(df, K, centers):
    """
    solve the discrete optimal transport problem
        * df is the dataframe with cols 'pop' and 'geometry'
        * state_geometry is obvious
        * K is number of centers
        * centers are the optional centers
    returns:
        * the sinkhorn results, the agglomerated result, the approximated cost 
    """
    centroids = df['geometry'].centroid
 
    # calculate cost matrix
    C = np.array([centroids.distance(p) for p in centers]).T
    C /= np.max(C)
    # fill in densities
    a, b = df['pop'].values, np.ones(K)/K
    # solve sinkhorn
    res = sinkhorn(C, a, b)
    # agglomerate result (approximating each as binary allocation!) 
    df2 = df.copy()
    # if more than 1% goes to another district, put it in the "split" pile
    split = (res.T/res.sum(1)).T.max(1)<0.99
    dist = res.argmax(1)
    dist[split] = -1
    df2['district'] = dist
    df2 = df2.dissolve(by='district', aggfunc='sum')

    centers = []
    for i in range(K):
        x, y = centroids[dist==i].x, centroids[dist==i].y
        pop = df['pop'].values[dist==i]
        mean_x, mean_y = np.mean(x*pop)/np.sum(pop), np.mean(y*pop)/np.sum(pop)
        centers.append(Point([mean_x, mean_y]))
    return res, df2, cost(res, C), centers

# def lloyd_alg(state_num,K,lvl='tract'):
#     block_df, tract_df, county_df, state = load_pop_df(state_num)
#     if lvl=='block':
#         df = block_df
#     elif lvl=='tract':
#         df = tract_df
#     elif lvl=='county':
#         df = county_df
#     sinkhorn_res, df_res, cost_res, centers = [], [], [], []
#     for i in range(10):
#         if i == 0:
#             a, b, c, d = solve_discrete(df, state, K)
#         else:
#             a, b, c, d = solve_discrete(df, state, K, df_res[-1]['geometry'].centroid.values)
#         if np.isnan(a).any():
#             raise RuntimeError('nan values in sinkhorn method. results not trustworthy')
#         sinkhorn_res.append(a)
#         df_res.append(b)
#         cost_res.append(c)
#         centers.append(d)
#     return sinkhorn_res, df_res, cost_res, centers

def solve_discrete(state : State, K, lvl='tract', centers = None):
    if lvl=='block':
        df = state.block_df
    elif lvl=='tract':
        df = state.tract_df
    elif lvl=='county':
        df = state.county_df
    if centers is None:
        centers = [rand_guess(state.state_geometry) for i in range(K)]

    res, df2, cost_val, centers = _solve_discrete(df, K, centers)

    district = District(state, res, df2, K, cost_val, centers)
    return district