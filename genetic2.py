##### imports #####
import demand as dem
import customGraph as gc
import graphFunctions as gf
import random
import copy

# a population contains a set of individuals (genomes) and can rank them
class population:
    def __init__(self,G,d_list,pop_size):
	self.G=G
	self.d_list=d_list
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
		self.individuals[j].mutate(level)

    # determine the fitness for all genomes and store to fitness dict
    def rateall(self):
	for i in range(len(self.individuals)):
		self.fitness[i]=self.individuals[i].rate(self.G)[0]

    # determine the ranking based on fitness
    def rank(self):
	self.ranking=sorted(self.fitness, key=self.fitness.get, reverse=True)

    # produce the next generation (keep nr 1&2, privilege nr 3&4 by having 2 children each)
    def fork(self,level):
	new_individuals=[]
	for l in range(len(self.individuals)):
		index=self.ranking[l]
		if l==0 or l==1:	
			new_individuals.append(self.individuals[index])
		elif l==2 or l==3:
			new_individuals.append(self.individuals[index].mutate(level))
			new_individuals.append(self.individuals[index].mutate(level))
		elif l<len(self.individuals):
			new_individuals.append(self.individuals[index].mutate(level))
	self.individuals=new_individuals

    # return best genome of population
    def best_genome(self):
	index=self.ranking[0]
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
    def mutate(self,level):
	# get random positions in genome
    	randpos=self.randpos(level)
    	for i in randpos:
		# for a given probability (percentage) delete the gen to None
		if randb(10)==1:
			self.list[i]=None
		else:
			# get gen pool of possibilities for genome position
	    		gen_pool=self.d_list[i].paths_pack
			if gen_pool!=[]:
				new_gen=random.choice(gf.pack2p(gen_pool))
				self.list[i]=new_gen
	return self

    # reports back the number of allocated paths with a given genome
    def rate(self, G):
	G_updated=copy.deepcopy(G)
	counter=0
	alloc_status=[]
	for i in range(self.size):
		alloc_status.append(None)
		if self.list[i]!=None:
			[G_updated, success] = alloc_gen(G_updated, self.list[i], self.d_list[i].bw)
			if success == True:
				counter+=1
				alloc_status[i]=True
			elif success == False:
				alloc_status[i]=None
	used_bw=bw_consum(G, G_updated)
	if used_bw<=0:
		fitness=0
	else:
		fitness=0.9*float(counter)+0.1/used_bw
	#print 'fitness: '+str(fitness)
	return [fitness,alloc_status]

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


# runs multiple evolution iterations in order to find the best genome
def paraevolution(G,d_list):
	# determine all feasible paths
	for i in range(len(d_list)):
		pathpack=gf.shortest_p(G,d_list[i].source,d_list[i].target,d_list[i].lat)
		d_list[i].set_paths_pack(pathpack)

	# pop size should at least be 5 (because of fork privileges)
	pop_size=8
	p=population(G,d_list,pop_size)
	p.mutall(1)

	# set burst duration
	burst_duration=2
	# For number of iterations:
	cycles=0
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

		if cycles==12:
			selection=p.best_genome()
			print 'selection rating: '+str(selection.rate(G))
			result=[]
			alloc_counter=0
			# only show the allocatable paths as a result
			for j in range(len(selection.list)):
				if selection.list[j]:
					result.append(selection.list[j])
					alloc_counter+=1
				else:
					pass
					#result.append(None)
			acc_ratio=float(alloc_counter)/float(len(selection.list))*100
			break
		cycles+=1
		p.fork(mutationrate)

	print '\nRun Genetic Algorithm'
	print 'Acceptance ratio: '+str(acc_ratio)+'%'
	print 'Result: '+str(result)
	print 'Iterations: '+str(cycles)

	return result




# runs multiple evolution iterations in order to find the best genome
def evolution(G,d_list):
	for i in range(len(d_list)):
		pathpack=gf.shortest_p(G,d_list[i].source,d_list[i].target,d_list[i].lat)
		d_list[i].set_paths_pack(pathpack)

	a=genome(d_list)
	a.mutate(1)

	# set burst duration
	burst_duration=2
	# For number of iterations:
	cycles=0
	burst_timer=burst_duration
	bursting=False
	while(True):
		if cycles%50 == 0 or bursting:
			bursting=True
			mutationrate=4
			burst_timer-=1
			if burst_timer<=0:
				burst_timer=burst_duration
				bursting=False
		else:
			mutationrate=1
		old_rating = a.rate(G)[0]
		#print 'a='+str(a.list)+' with rating: '+str(old_rating)
		b = a.mutate(mutationrate)
		new_rating = b.rate(G)[0]
		#print 'b='+str(a.list)+' with rating: '+str(new_rating)
		if new_rating>old_rating:
			#print 'take b as a'
			a=b
		cycles+=1
		# reset after n iterations
		#if cycles%400 == 0:
			#a=genome(d_list)
		#print 'cycles: '+str(cycles)
		#print 'rating: '+str(a.rate(G)[0])
		# stop after 1000 iterations or when acceptance ratio 100%
		if cycles==200 or new_rating==len(d_list):
			selection=a.rate(G)[1]
			result=[]
			alloc_counter=0
			# only show the allocatable paths as a result
			for j in range(len(selection)):
				if selection[j]:
					result.append(a.list[j])
					alloc_counter+=1
				else:
					result.append(None)
			acc_ratio=float(alloc_counter)/float(len(selection))*100
			break

	print '\nRun Genetic Algorithm'
	print 'Acceptance ratio: '+str(acc_ratio)+'%'
	print 'Result: '+str(result)
	print 'Iterations: '+str(cycles)

	return result
