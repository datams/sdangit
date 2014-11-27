##### imports #####
import demand as dem
import customGraph as gc
import graphFunctions as gf
import random
import copy


class genome:
    def __init__(self, d_list):
	self.d_list=d_list
	self.size=len(d_list)
	self.list = []
	for k in range(self.size):
		self.list.append(None)

    def randpos(self, level):
	# generates a list of level-many positions in genome
	variants=range(self.size)
	randpos=random.sample(set(variants), level)
	return randpos

    def mutate(self,level):
    	# mutates a genome on level-many positions if possible
    	randpos=self.randpos(level)
    	for i in randpos:
    		gen_pool=self.d_list[i].paths_pack
	if gen_pool!=[]:
		new_gen=random.choice(gf.pack2p(gen_pool))
		self.list[i]=new_gen
	return self

    # reports back the number of allocated paths with a given genome
    def rate(self, G):
	G_updated=copy.deepcopy(G)
	counter=0
	for i in range(self.size):
		if self.list[i]!=None:
			[G_updated, success] = alloc_gen(G_updated, self.list[i], self.d_list[i].bw)
			if success == True:
				counter+=1
	return counter


# tries to allocate a selected path with a given bw and reports if it was possible
def alloc_gen(G, sel_path, bw):
	G_updated=copy.deepcopy(G)
	G_updated=gf.update_edges(G_updated, sel_path, bw)
	if gf.minimum_bw(G_updated)>0:	
		success=True
	else:
		success=False
		G_updated=G
	return [G_updated, success]

# runs multiple evolution iterations in order to find the best genome
def evolution(G,d_list):
	for i in range(len(d_list)):
		pathpack=gf.shortest_p(G,d_list[i].source,d_list[i].target,d_list[i].lat)
		d_list[i].set_paths_pack(pathpack)

	a=genome(d_list)
	a.mutate(1)

	# For number of iterations:
	for i in range(20):
		old_rating = a.rate(G)
		print 'a='+str(a.list)+' with rating: '+str(old_rating)
		if old_rating==len(d_list):
			break
		b = a.mutate(1)
		new_rating = b.rate(G)
		print 'b='+str(a.list)+' with rating: '+str(new_rating)
		if new_rating>old_rating:
			print 'take b as a'
			a=b
	return a.list
