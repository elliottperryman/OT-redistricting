from os import system
system('cd data && bash get.sh')
from State import State
state = State(23) # use alabama because I have it downloaded
from lloyd_alg import lloyd_alg
districts = lloyd_alg(state, 10)