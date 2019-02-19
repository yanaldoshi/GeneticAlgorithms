import random
import argparse
import math

model = -1

class Individual():

	def __init__(self, chromosome):
		self.chromosome = chromosome
		self.fitness = self.cal_fitness()

	def cal_fitness(self):
		global model
		return abs((model-int(self.chromosome,2)))

	def mate(self, other):
		offspring = ""
		chromosome_length=len(self.chromosome)
		for i in range(chromosome_length):
			p = random.random()
			if(p < 0.150): offspring = offspring + str(mutation())
			elif(p <= 0.425): offspring = offspring + other.chromosome[i]
			elif(p > 0.425): offspring = offspring + self.chromosome[i]
		return Individual(offspring)

	def __lt__(self, other):
		return self.fitness < other.fitness
	
	def __gt__(self, other):
		return self.fitness > other.fitness	

	def __str__(self):
		return self.chromosome

	def __repr__(self):
		return self.chromosome

def mutation():
	p = random.random()
	if(p > 0.5): return 1
	else: return 0


def createGnome(k):
	b = random.getrandbits(k)
	return bin(b)[2:].zfill(k)


def world(inpNum, population_size):

	f=open('output.txt','w+')
	global model
	generation = 0
	model = inpNum
	population = []
	bit_power = math.ceil(math.log(model, 2))
	f.write("Model Number: {m}\tBits: {b}\n".format(m=model,b=bit_power))
	for i in range(population_size):
		population.append(Individual(createGnome(bit_power)))
	population=sorted(population)

	f.write("Initial Population: {p}\tBest Fitness: {f}\n".format(p=population,f=population[0].fitness))

	while(population[0].fitness != 0):

		new_generation = []
		s = (10*population_size)//100
		for i in range(s):
			new_generation.append(population[i])
		s=(90*population_size)//100
		for i in range(s):
			length = len(population)
			r = random.randrange(0, length)
			parent1 = population[r]
			r = random.randrange(0, length)
			parent2 = population[r]
			offspring = parent1.mate(parent2)
			new_generation.append(offspring)

		population = sorted(new_generation)
		generation = generation + 1
		f.write("Generation: {g}\tBest Individual: {i}\tFitness: {f}\n".format(g=generation, i=population[0], f=population[0].fitness))

	f.write("Final Generation: {g}\tSolution: {i}\tFitness: {f}\n".format(g=generation, i=population[0], f=population[0].fitness))
	f.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--model', type = int, help = "Number you want to achieve")
	parser.add_argument('--size', type = int, help = "Population size")
	args = parser.parse_args()
	world(args.model, args.size)





