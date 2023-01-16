"""
Algorithms for solving redistricting by optimal transport
"""

## Standard imports
import json
import numpy as np
import shapely
from geopandas import GeoSeries
from State import State
import matplotlib.pyplot as plt

def rand_guess(state):
    """
    rand_guess puts a point randomly in the box surrounding the state
    """
    minx, miny, maxx, maxy = state.bounds
    LB, UB = np.array([minx, miny]), np.array([maxx, maxy])
    p = shapely.geometry.Point(*(np.random.random()*(UB-LB)+LB))
    return p

def sample_rand(state:State):
    # centroids = df.to_crs(crs=3857).centroid.to_crs(4269).values
    chosen = np.random.choice(a=len(state.df), size=state.num_districts, replace=False, p=state.df['pop'].values)
    samples =  GeoSeries(state.centroid.values[chosen])
    samples.set_crs(4269)
    return samples

def plot_list_of_districts(districts):
    scores = []
    for i,d in enumerate(districts):
        num = d.state.state_num
        d.plot(save_filename='data/state_'+str(num)+'_district_'+str(i))
        print(d)
        scores.append(d.score())
        print(d.dissolved.head())
    with open('data/state_'+str(num)+'_scores.json', 'w') as file:
        file.write(json.dumps(scores))
    plt.close()
    plt.gca().clear()
    plt.plot(list(range(1,len(scores)+1)), scores)
    plt.title('Summed distance to center vs iteration')
    plt.ylabel(r'$\sum_i \alpha_i * ||d_i - c||$')
    plt.xlabel('iteration')
    plt.savefig('data/state_'+str(num)+'_scores', bbox_inches='tight', transparent=True)
