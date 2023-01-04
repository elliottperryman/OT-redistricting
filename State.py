import geopandas
import matplotlib.pyplot as plt

states_dict= {val:key for key,val in {
     "ALABAMA": 1, "ALASKA": 2, "ARIZONA": 4, "ARKANSAS": 5, "CALIFORNIA": 6, "COLORADO": 8, "CONNECTICUT": 9, "DELAWARE": 10, "DISTRICT_OF_COLUMBIA": 11, "FLORIDA": 12, "GEORGIA": 13, "HAWAII": 15, "IDAHO": 16, "ILLINOIS": 17, "INDIANA": 18, "IOWA": 19, "KANSAS": 20, "KENTUCKY": 21, "LOUISIANA": 22, "MAINE": 23, "MARYLAND": 24, "MASSACHUSETTS": 25, "MICHIGAN": 26, "MINNESOTA": 27, "MISSISSIPPI": 28, "MISSOURI": 29, "MONTANA": 30, "NEBRASKA": 31, "NEVADA": 32, "NEW_HAMPSHIRE": 33, "NEW_JERSEY": 34, "NEW_MEXICO": 35, "NEW_YORK": 36, "NORTH_CAROLINA": 37, "NORTH_DAKOTA": 38, "OHIO": 39, "OKLAHOMA": 40, "OREGON": 41, "PENNSYLVANIA": 42, "RHODE_ISLAND": 44, "SOUTH_CAROLINA": 45, "SOUTH_DAKOTA": 46, "TENNESSEE": 47, "TEXAS": 48, "UTAH": 49, "VERMONT": 50, "VIRGINIA": 51, "WASHINGTON": 53, "WEST_VIRGINIA": 54, "WISCONSIN": 55, "WYOMING": 56, "PUERTO_RICO": 72
     }.items()}

class State():
    def __init__(self, state_num, discrete=True):
        self.state_num = state_num
        self.state_name = states_dict[state_num]
        self.pretty_name = self.state_name.replace('_',' ').title()
        self.discrete = discrete

        df = df = geopandas.read_file(f'data/tl_2020_{state_num:02d}_tabblock20/tl_2020_{state_num:02d}_tabblock20.shp')

        # only worry about regions with non-zero population
        df = df[df['POP20']>0]
        # count total people in region 
        total_people = df['POP20'].sum()
        # create template to grab features from
        df = geopandas.GeoDataFrame({
            'state': df['STATEFP20'].astype(int), 
            'county': df['COUNTYFP20'].astype(int),
            'tract': df['TRACTCE20'].astype(int), 
            'block': df['BLOCKCE20'].astype(int),
            'pop': df['POP20'].astype(float)/total_people, 
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
    
    def plot(self):
        self.block_df.plot(column='pop', cmap='Reds')
        plt.ylabel('Longitude')
        plt.xlabel('Latitude')
        plt.title(self.state.pretty_name)

