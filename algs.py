import numpy as np
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
    state_df = (df[['state', 'geometry']]).dissolve('state')
    county_df = (df[['county', 'pop', 'geometry']]).dissolve('county', aggfunc='sum')
    tract_df = (df[['tract', 'pop', 'geometry']]).dissolve('tract', aggfunc='sum')
    block_df = df[['block', 'pop', 'geometry']]
    return block_df, tract_df, county_df, state_df

def discrete(df):
    df['geometry'] = df['geometry'].to_crs(3857).centroid.to_crs(epsg=4326)
    return df

def rand_guess(state):
    minx, miny, maxx, maxy = state.geometry.values[0].bounds
    LB, UB = np.array([minx, miny]), np.array([maxx, maxy])
    p = shapely.geometry.Point(*(np.random.random()*(UB-LB)+LB))
    return p

def sinkhorn(C, ϵ, a, b, MAX_ITER = 1000, verbose = True):

    K = np.exp(-C/ϵ)

    u = np.random.normal(size=K.shape[0])
    v = np.random.normal(size=K.shape[1])
    for i in range(MAX_ITER):
        u_ = a / (K @ v)
        v_ = b / (u_ @ K)
        if np.linalg.norm(u_-u) + np.linalg.norm(v_-v) < 1e-14 and i > 50:
            if verbose: print("Sinkhorn ended with %d iterations"%i)
            break
        u = u_
        v = v_
    return np.diag(u) @ K @ np.diag(v)
