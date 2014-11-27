##### imports #####
import demand as dem
import customGraph as gc
import graphFunctions as gf
import random
import copy

# todo for parallels
class population:
    def __init__(self):
	self.individuals=[]
	self.rankings={}

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
				los=[0,0,0,0,0,0,0,0,1,1]
				leer=random.choice(los)
				if leer==0:
					self.list[i]=new_gen
				else:
					self.list[i]=None
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
	return [counter,alloc_status]


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

# returns 1 with a percentage probability, else 0
def randb(percentage):
	los=[1]*percentage + [0]*(100-percentage)
	decision=random.choice(los)
	return decision

# runs multiple evolution iterations in order to find the best genome
def evolution(G,d_list):
	for i in range(len(d_list)):
		pathpack=gf.shortest_p(G,d_list[i].source,d_list[i].target,d_list[i].lat)
		d_list[i].set_paths_pack(pathpack)

	a=genome(d_list)
	a.mutate(1)

	# For number of iterations:
	cycles=0
	burst_start=50
	burst_duration=2
	while(True):
		if burst_start==0:
			mutationrate=4
			burst_duration-=1
			if burst_duration==0:
				burst_duration=4
				burst_start=50
			burst_start+=1
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
		burst_start-=1
		# reset after 200 iterations
		if cycles%200 == 0:
			a=genome(d_list)
		#print 'cycles: '+str(cycles)
		#print 'rating: '+str(a.rate(G)[0])
		# stop after 1000 iterations or when acceptance ratio 100%
		if cycles==1000 or new_rating==len(d_list):
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

	print 'Result: '+str(result)
	print 'Acceptance Rate: '+str(acc_ratio)
	return result
