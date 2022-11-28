import numpy as np
import matplotlib.pyplot as plt
import fiona
import shapely
import geopandas

def load_pop_df(state_num, discrete=True):
    df = geopandas.read_file('data/tl_2020_'+str(state_num).zfill(2)+'_tabblock20.shp')
    return df
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
