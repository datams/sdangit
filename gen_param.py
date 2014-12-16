class gen_param:
	def __init__(self):
		# pos. int population size (number of genomes in one generation)
		self.pop_size_pool=[8,10,15,20]
		# pos. int maximum number of iterations resp. generations
		self.maxgenerations_pool=[10,15,30]
		# decimal amount of number of high society genomes in a population
		self.clergy_size_pool=[0.1]
		# pos. int (smaller than pop_size) number of children of high society genomes
		self.clergy_children_pool=[2,4]
		# decimal amount of number of middle class genomes in a population
		self.nobility_size_pool=[0.1]
		# pos. int (smaller than pop_size) number of children of middle class genomes
		self.nobility_children_pool=[2]
		# pos. int (smaller than nr of demands) mutation rate at beginning
		self.start_mut_pool=[8,4,1]
		# pos. int (smaller than nr of demands) mutation rate at the end
		self.end_mut_pool=[1]
		# non-allocated choice probability percentage
		self.non_prob_pool=[10,15]
		# weight of acceptance in fitness function		
		self.weight_ac_pool=[0.9,0.7]
		self.all_param=[]
		for pop_size in self.pop_size_pool:
			for maxgenerations in self.maxgenerations_pool:
				for clergy_size in self.clergy_size_pool:
					for clergy_children in self.clergy_children_pool:
						for nobility_size in self.nobility_size_pool:
							for nobility_children in self.nobility_children_pool:
								for start_mut in self.start_mut_pool:
									for end_mut in self.end_mut_pool:
										for non_prob in self.non_prob_pool:
											for weight_ac in self.weight_ac_pool:
												self.all_param.append([pop_size, maxgenerations, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, end_mut, non_prob, weight_ac])
		self.counter=0
	
	def next(self):
		if self.counter<len(self.all_param):
			self.counter+=1
			return self.all_param[self.counter-1]
		else:
			None

	def size(self):
		return len(self.all_param)


'''
a=gen_param()
while(True):
	val = a.get_set()
	if val==None:
		print 'Value Counter '+str(a.counter)
		break
	else:
		print val
'''