##### imports #####
import demand as dem
import customGraph as gc
import graphFunctions as gf
import random
import copy

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

    # return best genome of population and it's fitness
    def best_genome(self):
	i=self.ranking[0]
	print 'fitness of best genome: '+str(self.fitness[i])
	#print ' with genome '+str(self.individuals[self.ranking[0]].list)
	return [self.individuals[i],self.fitness[i]]
   
        # produce the next generation (clergy are preserved and have clergy_children children, nobility have nobility_children, rest gets remaining slots)
    def evolute(self,mutrate):
	#print 'clergy members '+str(self.clergy_members)
	#print 'nobility members'+str(self.nobility_members)
	#print 'nobility childern '+str(self.nobility_children)
	#print 'nobility childern '+str(self.clergy_children)
	self.rateall()
	self.rank()
	temp=[]
	for ii in range(len(self.individuals)):
		if len(temp)<len(self.individuals):
			if ii in self.clergy_members or ii==0:
				jj=self.ranking[ii]
				#current_genome=copy.deepcopy(self.individuals[jj])
				current_genome=self.individuals[jj].copy()
				temp.append(current_genome)
				for kk in range(self.clergy_children):
					#current_genome=copy.deepcopy(self.individuals[jj])
					current_genome=self.individuals[jj].copy()
					temp.append(current_genome.mutate(mutrate,self.non_prob))
			elif ii in self.nobility_members:
				jj=self.ranking[ii]
				for kk in range(self.nobility_children):
					#current_genome=copy.deepcopy(self.individuals[jj])
					current_genome=self.individuals[jj].copy()
					temp.append(current_genome.mutate(mutrate,self.non_prob))
			else:
				jj=self.ranking[ii]
				#current_genome=copy.deepcopy(self.individuals[jj])
				current_genome=self.individuals[jj].copy()
				temp.append(current_genome.mutate(mutrate,self.non_prob))
	#print 'equal len '+str(len(temp)==len(self.individuals))
	self.individuals=temp


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
	#G_updated=copy.deepcopy(G)
	G_updated=G.copy()
	counter=0
	#alloc_status=[]
	one_failed=False
	#for i in range(len(self.d_list)):
	for i in range(self.size):
		#alloc_status.append(None)
		if self.list[i]!=None:
			#[G_updated, success] = alloc_gen(G_updated, self.list[i], self.d_list[i].bw)
			[G_updated, success] = alloc_gen(G_updated, self.list[i], self.bws[i])
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
		#for i in range(len(self.d_list)):
		for i in range(self.size):
			if self.list[i]!=None:
				total_req_bw+=self.bws[i]
		if total_alloc_bw>0:
			#print weight_ac*float(counter)/float(len(self.d_list))
			#print weight_bw*float(total_req_bw)/float(total_alloc_bw)
			fitness = weight_ac*float(counter)/float(self.size) + weight_bw*float(total_req_bw)/float(total_alloc_bw)
			#print 'tot '+str(fitness)
			#fitness=0.9*float(counter)+0.1/total_alloc_bw
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
def paraevolution(G,d_list,pop_size,maxgenerations,clergy_size,clergy_children,nobility_size,nobility_children, start_mut, end_mut, non_prob, weight_ac, target_ratio):
	
	# determine all feasible paths
	for i in range(len(d_list)):
		#G_prune=copy.deepcopy(G)
		G_prune=G.copy()
		G_prune=gf.prune_bw(G_prune, d_list[i].get_bw())
		pathpack=gf.shortest_p(G_prune,d_list[i].source,d_list[i].target,d_list[i].lat)
		d_list[i].set_paths_pack(pathpack)

	# create population
	p=population(G, d_list, pop_size, clergy_size, clergy_children, nobility_size, nobility_children, non_prob, weight_ac)

	# create initial generation by mutating all individuals
	p.mutall(1)

	# For number of iterations:
	cycles=0
	#mutationrate=shape_mut2(maxgenerations, start_mut, end_mut)
	# set initial mutation rate	
	mutrate=start_mut
	p.evolute(mutrate)

	print 'enter loop'
	while(True):
		print 'cycle '+str(cycles)
		#mutrate=mutationrate[cycles]
		print 'mutrate '+str(mutrate)
		# get best fitness value
		[selection, old_best_fitness]=p.best_genome()
		old_fitness=p.fitness.copy()
		#p.evolute(mutationrate[cycles])
		p.evolute(mutrate)
		# print p.ranking
		[selection, fitness]=p.best_genome()
		# count better childern
		#better_childern = [val for val in p.fitness.values() if val > old_best_fitness]
		n_better_childern=0
		for k in p.fitness:
			if p.fitness[k]>old_fitness[k]:
				n_better_childern+=1
		#print 'len(better_childern): '+str(len(better_childern))
		print 'n_better_childern: '+str(n_better_childern)
		print 'len(p.d_list)/5: '+str(len(p.d_list)/5)
		if n_better_childern>=len(p.d_list)/5 and mutrate<len(p.d_list):
			mutrate += 1
		elif mutrate>1:
			mutrate -=1
		#print 'best genome '+str(p.individuals[p.ranking[0]].list)+' with fitness '
		#print 'alle genomes: '
		#for kk in range(len(p.individuals)):
		#	print p.individuals[kk].list
		#print 'ranking '+str(p.ranking)
		#print 'fitness '+str(p.fitness)

		sel_paths={}
		result=[]
		acc_ratio=0
		if fitness>0:
			# only show the allocatable paths as a result
			for j in range(len(selection.list)):
				if selection.list[j]:
					result.append(selection.list[j])
					sel_paths[j]=[selection.list[j],d_list[j].bw]
				else:
					pass
					#result.append(None)
			acc_ratio=float(len(result))/float(len(d_list))

		target_hit=False
		if target_ratio>acc_ratio-0.05 and target_ratio<acc_ratio+0.05:
			target_hit=True

		#if cycles==maxgenerations-1 or target_hit:
		if target_hit:
			print '\n'
			break

		cycles+=1

	return [result, sel_paths, acc_ratio, cycles]

