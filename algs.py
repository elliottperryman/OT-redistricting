import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import fiona
import shapely
import geopandas

def load_pop_df(state_num, discrete=True):
    try: 
        df = geopandas.read_file('data/tl_2020_'+str(state_num).zfill(2)+'_tabblock20.shp')
    except Exception as err:
        print('exception. probably state number does not exist')
        raise err
    # only worry about regions with population 
    df = df[df['POP20']>0]
    total_people = df['POP20'].sum()
    df = geopandas.GeoDataFrame({
        'state': df['STATEFP20'].astype(int),
        'county': df['COUNTYFP20'].astype(int),
        'tract': df['TRACTCE20'].astype(int), 
        'pop': df['POP20'].astype(float)/total_people, 
        })  
    return df
def blur(df, level='tract'):
    pass
"""
def sinkhorn(C, ϵ, MAX_ITER = 1000, verbose = True):

    K = np.exp(-C/ϵ)

    u = np.random.normal(size=K.shape[0])
    v = np.random.normal(size=K.shape[1])
    for i in range(MAX_ITER):
        u_ = a / (K @ v)
        v_ = b / (u_ @ K)
        if np.linalg.norm(u_-u) + np.linalg.norm(v_-v) < 1e-14 and i > 50:
            #print(np.linalg.norm(u_-u), np.linalg.norm(v_-v))
            if verbose: print("Sinkhorn ended with %d iterations"%i)
            break
        u = u_
        v = v_
    return np.diag(u) @ K @ np.diag(v)
"""