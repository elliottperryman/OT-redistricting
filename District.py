from State import State
import matplotlib.pyplot as plt
import numpy as np
from geopandas import GeoSeries
from shapely.geometry import Point

class District():
    def __init__(self, state: State, res, centers, ϵ:float):
        self.state = state
        self.res = res
        self.dissolved = None
        self.old_centers = centers
        self.ϵ = ϵ

        # calculate centroids weighted by population (or not!)
        x, y = self.state.df['centroid'].x.values, self.state.df['centroid'].y.values
        normFactor = (self.state.df['pop'].values.reshape(-1,1)*res).sum(0)
        center_x = np.sum((x * self.state.df['pop'].values).reshape(-1,1) * self.res / normFactor, 0)
        center_y = np.sum((y * self.state.df['pop'].values).reshape(-1,1) * self.res / normFactor, 0)
        self.new_centers = GeoSeries([Point([a,b]) for a,b in zip(center_x,center_y)])

    def score(self):
        return np.sum(np.array([self.state.df.distance(p) for p in self.old_centers]).T * self.res)
    
    def plot(self, show=True, save_filename=None):
        if self.dissolved is None:
            self.dissolved = self.state.df.copy()
            self.dissolved['district'] = self.res.argmax(1)
            self.dissolved = self.dissolved.dissolve(by='district', aggfunc='sum')
        self.dissolved.plot(
            column=self.dissolved.index.values, categorical=True, legend=True,
            labels=['District %d' % i for i in range(1,self.state.num_districts+1)]
        )
        plt.ylabel('Longitude')
        plt.xlabel('Latitude')
        plt.title(self.state.pretty_name)
        plt.scatter([_.x for _ in self.old_centers], [_.y for _ in self.old_centers], marker='x', color='red')
        if show and save_filename is None:
            plt.show()
        elif save_filename is not None:
            plt.savefig(save_filename, transparent=True, bbox_inches='tight')

