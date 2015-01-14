class gen_param:
	def __init__(self):
		# pos. int population size (number of genomes in one generation)
		self.pop_size_pool=[20,50,80]
		# decimal amount of number of high society genomes in a population
		self.clergy_size_pool=[0,0.2]
		# pos. int (smaller than pop_size) number of children of high society genomes
		self.clergy_children_pool=[3]
		# decimal amount of number of middle class genomes in a population
		self.nobility_size_pool=[0,0.1]
		# pos. int (smaller than pop_size) number of children of middle class genomes
		self.nobility_children_pool=[2]
		# pos. int (smaller than nr of demands) mutation rate at beginning
		self.start_mut_pool=[3,5,10]
		# non-allocated choice probability percentage
		self.non_prob_pool=[20,30,50]
		# weight of acceptance in fitness function		
		self.weight_ac_pool=[0.9]
		# mutation rate method	
		self.mut_method_pool=[2,1]
		self.all_param=[]
		for pop_size in self.pop_size_pool:
			for clergy_size in self.clergy_size_pool:
				for clergy_children in self.clergy_children_pool:
					for nobility_size in self.nobility_size_pool:
						for nobility_children in self.nobility_children_pool:
							for start_mut in self.start_mut_pool:
								for non_prob in self.non_prob_pool:
									for weight_ac in self.weight_ac_pool:
										for mut_method in self.mut_method_pool:
											self.all_param.append(\
		[pop_size, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, non_prob, weight_ac, mut_method])
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
