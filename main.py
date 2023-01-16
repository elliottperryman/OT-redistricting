from misc import plot_list_of_districts
from State import State

num = 47 # gonna see if there are still islands

state = State(num, lvl='county') 
print(state)
print(state.df)
# from discrete_alg import solve_discrete
# district = solve_discrete(state)

from lloyd_alg import lloyd_alg
districts = lloyd_alg(state)
plot_list_of_districts(districts)
