from State import State
from discrete_alg import solve_discrete

def lloyd_alg(state: State, least_improvement=1e-3, max_iter=15):
    districts = [solve_discrete(state)]
    for i in range(max_iter-1):
        try:
            districts.append(solve_discrete(state, districts[-1].new_centers))
            if i>3:
                if (
                    abs(districts[-2].score()-districts[-1].score())<least_improvement and
                    abs(districts[-3].score()-districts[-2].score())<least_improvement and
                    abs(districts[-4].score()-districts[-3].score())<least_improvement
                ):
                    return districts
        except RuntimeError as err:
            print('got err')
            print(err)
            return districts
    return districts