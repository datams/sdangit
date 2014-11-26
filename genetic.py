##### imports #####
import demand as dem
import customGraph as gc
import graphFunctions as gf
import random
import copy

def gen_rand_index(d_list, level):
	variants=range(len(d_list))
	rand_index=random.sample(set(variants), level)
	return rand_index

def alloc_gen(G, sel_path, bw):
	G_updated=copy.deepcopy(G)
	G_updated=gf.update_edges(G_updated, sel_path, bw)
	if gf.minimum_bw(G_updated)<0:	
		success=True
	else:
		success=False
		G_updated=G
	return [G_updated, success]

def rate(G, d_list, genome):
	G_updated=copy.deepcopy(G)
	counter=0
	for i in range(len(d_list)):
		if genome[i]!=None:
			possible=d_list[i].paths_pack
			path=random.choice(gf.pack2p(possible))
			[G_updated, success] =  alloc_gen(G_updated, path, d_list[i].bw)
			if success == True:
				counter+=1		

def mutate(genome,d_list,level):
	rand_index=gen_rand_index(d_list, level)
	for i in rand_index:
			possible=d_list[i].paths_pack
			if possible!=[]:
				gen=random.choice(gf.pack2p(possible))
				genome[i]=gen
			else:
				genome[i]=None
	return genome

def evolution(G,d_list):
	for i in range(len(d_list)):
		pathpack=gf.shortest_p(G,d_list[i].source,d_list[i].target,d_list[i].lat)
		d_list[i].set_paths_pack(pathpack)

	# Produce Random Start Genome [selection_for_d1, selection_for_d2, selection_for_d3, ...]
	genome=[]
	for i in range(len(d_list)):
		genome.append(None)

	genome=mutate(genome,d_list, 1)

	# For number of iterations:
	for i in range(500):
		old_rating = rate(G, d_list, genome)	
		new_genome = mutate(genome, d_list, 1)
		new_rating = rate(G, d_list, new_genome)
		if new_rating>old_rating:
			genome=new_genome

	return genome
