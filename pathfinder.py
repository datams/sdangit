#!/usr/bin/env python

####################################################################
########################## imports #################################
####################################################################

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import networkx as nx
import random
import copy
#import matplotlib.cm as cmx
#import numpy as np
import pygraphviz
import os
import operator
import demand
import customGraph
import graphFunctions as gf

####################################################################
########################## parameters ##############################
####################################################################

repeats				= 50
plot_enable			= False
number_of_demands		= 10
path_selection_criterion	= 'hops'
graph_type			= 'srg'
bw_variants			= [1]
lat_variants			= [10]

####################################################################
######################## main program ##############################
####################################################################

# instantiate a graph
G=customGraph.make(graph_type)

# delete pngs and clear terminal
os.system('rm *.png')
print chr(27) + "[2J"

acceptance_rate_pool=[]
for j in range(repeats):

	# dict for all paths found and selected ever
	path_book={}
	selected_paths_book={}

	# dict for all paths found ever
	path_book={}

	# get working copy of graph
	G_updated=copy.deepcopy(G)

	# keep track of plots
	plot_counter=0
	plot_pngs=''

	# plot original graph
	plot_pngs+=gf.plot_graphviz(G_updated,None,None,plot_counter)+' '
	plot_counter+=1
	acceptance_counter=0

	for iteration in range(number_of_demands):
		print '\n \n########### \n'+str(iteration)+'th iteration'
	
		# copy of graph for pruning and updating
		G_prune=G_updated
		G_updated=copy.deepcopy(G_prune)

		# instantiate a demand
		d=demand.demand(G.nodes(),bw_variants,lat_variants)

		#d.make_choice_concrete(2,3)
		d.make_choice()

		# pruning
		G_prune=gf.prune_bw(G_prune, d.get_bw())

		# path finding
		paths_pack = gf.shortest_p(G_prune,d.get_source(),d.get_target(),d.get_lat())
		print '\nPaths (with lat.) found: \n'+str(paths_pack)

		if paths_pack!=[] and paths_pack!=None:
			# path selection
			selected_path = gf.select_path(paths_pack, path_selection_criterion)
			# store found paths in dictionary book
			path_book[(d.get_source(),d.get_target())]=paths_pack
			selected_paths_book[(d.get_source(),d.get_target())]=selected_path
			# update graph
			G_updated=gf.update_edges(G_updated, selected_path, d.get_bw())
			# plot the chosen path
			if plot_enable:
				plot_pngs+=gf.plot_graphviz(G_updated,d,selected_path,plot_counter)+' '
			# count the allocation
			acceptance_counter+=1
		else:
			print 'no path found'
			if plot_enable:
				plot_pngs+=gf.plot_graphviz(G_updated,d,None,plot_counter)+' '

		plot_counter+=1

	print 'path_book:\n'+str(path_book)

	print '\n\nLink utilization: '+str(gf.link_util(G,G_updated))
	print '\nAllocated demands: '+str(acceptance_counter)
	print 'Rejected demands: '+str(number_of_demands-acceptance_counter)
	print 'Total demands: '+str(number_of_demands)
	acceptance_rate = float(acceptance_counter)/float(number_of_demands)
	print 'Acceptance rate: '+str(acceptance_rate*100)+'%'
	print 'selected path book:'+str(selected_paths_book)

	# plot
	if plot_enable:
		os.system('convert '+plot_pngs+' +append topo.png')
		os.system('rm '+plot_pngs)
		os.system('eog topo.png')


	acceptance_rate_pool.append(acceptance_rate)

print 'avg acceptance rate: '+str(sum(acceptance_rate_pool)/len(acceptance_rate_pool))


