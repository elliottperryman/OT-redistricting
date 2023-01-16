from State import State
from lloyd_alg import lloyd_alg
import numpy as np

def uber_lloyd(state:State, tries=10):
	results = []
	for i in range(tries):
		results.append(lloyd_alg(state))
	best_i = np.argmax([results[i][-1].score() for i in range(tries)])
	return results[best_i]
