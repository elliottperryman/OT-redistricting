import geopandas
import matplotlib.pyplot as plt
from state_district_count import state_district_count
from state_name_by_number import state_name_by_number

class State():
    def __init__(self, state_num, lvl='tract', discrete=True):
        self.state_num = state_num
        self.state_name = state_name_by_number[state_num]
        self.pretty_name = self.state_name.replace('_',' ').title()
        self.discrete = discrete
        self.num_districts = state_district_count[self.state_name]

        df = geopandas.read_file(f'data/tl_2020_{state_num:02d}_tabblock20.shp')

        # only worry about regions with non-zero population
        df = df[df['POP20']>0]
        # count total people in region 
        self.total_people = df['POP20'].sum()
        if self.discrete:
            # create template to grab features from
            df = geopandas.GeoDataFrame({
                'state': df['STATEFP20'].astype(int), 
                'county': df['COUNTYFP20'].astype(int),
                'tract': df['TRACTCE20'].astype(int), 
                'block': df['BLOCKCE20'].astype(int),
                'pop': df['POP20'].astype(float)/self.total_people, 
                'geometry': df['geometry'], 
                })
            # create hierarchy of structures
            agg = {
                    'state':'first', 'county':'first', 
                    'tract':'first', 'block':'first', 'pop':'sum'
            }
            self.df = df.dissolve(by=lvl, aggfunc=agg)
            self._state_geometry = None
            self.df = df[['pop', 'geometry']]
            self.new_crs = self.df.estimate_utm_crs()
            self.old_crs = self.df.crs
            self.centroid = self.df.centroid
        else:
            self.df = geopandas.GeoDataFrame({
                'block': df['BLOCKCE20'].astype(int),
                'pop': df['POP20'].astype(float)/self.total_people, 
                'area': df['geometry'].area,
                'geometry': df['geometry'], 
                })
    def population_covered(self, region):
        '''
            Figure out what % of the total population is inside region
             * assumes a piecewise constant population density
        '''
        return (self.df['pop'] * self.df['geometry'].intersection(region).area / self.df['area']).sum()
    
    def __str__(self):
        return '%s\t\nPopulation: %d\t\n# districts: %d\n' % (self.pretty_name, self.total_people, self.num_districts)

    @property
    def state_geometry(self):
        if self._state_geometry is None:
            self._state_geometry = self.df.dissolve()['geometry'].values[0]
        return self._state_geometry

    def plot(self, show=True):
        self.df.plot(column=self.df['pop']*self.total_people, cmap='Reds')
        plt.ylabel('Longitude')
        plt.xlabel('Latitude')
        plt.title(self.pretty_name)
        if show:
            plt.show()
