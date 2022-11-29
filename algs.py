"""
Algorithms for solving redistricting by optimal transport
"""

## Standard imports
import numpy as np
import numba as nb # compile sinkhorn for speed
import matplotlib.pyplot as plt
# geometry tools
import pandas as pd
import fiona
import shapely
import geopandas

def load_pop_df(state_num):
    """
    load_pop_df loads the data for state identified by integer state_num
    the output:
        * dataframe of ['block', 'pop', 'geometry']
        * dataframe of ['tract', 'pop', 'geometry']
        * dataframe of ['county', 'pop', 'geometry']
        * geometry of state (0 population areas excluded
    
    if there is a file not found error, try running get.sh to download data
        or check that the state number exists
    """
    try:
        df = geopandas.read_file('data/tl_2020_'+str(state_num).zfill(2)+'_tabblock20.shp')
    except Exception as err:
        raise FileNotFoundError('exception. probably state number does not exist')
       # raise err
    # only worry about regions with population
    df = df[df['POP20']>0]
    # count total people in region 
    total_people = df['POP20'].sum()
    # create template to grab features from
    df = geopandas.GeoDataFrame({
        'state': df['STATEFP20'].astype(int), 
        'county': df['COUNTYFP20'].astype(int),
        'tract': df['TRACTCE20'].astype(int), 
        'block': df['BLOCKCE20'].astype(int),
        'pop': df['POP20'].astype(float)/total_people, 
        'geometry': df['geometry'], 
        })
    # create hierarchy of structures
    agg = {
            'state':'first', 'county':'first', 
            'tract':'first', 'block':'first', 'pop':'sum'
    }
    block_df = df[['block', 'pop', 'geometry']]
    tract_df = df.dissolve(by='tract', aggfunc=agg)
    county_df = tract_df.dissolve(by='county', aggfunc=agg)
    state_df = county_df.dissolve(by='state', aggfunc=agg)

    tract_df = tract_df[['pop', 'geometry']]
    county_df = county_df[['pop', 'geometry']]
    state = state_df['geometry'].values[0]
    return block_df, tract_df, county_df, state


# def discrete(df):
#     df['geometry'] = df['geometry'].centroid # to_crs(3857).centroid.to_crs(epsg=4326)
#     return df

def rand_guess(state):
    """
    rand_guess puts a point randomly in the box surrounding the state
    """
    minx, miny, maxx, maxy = state.bounds
    LB, UB = np.array([minx, miny]), np.array([maxx, maxy])
    p = shapely.geometry.Point(*(np.random.random()*(UB-LB)+LB))
    return p

"""
    The next section is a little confusing. sinkhorn runs the
    Sinkhorn algorithm for cost C, entropy epsilon, densities
    a and b, and for MAX_ITER iterations at most

    _sinkhorn is numba compiled, so it only contains deterministic
        functions. u_v_gen generates normal vectors as inputs
        and sinkhorn proper wraps it up
    cost calculates the cost of the transport plan
    compile runs the functions so that numba creates an efficient
    function without overwriting the names C, a, and b
"""
def u_v_gen(C):
    return np.random.normal(size=C.shape[0]), np.random.normal(size=C.shape[1])
@nb.njit(cache=True)
def _sinkhorn(C, ϵ, a, b, u, v, MAX_ITER):
    K = np.exp(-C/ϵ)
    for i in range(MAX_ITER):
        u_ = a / (K @ v)
        v_ = b / (u_ @ K)
        if np.linalg.norm(u_-u) + np.linalg.norm(v_-v) < 1e-14 and i > 50:
            break
        u = u_
        v = v_
    return np.diag(u) @ K @ np.diag(v)
def sinkhorn(C, ϵ, a, b, MAX_ITER=10_000):
    return _sinkhorn(C, ϵ, a, b, *u_v_gen(C), MAX_ITER)
@nb.njit(cache=True)
def cost(C,res):
    return np.sum(C*res)
def compile():
    C = np.random.random((4,2))
    a, b = np.ones(4)/2, np.ones(2)
    cost(C,sinkhorn(C, 1e-2, a, b))
compile()

# you can 
# def plot(res, df, name):
#     df.plot(column=res.argmax(1), categorical=True)
#     plt.savefig(name)

def solve_discrete(df, state_geometry, K, centers=None):
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
    if centers is None:
        centers = [rand_guess(state_geometry) for i in range(K)]
    # calculate cost matrix
    C = np.array([centroids.distance(p) for p in centers]).T
    C /= np.max(C)
    # fill in densities
    a, b = df['pop'].values, np.ones(K)/K
    # solve sinkhorn
    res = sinkhorn(C, 1e-3, a, b)
    # agglomerate result (approximating each as binary allocation!) 
    df2 = df.copy()
    split = (res.T/res.sum(1)).T.max(1)<0.99
    dist = res.argmax(1)
    dist[split] = -1
    df2['district'] = dist
    df2 = df2.dissolve(by='district', aggfunc='sum')

    return res, df2, cost(res, C), centers

def lloyd_alg(state_num,K,lvl='tract'):
    block_df, tract_df, county_df, state = load_pop_df(state_num)
    if lvl=='block':
        df = block_df
    elif lvl=='tract':
        df = tract_df
    elif lvl=='county':
        df = county_df
    sinkhorn_res, df_res, cost_res, centers = [], [], [], []
    for i in range(10):
        if i == 0:
            a,b,c,d = solve_discrete(df, state, 3)
        else:
            a,b,c,d = solve_discrete(df, state, 3, df_res[-1]['geometry'].centroid.values)
        sinkhorn_res.append(a)
        df_res.append(b)
        cost_res.append(c)
        centers.append(d)
    return sinkhorn_res, df_res, cost_res, centers
