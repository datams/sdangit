##### imports #####
import demand as dem
import customGraph as gc
import graphFunctions as gf
import random
import copy
import time

# a population contains a set of individuals (genomes) and can rank them
class population:
    def __init__(self, G, d_list, pop_size, clergy_size, clergy_children, nobility_size, nobility_children, non_prob, weight_ac):
	self.G=G
	self.d_list=d_list
	self.clergy_size=clergy_size
	[self.clergy_members, self.nobility_members, self.rest]=slice_list(range(pop_size), clergy_size, clergy_size+nobility_size)
	self.clergy_children=clergy_children
	self.nobility_size=nobility_size
	self.nobility_children=nobility_children
	self.non_prob=non_prob
	self.weight_ac=weight_ac
	self.weight_bw=1-self.weight_ac
	self.pop_size=pop_size
	# a list with ranking positions for each corresponding demand
	self.ranking=[]
	for k in range(pop_size):
		self.ranking.append(k)
	# a dict with the fitness value for each corresponding demand
	self.fitness={}
	for k in range(pop_size):
		self.fitness[k]=[0,0]
	# a list containing all genomes of the population
	self.individuals=[]
	for k in range(pop_size):
		self.individuals.append(genome(d_list))
    
    # mutate all genomes by level level
    def mutall(self, level):
	for j in range(len(self.individuals)):
		self.individuals[j].mutate(level,self.non_prob)

    # determine the fitness for all genomes and store to fitness dict
    def rateall(self):
	for i in range(len(self.individuals)):
		self.fitness[i]=self.individuals[i].rate(self.G, self.weight_ac, self.weight_bw)

    # determine the ranking based on fitness
    def rank(self):
	# rank due to single fitness value
	# self.ranking=sorted(self.fitness, key=self.fitness.get, reverse=True)
	

	# rank due to two fitness values
	fitness2list=[(k, v[0], v[1]) for k,v in self.fitness.items()]
	sorted_fitness2list = sorted(fitness2list, key = lambda x: (x[1], x[2]), reverse=True)
	self.ranking=[a for (a,b,c) in sorted_fitness2list]


    # return best genome of population and it's fitness
    def best_genome(self):
	i=self.ranking[0]
	#print 'fitness of best genome: '+str(self.fitness[i])
	#print ' with genome '+str(self.individuals[self.ranking[0]].list)
	return [self.individuals[i], self.fitness[i]]
   
    # produce the next generation (clergy are preserved and have clergy_children children, nobility have nobility_children, rest gets remaining slots)
    def evolute(self,mutrate):

	temp=[]
	
	for ii in range(len(self.individuals)):
		if len(temp)<len(self.individuals):
			if ii in self.clergy_members or ii==0:
				jj=self.ranking[ii]
				current_genome=self.individuals[jj].copy()
				temp.append(current_genome)
				for kk in range(self.clergy_children):
					current_genome=self.individuals[jj].copy()
					temp.append(current_genome.mutate(mutrate,self.non_prob))
			elif ii in self.nobility_members:
				jj=self.ranking[ii]
				for kk in range(self.nobility_children):
					current_genome=self.individuals[jj].copy()
					temp.append(current_genome.mutate(mutrate,self.non_prob))
			else:
				jj=self.ranking[ii]
				current_genome=self.individuals[jj].copy()
				temp.append(current_genome.mutate(mutrate,self.non_prob))
	self.individuals=temp

	self.rateall()
	self.rank()

