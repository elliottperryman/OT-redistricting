"""
Algorithms for solving redistricting by optimal transport
"""

## Standard imports
import numpy as np
import shapely
from geopandas import GeoSeries

def rand_guess(state):
    """
    rand_guess puts a point randomly in the box surrounding the state
    """
    minx, miny, maxx, maxy = state.bounds
    LB, UB = np.array([minx, miny]), np.array([maxx, maxy])
    p = shapely.geometry.Point(*(np.random.random()*(UB-LB)+LB))
    return p

def sample_rand(df, K):
    centroids = df.to_crs(crs=3857).centroid.to_crs(4269).values
    chosen = np.random.choice(a=len(df), size=K, replace=False, p=df['pop'].values)
    samples =  GeoSeries(centroids[chosen])
    samples.set_crs(4269)
    return samples