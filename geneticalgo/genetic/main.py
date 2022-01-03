# https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/
# genetic algorithm search of the one max optimization problem
from numpy.random import randint
from numpy.random import rand
from geneticalgo.trading.objective import fitness
import pandas as pd


df_sp=pd.read_csv("data/2021-12-06_Top25 SP500 daily.csv")
# Path for running code via notebook
# df_sp=pd.read_csv("../data/2021-12-06_Top25 SP500 daily.csv")
df_sp["datadate"] = pd.to_datetime(df_sp["datadate"].astype(str), format='%Y%m%d')
df_sp = df_sp[["datadate", "conm", "tic", "prcod", "prccd", "prchd", "prcld", "cshtrd"]].rename(columns={"prcod": "Open", "prccd": "Close", "prchd": "High", "prcld": "Low", "cshtrd": "Volume"})


# objective function
def onemax(x):
	return -sum(x)


def net_return(x):
	
	df_stock = df_sp[df_sp["tic"]=="AAL"]
	df_stock = df_stock.drop(columns=["conm", "tic"])
	df_stock = df_stock.sort_values(by="datadate")
	df_stock.reset_index(inplace=True, drop=True)
	
	return fitness(x, df_stock, "timeframe")[0]


# tournament selection
def selection(pop, scores, k=3):
	# first random selection
	selection_ix = randint(len(pop))
	for ix in randint(0, len(pop), k-1):
		# check if better (e.g. perform a tournament)
		if scores[ix] < scores[selection_ix]:
			selection_ix = ix
	return pop[selection_ix]


# crossover two parents to create two children
def crossover(p1, p2, r_cross):
	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	# check for recombination
	if rand() < r_cross:
		# select crossover point that is not on the end of the string
		pt = randint(1, len(p1)-2)
		# perform crossover
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]


# mutation operator
def mutation(bitstring, r_mut):
	for i in range(len(bitstring)):
		# check for a mutation
		if rand() < r_mut:
			# flip the bit
			bitstring[i] = 1 - bitstring[i]


# genetic algorithm
def genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut):
	# initial population of random bitstring
	pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
	# keep track of best solution
	best, best_eval = 0, objective(pop[0])
	# enumerate generations
	for gen in range(n_iter):
		print(f">{gen}")
		# evaluate all candidates in the population
		scores = [objective(c) for c in pop]
		# check for new best solution
		for i in range(n_pop):
			if scores[i] > best_eval:
				best, best_eval = pop[i], scores[i]
				print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))
		# select parents
		selected = [selection(pop, scores) for _ in range(n_pop)]
		# create the next generation
		children = list()
		for i in range(0, n_pop, 2):
			# get selected parents in pairs
			p1, p2 = selected[i], selected[i+1]
			# crossover and mutation
			for c in crossover(p1, p2, r_cross):
				# mutation
				mutation(c, r_mut)
				# store for next generation
				children.append(c)
		# replace population
		pop = children
	return [best, best_eval]


if __name__ == "__main__":

    # define the total iterations
    n_iter = 5
    # bits
    n_bits = 4
    # define the population size
    n_pop = 10
    # crossover rate
    r_cross = 0.9
    # mutation rate
    r_mut = 1.0 / float(n_bits)
    # perform the genetic algorithm search
    best, score = genetic_algorithm(net_return, n_bits, n_iter, n_pop, r_cross, r_mut)
    print('Done!')
    print('f(%s) = %f' % (best, score))