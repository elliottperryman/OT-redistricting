import json
from State import State
state = State(23) # use maine because it has only 2 districts

# from discrete_alg import solve_discrete
# district = solve_discrete(state)

from lloyd_alg import lloyd_alg
districts = lloyd_alg(state, 3)

scores = []
for i,d in enumerate(districts):
    d.plot(save_filename='data/state_23_district_'+str(i))
    scores.append(d.score())
with open('data/state_23_scores.json', 'w') as file:
    file.write(json.dumps(scores))