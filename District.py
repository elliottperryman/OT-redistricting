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
        x, y = self.state.centroid.x.values, self.state.centroid.y.values
        normFactor = (self.state.df['pop'].values.reshape(-1,1)*res).sum(0)
        center_x = np.sum((x * self.state.df['pop'].values).reshape(-1,1) * self.res / normFactor, 0)
        center_y = np.sum((y * self.state.df['pop'].values).reshape(-1,1) * self.res / normFactor, 0)
        self.new_centers = GeoSeries([Point([a,b]) for a,b in zip(center_x,center_y)])

        self._score = None
    def score(self):
        if self._score is None:
            self._score = np.sum(np.array([self.state.centroid.distance(p) for p in self.old_centers]).T * self.res)
        return self._score

    def dissolve(self):
        if self.dissolved is None:
            self.dissolved = self.state.df[['geometry']]
            self.dissolved['district'] = self.res.argmax(1)
            self.dissolved = self.dissolved.dissolve(by='district')

    def plot(self, show=True, save_filename=None):
        self.dissolve()
        self.dissolved.plot(
            column=self.dissolved.index.values, categorical=True 
        )
        # plt.ylabel('Longitude')
        # plt.xlabel('Latitude')
        plt.axis('off')
        plt.title(self.state.pretty_name)
        plt.scatter([_.x for _ in self.old_centers], [_.y for _ in self.old_centers], marker='x', color='red')
        if show and save_filename is None:
            plt.show()
        elif save_filename is not None:
            plt.savefig(save_filename, transparent=True, bbox_inches='tight')

    def __str__(self):
        return 'State: %s\n\tScore: %f\n\tϵ = %f' % (self.state.pretty_name, self.score(), self.ϵ)
