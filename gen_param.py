class gen_param:
	def __init__(self):

		self.counter=0

		# for my adapted mutation rate

		# pos. int population size (number of genomes in one generation)
		pop_size_pool=[20,50,80]
		# decimal amount of number of high society genomes in a population
		clergy_size_pool=[0,0.2]
		# pos. int (smaller than pop_size) number of children of high society genomes
		clergy_children_pool=[3]
		# decimal amount of number of middle class genomes in a population
		nobility_size_pool=[0,0.1]
		# pos. int (smaller than pop_size) number of children of middle class genomes
		nobility_children_pool=[2]
		# pos. int (smaller than nr of demands) mutation rate at beginning
		start_mut_pool=[3,5,10]
		# non-allocated choice probability percentage
		non_prob_pool=[20,30,50]
		# weight of acceptance in fitness function		
		weight_ac_pool=[0.9]
		# mutation rate method	
		mut_method_pool=[2]
		self.all_param=[]
		for pop_size in pop_size_pool:
			for clergy_size in clergy_size_pool:
				for clergy_children in clergy_children_pool:
					for nobility_size in nobility_size_pool:
						for nobility_children in nobility_children_pool:
							for start_mut in start_mut_pool:
								for non_prob in non_prob_pool:
									for weight_ac in weight_ac_pool:
										for mut_method in mut_method_pool:
											self.all_param.append(\
		[pop_size, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, non_prob, weight_ac, mut_method])
		
	
		# for the 1/5 rule

		# pos. int population size (number of genomes in one generation)
		pop_size_pool=[20,50,80]
		# decimal amount of number of high society genomes in a population
		clergy_size_pool=[0]
		# pos. int (smaller than pop_size) number of children of high society genomes
		clergy_children_pool=[0]
		# decimal amount of number of middle class genomes in a population
		nobility_size_pool=[0]
		# pos. int (smaller than pop_size) number of children of middle class genomes
		nobility_children_pool=[0]
		# pos. int (smaller than nr of demands) mutation rate at beginning
		start_mut_pool=[3,5,10]
		# non-allocated choice probability percentage
		non_prob_pool=[20,30,50]
		# weight of acceptance in fitness function		
		weight_ac_pool=[0.9]
		# mutation rate method	
		mut_method_pool=[1]
		self.all_param=[]
		for pop_size in pop_size_pool:
			for clergy_size in clergy_size_pool:
				for clergy_children in clergy_children_pool:
					for nobility_size in nobility_size_pool:
						for nobility_children in nobility_children_pool:
							for start_mut in start_mut_pool:
								for non_prob in non_prob_pool:
									for weight_ac in weight_ac_pool:
										for mut_method in mut_method_pool:
											self.all_param.append(\
		[pop_size, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, non_prob, weight_ac, mut_method])
		


	def next(self):
		if self.counter<len(self.all_param):
			self.counter+=1
			return self.all_param[self.counter-1]
		else:
			None

	def size(self):
		return len(self.all_param)


# converts a number of seconds to a string hh:mm:ss
def sec2timestr(sec):
	m, s = divmod(sec, 60)
	h, m = divmod(m, 60)
	return "%d:%02d:%02d" % (h, m, s)




