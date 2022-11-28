import numpy as np

from algs import load_pop_df, discrete, rand_guess, sinkhorn

block, tract, county, state = load_pop_df(10)

df = discrete(tract)
K = 3
centers = np.array([rand_guess(state) for i in range(K)]) 
C = np.array([df['geometry'].distance(p) for p in centers]).T
C /= np.max(C)

N = len(df)
a, b = np.ones(N)/N, np.ones(K)/K

res = sinkhorn(C, 1e-3, a, b, 100)
print(res)
