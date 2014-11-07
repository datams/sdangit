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
import demand as dem
import customGraph
import graphFunctions as gf

####################################################################
########################## parameters ##############################
####################################################################

repeats				= 1
plot_enable			= True
number_of_demands		= 8
path_selection_criterion	= 'lat'
graph_type			= 'eight'
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
	
	# create all demands
	d_list=[]
	demand_dict={}
	for k in range(number_of_demands):
		temp_dem = dem.demand(G.nodes(),bw_variants,lat_variants)
		temp_dem.make_choice()
		d_list.append(temp_dem)
		demand_dict[(temp_dem.get_source(),temp_dem.get_target())]=k

	
	i = 0
	while(True):
		print '\n \n########### \n'+str(i)+'th iteration'
	
		# copy of graph for pruning and updating
		G_prune=G_updated
		G_updated=copy.deepcopy(G_prune)

		print '\nDemand: '
		print 'Path to find: '+str(d_list[i].source)+' ==> '+str(d_list[i].target)
		print "bw req: "+str(d_list[i].bw)
		print "lat req: "+str(d_list[i].lat)

		# pruning
		G_prune=gf.prune_bw(G_prune, d_list[i].get_bw())

		# path finding
		paths_pack = gf.shortest_p(G_prune,d_list[i].get_source(),d_list[i].get_target(),d_list[i].get_lat())
		print '\nPaths (with lat.) found: \n'+str(paths_pack)

		if paths_pack!=[] and paths_pack!=None:
			# store found paths in dictionary book
			path_book[(d_list[i].get_source(),d_list[i].get_target())]=paths_pack
			# store found paths in demand
			d_list[i].set_paths_pack(paths_pack)
			# path selection
			selected_path = gf.select_path(paths_pack, path_selection_criterion)
			# store selected path in dictionary book
			selected_paths_book[(d_list[i].get_source(),d_list[i].get_target())]=selected_path
			# store selected path in demand
			d_list[i].set_allocated()
			d_list[i].set_path(selected_path)
			# update graph
			G_updated=gf.update_edges(G_updated, selected_path, d_list[i].get_bw())
			# plot the chosen path
			if plot_enable:
				plot_pngs+=gf.plot_graphviz(G_updated,d_list[i],selected_path,plot_counter)+' '
			# count the allocation
			acceptance_counter+=1
		else:
			print 'no path found, looking now at previous allocations..\n'
			path_pack_in_empty_graph=gf.shortest_p(G,d_list[i].get_source(),d_list[i].get_target(),d_list[i].get_lat())
			if path_pack_in_empty_graph == []:
				print 'there is really no path for this demand, no chance!'
			else:
				print 'The best path in the empty graph would be:'
				optimal_path = gf.select_path(path_pack_in_empty_graph, path_selection_criterion)
				print optimal_path
				print 'which would have all the following intersections: '
				intersect_dict=gf.check_setintersection(optimal_path, selected_paths_book.values())
				print intersect_dict
				print 'although the worst one is: '+str(intersect_dict[max(intersect_dict)])
				worst_intersect = intersect_dict[max(intersect_dict)]
				print 'therefore please consider rerouting the path from '+str(worst_intersect[0])+' to '+str(worst_intersect[-1])
				to_reroute=demand_dict[worst_intersect[0],worst_intersect[-1]]
				print 'which would be demand nr: '+str(to_reroute)
				# nehme den betroffenen demand, setze ihn auf unallocated
				# update den graphen mit minus bw
				# alloziere den neuen demand?
				# alloziere den alten demand? den kann man per demand dict wieder finden und mit i kann man steuern was behandelt wird
			if plot_enable:
				plot_pngs+=gf.plot_graphviz(G_updated,d_list[i],None,plot_counter)+' '

		plot_counter+=1
		i+=1
		if i==number_of_demands:
			break

		
	# print out result stats
	print '\n\n\n%%%%% END STATS %%%%%'
	#print 'path_book:\n'+str(path_book)
	print 'Allocated demands: '+str(acceptance_counter)
	print 'Rejected demands: '+str(number_of_demands-acceptance_counter)
	print 'Total demands: '+str(number_of_demands)
	acceptance_rate = float(acceptance_counter)/float(number_of_demands)
	print 'Acceptance rate: '+str(acceptance_rate*100)+'%'
	print 'Link utilization: '+str(gf.link_util(G,G_updated))
	print 'selected path book:\n'+str(selected_paths_book)

	# plot
	if plot_enable:
		os.system('convert '+plot_pngs+' +append topo.png')
		os.system('rm '+plot_pngs)
		os.system('eog topo.png')


	acceptance_rate_pool.append(acceptance_rate)

if repeats>1:
	print '\navg acceptance rate: '+str(sum(acceptance_rate_pool)/len(acceptance_rate_pool))


