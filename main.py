from misc import plot_list_of_districts
from State import State
from uber_lloyd import uber_lloyd

num = 47 # gonna see if there are still islands

state = State(num, lvl='county') 
print(state)
print(state.df)

districts = uber_lloyd(state)
plot_list_of_districts(districts)