# reflects a genome as a list of path choices for demands
class genome:
    def __init__(self, d_list):
	self.d_list=d_list
	self.size=len(d_list)
	self.list = []
	self.gene_pool=[]
	self.bws=[]
	for k in range(self.size):
		self.list.append(None)
	for i in range(self.size):
		self.gene_pool.append(d_list[i].paths_pack)
	for j in range(self.size):
		self.bws.append(d_list[i].bw)

    def copy(self):
	genome_copy = genome(self.d_list)
	genome_copy.list=self.list[:]
	return genome_copy

    # generates a list of level-many positions in genome
    def randpos(self, level):
	variants=range(self.size)
	randpos=random.sample(set(variants), level)
	return randpos

    # mutates a genome at level-many positions
    def mutate(self,level,non_prob):
	# get random positions in genome
    	randpos=self.randpos(level)
    	for i in randpos:
		# for a given probability (percentage) delete the gen to None
		if randb(non_prob)==1:
			self.list[i]=None
		else:
			# get gen pool of possibilities for genome position
	    		#gene_pool=self.d_list[i].paths_pack
			if self.gene_pool[i]!=[]:
				new_gen=random.choice(gf.pack2p(self.gene_pool[i]))
				self.list[i]=new_gen
	return self

    # reports back the number of allocated paths with a given genome
    def rate(self, G, weight_ac, weight_bw):
	G_updated=G.copy()
	counter=0
	one_failed=False
	for i in range(self.size):
		if self.list[i]!=None:
			#[G_updated, success] = alloc_gen(G_updated, self.list[i], self.d_list[i].bw)
			[G_updated, success] = alloc_gen(G_updated, self.list[i], self.bws[i])
			if success == True:
				counter+=1
			elif success == False:
				one_failed=True
	
	# default fitness
	fitness=[0,0]

	# check if genome sane
	'''	
	genome_is_sane=False
	if gf.minimum_bw(G_updated)>=0:
		genome_is_sane=True
	if genome_is_sane and one_failed==False:
	'''
	
	# bw usage calculations	
	total_alloc_bw=bw_consum(G, G_updated)
	total_req_bw=0
	for i in range(self.size):
		if self.list[i]!=None:
			total_req_bw+=self.bws[i]

	# calculate fitness
	if one_failed==False and total_alloc_bw>0:
		ac_fitness = float(counter)/float(self.size)
		bw_fitness = float(total_req_bw)/float(total_alloc_bw)
		fitness = [ac_fitness, bw_fitness]
	else:
		fitness=[0,0]
	
	return fitness

# tries to allocate a selected path with a given bw and reports if it was possible
def alloc_gen(G, sel_path, bw):
	#G_updated=copy.deepcopy(G)
	G_updated=G.copy()
	if sel_path!=None:
		#print 'alloc: '+str(sel_path)
		G_updated=gf.update_edges(G_updated, sel_path, bw)
		if gf.minimum_bw(G_updated)>0:	
			success=True
		else:
			success=False
			G_updated=G
	else:
		success=False
		G_updated=G
	return [G_updated, success]

# calculates the total bw on all edges available
def bw_available(G):
	total_bw=float(0)
	edges = G.edges()
	for edge in edges:
		from_node = edge[0]
		to_node = edge[1]
		bw = G[from_node][to_node]['bw']
		total_bw+=bw
	return total_bw

# calculates the total bw on all edges consumed
def bw_consum(G, G_updated):
	total_bw=float(0)
	edges = G.edges()
	for edge in edges:
		from_node = edge[0]
		to_node = edge[1]
		orig_bw = G[from_node][to_node]['bw']
		end_bw = G_updated[from_node][to_node]['bw']
		used_bw=float(orig_bw)-float(end_bw)
		total_bw+=used_bw
	return total_bw

# returns 1 with a percentage probability, else 0
def randb(percentage):
	los=[1]*percentage + [0]*(100-percentage)
	decision=random.choice(los)
	return decision

# slices list into 3 parts (0-len*cut1, len*cut1-len*cut2, cut2-end)
def slice_list(orig_list,cut1,cut2):
	first_list = orig_list[0 : int(len(orig_list) * cut1)]
	second_list = orig_list[int(len(orig_list) * cut1) : int(len(orig_list) * cut2)]
	third_list = orig_list[int(len(orig_list) * cut2) : ]
	return[first_list, second_list,	third_list]

