from State import State
import matplotlib.pyplot as plt

class District():
    def __init__(self, state: State, res, df, cost_val, centers):
        self.state = state
        self.res = res
        self.df = df
        self.cost_val = cost_val
        self.centers = centers

    def plot(self):
        self.df.plot(column=self.df.index.values, categorical=True, legend=True)
        plt.ylabel('Longitude')
        plt.xlabel('Latitude')
        plt.title(self.state.pretty_name)
        plt.scatter([_.x for _ in self.centers], [_.y for _ in self.centers])