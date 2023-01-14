import json
import matplotlib.pyplot as plt
from State import State
state = State(23) # use maine because it has only 2 districts

# from discrete_alg import solve_discrete
# district = solve_discrete(state)

from lloyd_alg import lloyd_alg
districts = lloyd_alg(state, 4)

scores = []
for i,d in enumerate(districts):
    d.plot(save_filename='data/state_23_district_'+str(i))
    print(d)
    scores.append(d.score())
    print(d.dissolved.head())
with open('data/state_23_scores.json', 'w') as file:
    file.write(json.dumps(scores))
plt.close()
plt.gca().clear()
plt.plot(list(range(1,len(scores)+1)), scores)
plt.title('Summed distance to center vs iteration')
plt.ylabel(r'$\sum_i \alpha_i * ||d_i - c||$')
plt.xlabel('iteration')
plt.savefig('data/state_23_scores', bbox_inches='tight', transparent=True)