# creates a list of mutation rate (integers) with n-many values between bottom and upper
def shape_mut2(n, bottom, upper):
    data=[]
    distance = float(upper - bottom)
    steps = float(n)
    step =  distance / steps
    for i in range(n):
	value=float(bottom) + step * float(i)
	rounded_value=round(value,0)
	int_value=int(rounded_value)
        data.append(int_value)
    return data


# runs multiple evolution iterations in order to find the best genome
def paraevolution(G,d_list,pop_size,clergy_size,clergy_children,nobility_size,nobility_children, start_mut, non_prob, weight_ac, mut_method, target_ratio, e, return_ratio, return_paths, ga_thread):
	
	# get start time for time out
	time_start = time.time()

	# create population
	p=population(G, d_list, pop_size, clergy_size, clergy_children, nobility_size, nobility_children, non_prob, weight_ac)

	# For number of iterations:
	cycles=0

	# set initial mutation rate	
	mutrate=int(start_mut*len(d_list)/100)
	#mutrate=int(len(p.d_list)*0.7)

	# initial iteration
	p.evolute(mutrate)

	# EVOLUTION
	while(True):
		# get old best genome
		[old_best_genome, old_best_fitness]=p.best_genome()
		old_best_acc=old_best_fitness[0]
		old_fitness=p.fitness.copy()
		
		# ITERATION
		p.evolute(mutrate)

		# get new best gnome
		[new_best_genome, new_best_fitness]=p.best_genome()
		###gf.write2file('GAGARATE', 'ga_thread '+str(ga_thread)+'new best fitness: '+str(new_best_fitness))
		new_best_acc=new_best_fitness[0]
		new_fitness=p.fitness
		
		# check hit
		target_hit=False
		if target_ratio-0.05<=new_best_acc:
			target_hit=True
		
		# check timeout
		GA_timeout=False
		time_now = time.time()
		calc_time = time_now - time_start
		if calc_time>12:
			GA_timeout=True

		# handle hit, timeout or termination
		if target_hit or GA_timeout:
			result=[]
			sel_paths={}
			acc_ratio=0
			# red out the allocated paths
			for j in range(new_best_genome.size):
				if new_best_genome.list[j]!=None:
					result.append(new_best_genome.list[j])
					sel_paths[j]=[new_best_genome.list[j],d_list[j].bw]
				else:
					pass
			acc_ratio=float(len(result))/float(len(d_list))

		if target_hit:
			print 'GA hit target'
			e.set()
			return_ratio[0]=[new_best_acc]
			return_paths[0]=[sel_paths]
			break
		if GA_timeout:
			print 'GA timeout'
			e.set()
			return_ratio[0]=[new_best_acc]
			return_paths[0]=[sel_paths]
			break
		if e.is_set():
			print 'Another GA finished'
			break

		# PRODUCE MUT RATE
		# constant mutation rate
		if mut_method==0:
			pass
			# constant mutation rate

		# adaptive mut rate 1/5 rule
		if mut_method==1:
			n_better_childern=0
			for k in new_fitness:
				if new_fitness[k][0]>old_fitness[k][0]:
					n_better_childern+=1
			if n_better_childern > p.pop_size/5 and mutrate<len(p.d_list):
				mutrate += 1
			elif n_better_childern == p.pop_size/5:
				pass
			elif mutrate>1:
				mutrate -=1
		
		if mut_method==2:
			# adaptive mut rate based on diff
			diff=new_best_acc-old_best_acc
			if diff>0.2:
				if mutrate>1: # mutrate>int((1-new_best_acc+0.2)*len(p.d_list)*0.7): #as the maximum mut rate going down over time
					mutrate-=1
			if diff<0.2:
				if mutrate<len(p.d_list):
					mutrate+=1

		cycles+=1

	return [result, sel_paths, new_best_acc, cycles]

