from State import State
from discrete_alg import solve_discrete

def lloyd_alg(state: State, lvl='tract', iterations=10):
    districts = [solve_discrete(state, lvl)]
    for i in range(iterations-1):
        try:
            districts.append(solve_discrete(state, lvl, districts[-1].centers))
        except RuntimeError as err:
            print('got err')
            print(err)
            return districts
    return districts