from PIL import Image, ImageDraw
import argparse
import random
import numpy as np

src_path = 'yingyang1010.jpg'
model_img = Image.open(src_path)
model_imgarr = np.array(model_img)


class Individual():

	def __init__(self, imgarr):
		self.imgarr = imgarr
		self.fitness = self.cal_fitness()

	def cal_fitness(self):
		global model_imgarr
		fitness = 0
		modelarr_shape = model_imgarr.shape
		for i in range(modelarr_shape[0]):
			for j in range(modelarr_shape[1]):
				#if((self.imgarr[i][j][0] == model_imgarr[i][j][0]) and (self.imgarr[i][j][1] == model_imgarr[i][j][1]) and (self.imgarr[i][j][2] == model_imgarr[i][j][2])):
				if(self.imgarr[i][j] == model_imgarr[i][j]):
					fitness = fitness + 1 
		return (fitness/(modelarr_shape[0]*modelarr_shape[1]))*100

	def mate(self, other):
		global model_imgarr
		modelarr_shape = model_imgarr.shape
		offspring = np.zeros(shape=modelarr_shape, dtype=model_imgarr.dtype)
		for i in range(modelarr_shape[0]):
			for j in range(modelarr_shape[1]):
				p = random.random()
				if (p > 0.75):
					offspring[i][j] = other.imgarr[i][j]
				elif (p >= 0.20):
					offspring[i][j] = self.imgarr[i][j]
				else:
					offspring[i][j] = mutation()
				# if (p > 0.80):
				# 	offspring[i][j] = mutation()
				# elif (p > 0.30):
				# 	p1 = random.random()
				# 	if (p1 > 0.50):
				# 		offspring[i][j] = self.imgarr[i][j]
				# 	else:
				# 		offspring[i][j] = other.imgarr[i][j]
				# elif (p <= 0.30):
				# 		offspring[i][j] = (self.imgarr[i][j] + other.imgarr[i][j])/2
		return Individual(offspring)
	
	def __lt__(self, other):
		return self.fitness < other.fitness

	def __gt__(self, other):
		return self.fitness > other.fitness

	def __eq__(self, other):
		return self.fitness == other.fitness

	def __repr__(self):
		return str(self.fitness)

def createGnome():
	global model_imgarr
	modelarr_shape = model_imgarr.shape
	gnome = np.zeros(shape=modelarr_shape, dtype=model_imgarr.dtype)
	for i in range(modelarr_shape[0]):
		for j in range(modelarr_shape[1]):
			gene_pixel = mutation()
			gnome[i][j] = gene_pixel
	return gnome

def mutation():
	li=[0,255]
	return random.choice(li)

def world(population_size, save_interval):

	img_names=['geneticimgs/frame{:05d}.gif'.format(i) for i in range(90000)]
	global model_img
	global model_imgarr

	generation = 0
	population = []
	save_ind = 0

	for i in range(population_size):
		population.append(Individual(createGnome()))

	population = sorted(population, reverse=True)

	while(population[0].fitness < 90):

		new_generation = []
		s = (30*population_size)//100
		for i in range(s):
			new_generation.append(population[i])
		for i in range(s):
			parent1 = random.choice(new_generation)
			parent2 = random.choice(new_generation)
			offspring = parent1.mate(parent2)
			new_generation.append(offspring)
		s = (40*population_size)//100
		for i in range(s):
			parent1 = random.choice(population)
			parent2 = random.choice(population)
			offspring = parent1.mate(parent2)
			new_generation.append(offspring)
		population = sorted(new_generation, reverse=True)
		generation = generation + 1

		if((generation % save_interval) == 0):
			print("Generation: {g}".format(g=generation))
			print("Fitness: {f}".format(f=population[0].fitness))
			print("Saving {s}...".format(s=img_names[save_ind]))
			save_frame = Image.fromarray(population[0].imgarr)
			save_frame.save(img_names[save_ind])
			save_ind = save_ind + 1

if __name__ == '__main__':
	world(50,100)