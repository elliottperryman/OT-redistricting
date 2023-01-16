"""
Algorithms for solving redistricting by optimal transport
"""

## Standard imports
import json
import numpy as np
from shapely.geometry import Point
from geopandas import GeoSeries
from State import State
import matplotlib.pyplot as plt

def rand_guess(state)->Point:
    """
    rand_guess puts a point randomly in the box surrounding the state
    """
    minx, miny, maxx, maxy = state.state_geometry.bounds
    LB, UB = np.array([minx, miny]), np.array([maxx, maxy])
    p = Point(*(np.random.random()*(UB-LB)+LB))
    return p

def grid_points(state, h)->GeoSeries:
    minx, miny, maxx, maxy = state.state_geometry.bounds
    LB, UB = np.array([minx, miny]), np.array([maxx, maxy])
    x = np.arange(LB[0], UB[0], h)
    y = np.arange(LB[1], UB[1], h)
    pts = GeoSeries([Point([x[i],y[j]]) for i in range(len(x)) for j in range(len(y))])
    pts.set_crs(state.df.crs)
    return pts

def sample_rand(state:State)->GeoSeries:
    # centroids = df.to_crs(crs=3857).centroid.to_crs(4269).values
    chosen = np.random.choice(a=len(state.df), size=state.num_districts, replace=False, p=state.df['pop'].values)
    samples =  GeoSeries(state.centroid.values[chosen])
    samples.set_crs(4269)
    return samples

def plot_list_of_districts(districts):
    scores = []
    for i,d in enumerate(districts):
        num = d.state.state_num
        d.plot(save_filename='figs/state_'+str(num)+'_district_'+str(i))
        print(d)
        scores.append(d.score())
        print(d.dissolved.head())
    with open('data/state_'+str(num)+'_scores.json', 'w') as file:
        file.write(json.dumps(scores))
    plt.close()
    plt.gca().clear()
    plt.plot(list(range(1,len(scores)+1)), scores)
    plt.yscale('log')
    plt.title('Summed distance to center vs iteration')
    plt.ylabel(r'$\sum_i \alpha_i * ||d_i - c||$')
    plt.xlabel('iteration')
    plt.savefig('figs/state_'+str(num)+'_scores', bbox_inches='tight', transparent=True)
