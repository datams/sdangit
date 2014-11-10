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
number_of_demands		= 7
path_selection_criterion	= 'lat'
graph_type			= 'eight'
bw_variants			= [1]
lat_variants			= [16]


####################################################################
######################## main program ##############################
####################################################################

# instantiate a graph
G=customGraph.make(graph_type)

# delete pngs and clear terminal
os.system('rm *.png')
print chr(27) + "[2J"

# over repeats stats vars
acceptance_ratio_pool=[]
successful_rerouting_fraction_pool=[]
number_of_rerouting_attempts_pool=0

for j in range(repeats):

	# dict for all sel paths
	sel_paths_book={}

	# get working copy of graph
	G_updated=copy.deepcopy(G)

	# keep track of plots
	plot_counter=0
	plot_pngs=''

	# plot original graph
	[plot_pngs, plot_counter] = gf.ppng(G_updated, None, plot_pngs, plot_counter, 1, plot_enable)

	# counters	
	number_of_rerouting_attempts=0
	number_of_rerouting_success=0

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

		# allocate path in graph	
		[G_updated, paths_pack, sel_path, sel_paths_book]=gf.alloc(G_updated,d_list[i],path_selection_criterion, sel_paths_book)

		# plot the chosen path
		if sel_path!=[]:
			[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[i], plot_pngs, plot_counter, 1, plot_enable)
		else:
			print 'no path found, looking now at previous allocations..\n'
			path_pack_in_empty_graph=gf.shortest_p(G,d_list[i].get_source(),d_list[i].get_target(),d_list[i].get_lat())
			if path_pack_in_empty_graph == []:
				print 'there is really no path for this demand, no chance!'
			else:
				# Go through path book of least intersectioning demand d_u and reroute to the shortest non-intersecting path
				# if there is none: reroute d_u to the least intersecting one
				# try now to allocate d_n
				# try to allocate d_u again, if it does not succeed, revert d_u and do not allocate d_n

				# Only allocate new demand d_n if the old d_u can be allocated again
				# demand cannot be allocated, what could be done?
				# plot hard demand
				[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[i], plot_pngs, plot_counter, 1, plot_enable)
				print 'The best path in the empty graph would be:'
				# determine optimal path				
				optimal_path = gf.select_path(path_pack_in_empty_graph, path_selection_criterion)
				print optimal_path
				# find intersections of optimal path with previous allocations				
				print 'which would have all the following intersections: '
				intersect_dict=gf.check_setintersection(optimal_path, sel_paths_book.values())
				print intersect_dict
				if intersect_dict!={}:
					# find worst intersection path
					print 'although the worst one is: '+str(intersect_dict[max(intersect_dict)])
					worst_intersect = intersect_dict[min(intersect_dict)]
					# find according demand
					print 'therefore rerouting the path from '+str(worst_intersect[0])+' to '+str(worst_intersect[-1])
					to_reroute=demand_dict[worst_intersect[0],worst_intersect[-1]]
					# plot path to un-allocated
					[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[to_reroute], plot_pngs, plot_counter, 2, plot_enable)
					# un-allocate
					[G_updated, sel_paths_book] = gf.unalloc(G_updated, d_list[to_reroute], sel_paths_book)
					# plot un-allocated graph
					[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[to_reroute], plot_pngs, plot_counter, 2, plot_enable)
					# allocate current demand
					number_of_rerouting_attempts+=1
					print 'allocate current demand'
					[G_updated, paths_pack, sel_path, sel_paths_book]=gf.alloc(G_updated,d_list[i],path_selection_criterion, sel_paths_book)
					# plot current demand allocated path
					[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[i], plot_pngs, plot_counter, 1, plot_enable)
					print  'allocate old demand again'
					[G_updated, paths_pack, sel_path, sel_paths_book]=gf.alloc(G_updated,d_list[to_reroute],path_selection_criterion, sel_paths_book)
					if paths_pack!=[]:
						number_of_rerouting_success+=1				
					# plot old demand allocated again
					[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[to_reroute], plot_pngs, plot_counter, 1, plot_enable)
							
		i+=1
		if i==number_of_demands:
			break
	
	# print out result stats154
	print '\n\n\n%%%%% END STATS %%%%%\n'
	acceptance_counter = sum([d.x for d in d_list])
	print 'Allocated demands: '+str(acceptance_counter)
	print 'Rejected demands: '+str(number_of_demands-acceptance_counter)
	print 'Rerouting attempts: '+str(number_of_rerouting_attempts)
	number_of_rerouting_attempts_pool+=number_of_rerouting_attempts
	print 'Successful reroutings '+str(number_of_rerouting_success)
	if number_of_rerouting_attempts>0:
		print 'Successful rerouting fraction '+str(float(number_of_rerouting_success)/float(number_of_rerouting_attempts))
		successful_rerouting_fraction_pool.append(float(number_of_rerouting_success)/float(number_of_rerouting_attempts))
	print 'Total demands: '+str(number_of_demands)
	acceptance_ratio = float(acceptance_counter)/float(number_of_demands)
	acceptance_ratio_pool.append(acceptance_ratio)
	print 'Acceptance ratio: '+str(acceptance_ratio*100)+'%'
	print 'Link utilization: '+str(gf.link_util(G,G_updated))
	# saves link utilization to l_util.png
	os.system('rm l_util.png')
	gf.util_histo(G, G_updated)
	print 'sel path book:\n'+str(sel_paths_book)

	# plot
	if plot_enable:
		os.system('convert '+plot_pngs+' +append topo.png')
		os.system('rm '+plot_pngs)
		os.system('eog topo.png')

	
	

if repeats>1:
	print '\n \n \nnumber of rerouting attempts: '+str(number_of_rerouting_attempts_pool)
	print '\navg acceptance ratio: '+str(sum(acceptance_ratio_pool)/len(acceptance_ratio_pool))
	if len(successful_rerouting_fraction_pool)>0:
		print '\navg Successful rerouting fraction: '+str(sum(successful_rerouting_fraction_pool)/len(successful_rerouting_fraction_pool))
	

