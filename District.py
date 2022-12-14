from State import State
import matplotlib.pyplot as plt
import numpy as np

class District():
    def __init__(self, state: State, res, centers):
        self.state = state
        self.res = res
        self.dissolved = None
        self.centers = centers

    def score(self):
        return np.sum(np.array([self.df.distance(p) for p in self.centers]).T * self.res)
    
    def plot(self, plot=True):
        if self.dissolved is None:
            self.dissolved = self.df.copy()
            self.dissolved['district'] = self.res.argmax(1)
            self.dissolved = self.df.dissolve(by='district', aggfunc='sum')
        self.dissolved.plot(column=self.df.index.values, categorical=True, legend=True)
        plt.ylabel('Longitude')
        plt.xlabel('Latitude')
        plt.title(self.state.pretty_name)
        plt.scatter([_.x for _ in self.centers], [_.y for _ in self.centers])
        if plot:
            plt.show()