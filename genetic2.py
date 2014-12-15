##### imports #####
import demand as dem
import customGraph as gc
import graphFunctions as gf
import random
import copy

# a population contains a set of individuals (genomes) and can rank them
class population:
    def __init__(self, G, d_list, pop_size, clergy_size, clergy_children, nobility_size, nobility_children, non_prob, weight_ac, weight_bw):
	self.G=G
	self.d_list=d_list
	self.clergy_size=clergy_size
	self.clergy_children=clergy_children
	self.nobility_size=nobility_size
	self.nobility_children=nobility_children
	self.non_prob=non_prob
	self.weight_ac=weight_ac
	self.weight_bw=weight_bw
	# a list with ranking positions for each corresponding demand
	self.ranking=[]
	# a dict with the fitness value for each corresponding demand
	self.fitness={}
	# a list containing all genomes of the population
	self.individuals=[]
	# initialize all genomes
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
	self.ranking=sorted(self.fitness, key=self.fitness.get, reverse=True)

    # produce the next generation (clergy are preserved and have clergy_children children, nobility have nobility_children, rest gets remaining slots)
    def fork(self,level):
	# initialize individuals
	new_individuals=[]
	# create indices for clergy, nobility and rest
	[clergy, nobility, rest]= slice_list(range(len(self.individuals)), self.clergy_size, self.nobility_size)
	#print len(self.individuals)
	#print clergy
	#print nobility
	for l in range(len(self.individuals)):
		index=self.ranking[l]
		if l in clergy:
			new_individuals.append(self.individuals[index])
			for h in range(self.clergy_children):
				new_individuals.append(self.individuals[index].mutate(level,self.non_prob))
		elif l in nobility:
			for h in range(self.nobility_children):
				new_individuals.append(self.individuals[index].mutate(level,self.non_prob))
		elif len(new_individuals)<len(self.individuals):
			new_individuals.append(self.individuals[index].mutate(level,self.non_prob))
	self.individuals=new_individuals

    # return best genome of population
    def best_genome(self):
	index=self.ranking[0]
	print 'fitness of best genome: '+str(self.fitness[index])
	print 'all ranking values: '+str(self.ranking)
	print 'all fitness values: '+str(self.fitness)
	return self.individuals[index]


# reflects a genome as a list of path choices for demands
class genome:
    def __init__(self, d_list):
	self.d_list=d_list
	self.size=len(d_list)
	self.list = []
	for k in range(self.size):
		self.list.append(None)

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
	    		gen_pool=self.d_list[i].paths_pack
			if gen_pool!=[]:
				new_gen=random.choice(gf.pack2p(gen_pool))
				self.list[i]=new_gen
	return self

    # reports back the number of allocated paths with a given genome
    def rate(self, G, weight_ac, weight_bw):
	G_updated=copy.deepcopy(G)
	counter=0
	#alloc_status=[]
	one_failed=False
	for i in range(len(self.d_list)):
		#alloc_status.append(None)
		if self.list[i]!=None:
			[G_updated, success] = alloc_gen(G_updated, self.list[i], self.d_list[i].bw)
			if success == True:
				counter+=1
				#alloc_status[i]=True
			elif success == False:
				#alloc_status[i]=None
				one_failed=True
	
	# default fitness=0
	fitness=0	

	# check if genome sane
	#genome_is_sane=False
	#if gf.minimum_bw(G_updated)>=0:
	#	genome_is_sane=True
	#if genome_is_sane and one_failed==False:
	if one_failed==False:
		# calculate fitness
		total_alloc_bw=bw_consum(G, G_updated)
		total_req_bw=0
		for i in range(len(self.d_list)):
			if self.list[i]!=None:
				total_req_bw+=self.d_list[i].bw
		if total_alloc_bw>0:
			fitness = weight_ac*float(counter)/float(len(self.d_list)) + weight_bw*float(total_req_bw)/float(total_alloc_bw)
			#fitness=0.9*float(counter)+0.1/total_alloc_bw
	return fitness

# tries to allocate a selected path with a given bw and reports if it was possible
def alloc_gen(G, sel_path, bw):
	G_updated=copy.deepcopy(G)
	if sel_path!=None:
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
def paraevolution(G,d_list,pop_size,maxgenerations,lp_ratio,clergy_size,clergy_children,nobility_size,nobility_children, start_mut, end_mut, non_prob, weight_ac, weight_bw):
	
	# determine all feasible paths
	for i in range(len(d_list)):
		G_prune=copy.deepcopy(G)
		G_prune=gf.prune_bw(G_prune, d_list[i].get_bw())
		pathpack=gf.shortest_p(G_prune,d_list[i].source,d_list[i].target,d_list[i].lat)
		d_list[i].set_paths_pack(pathpack)

	# create population
	p=population(G, d_list, pop_size, clergy_size, clergy_children, nobility_size, nobility_children, non_prob, weight_ac, weight_bw)

	# create initial generation by mutating all individuals
	p.mutall(1)

	# set burst duration
	burst_duration=2
	# For number of iterations:
	cycles=0
	mutationrate=shape_mut2(maxgenerations, start_mut, end_mut)

	while(True):
		p.rateall()
		p.rank()
		print 'ranking '+str(p.ranking)
		print 'fitness '+str(p.fitness)

		if cycles==maxgenerations-1:
			selection=p.best_genome()
			sel_paths={}
			result=[]
			alloc_counter=0
			# only show the allocatable paths as a result
			for j in range(len(selection.list)):
				if selection.list[j]:
					result.append(selection.list[j])
					sel_paths[j]=[selection.list[j],d_list[j].bw]
					alloc_counter+=1
				else:
					pass
					#result.append(None)
			acc_ratio=float(len(result))/float(len(d_list))
			break

		cycles+=1
		p.fork(mutationrate[cycles])


	'''	
	burst_timer=burst_duration
	bursting=False
	while(True):
		if cycles%7 == 0 or bursting:
			bursting=True
			mutationrate=4
			burst_timer-=1
			if burst_timer<=0:
				burst_timer=burst_duration
				bursting=False
		else:
			mutationrate=1
		p.rateall()
		p.rank()

		if cycles==maxgenerations:
			selection=p.best_genome()
			sel_paths={}
			result=[]
			alloc_counter=0
			# only show the allocatable paths as a result
			for j in range(len(selection.list)):
				if selection.list[j]:
					result.append(selection.list[j])
					sel_paths[j]=[selection.list[j],d_list[j].bw]
					alloc_counter+=1
				else:
					pass
					#result.append(None)
			acc_ratio=float(len(result))/float(len(d_list))
			break
		cycles+=1
		p.fork(mutationrate)
	'''
	return [result, sel_paths, acc_ratio, cycles]




