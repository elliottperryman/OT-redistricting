import geopandas
import matplotlib.pyplot as plt
from state_district_count import state_district_count
from state_name_by_number import state_name_by_number

class State():
    def __init__(self, state_num, discrete=True):
        self.state_num = state_num
        self.state_name = state_name_by_number[state_num]
        self.pretty_name = self.state_name.replace('_',' ').title()
        self.discrete = discrete
        self.num_districts = state_district_count[self.state_name]

        df = df = geopandas.read_file(f'data/tl_2020_{state_num:02d}_tabblock20/tl_2020_{state_num:02d}_tabblock20.shp')

        # only worry about regions with non-zero population
        df = df[df['POP20']>0]
        # count total people in region 
        self.total_people = df['POP20'].sum()
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
        self.block_df = df[['block', 'pop', 'geometry']]
        tract_df = df.dissolve(by='tract', aggfunc=agg)
        county_df = tract_df.dissolve(by='county', aggfunc=agg)
        state_df = county_df.dissolve(by='state', aggfunc=agg)

        self.tract_df = tract_df[['pop', 'geometry']]
        self.county_df = county_df[['pop', 'geometry']]
        self.state_geometry = state_df['geometry'].values[0]
    
    def plot(self, show=True):
        self.block_df.plot(column=self.block_df['pop']*self.total_people, cmap='Reds')
        plt.ylabel('Longitude')
        plt.xlabel('Latitude')
        plt.title(self.pretty_name)
        if show:
            plt.show()
