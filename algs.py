import numpy as np
import numba as nb
import matplotlib.pyplot as plt
import pandas as pd
import fiona
import shapely
import geopandas

def load_pop_df(state_num):
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
    state = (df[['state', 'geometry']]).dissolve('state')['geometry'].values[0]
    county_df = (df[['county', 'pop', 'geometry']]).dissolve('county', aggfunc='sum')
    tract_df = (df[['tract', 'pop', 'geometry']]).dissolve('tract', aggfunc='sum')
    block_df = df[['block', 'pop', 'geometry']]
    return block_df, tract_df, county_df, state

def discrete(df):
    df['geometry'] = df['geometry'].centroid # to_crs(3857).centroid.to_crs(epsg=4326)
    return df

def rand_guess(state):
    minx, miny, maxx, maxy = state.bounds
    LB, UB = np.array([minx, miny]), np.array([maxx, maxy])
    p = shapely.geometry.Point(*(np.random.random()*(UB-LB)+LB))
    return p

def u_v_gen(C):
    return np.random.normal(size=C.shape[0]), np.random.normal(size=C.shape[1])

@nb.njit(cache=True)
def _sinkhorn(C, ϵ, a, b, u, v, MAX_ITER = 10_000, verbose = True):

    K = np.exp(-C/ϵ)

    for i in range(MAX_ITER):
        u_ = a / (K @ v)
        v_ = b / (u_ @ K)
        if np.linalg.norm(u_-u) + np.linalg.norm(v_-v) < 1e-14 and i > 50:
            # if verbose: print("Sinkhorn ended with %d iterations"%i)
            break
        u = u_
        v = v_
    return np.diag(u) @ K @ np.diag(v)
def sinkhorn(C, ϵ, a, b, MAX_ITER=10_000, verbose=True):
    return _sinkhorn(C, ϵ, a, b, *u_v_gen(C), MAX_ITER, verbose)
@nb.njit(cache=True)
def cost(C,res):
    return np.sum(C*res)

C = np.random.random((4,2))
a, b = np.ones(4)/2, np.ones(2)
cost(C,sinkhorn(C, 1e-2, a, b))

def plot(res, df, name):
    df.plot(column=res.argmax(1), categorical=True)
    plt.savefig(name)
    
def solve_discrete(state_num, K):
    block, tract, county, state = load_pop_df(10)
    df = tract 
    centers = [rand_guess(state) for i in range(K)]
    centroids = df['geometry'].centroid 
    C = np.array([centroids.distance(p) for p in centers]).T
    C /= np.max(C)

    N = len(df)
    a, b = df['pop'].values, np.ones(K)/K

    res = sinkhorn(C, 1e-3, a, b, 100) 
    df2 = df.copy()
    df2['district'] = res.argmax(1)
    df2 = df2.dissolve(by='district', aggfunc='sum')

    return res, df, df2, cost(res, C)
