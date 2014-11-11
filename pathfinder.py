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
lat_variants			= [10]


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
				# d_n the new demand, which no path could be found for
				# plot d_n
				[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[i], plot_pngs, plot_counter, 1, plot_enable)

				# Calculate best path p_n for d_n in empty graph
				print 'The best path in the empty graph would be:'
				# determine optimal path
				optimal_path = gf.select_path(path_pack_in_empty_graph, path_selection_criterion)
				print optimal_path

				# Find least intersecting demand
				# find intersections of optimal path with previous allocations				
				print 'which would have all the following intersections: '
				intersect_dict=gf.check_setintersection(optimal_path, sel_paths_book.values())
				print intersect_dict
				if intersect_dict!={}:
					# find critical intersection path
					print 'although the critical one is: '+str(intersect_dict[max(intersect_dict)])
					critical_intersect = intersect_dict[min(intersect_dict)]
					# find according demand
					print 'therefore rerouting the path from '+str(critical_intersect[0])+' to '+str(critical_intersect[-1])
					d_u=demand_dict[critical_intersect[0],critical_intersect[-1]]
					# Look for path for d_u that does not intersect with optimal_path
					d_u_paths=[path for (path,lat,hops) in d_list[d_u].paths_pack]
					d_u_intersect_paths=gf.check_setintersection(optimal_path, d_u_paths)
					# if there are multiple such paths, take the shortest p_u for d_u
					# if there is no such paths, take the least intersecting one p_u for d_u
					p_u = min(d_u_intersect_paths)
					# deallocate d_u
					# plot path to un-allocated
					[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[d_u], plot_pngs, plot_counter, 2, plot_enable)
					number_of_rerouting_attempts+=1
					# un-allocate
					[G_updated, sel_paths_book] = gf.unalloc(G_updated, d_list[d_u], sel_paths_book)
					# plot un-allocated graph
					[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[d_u], plot_pngs, plot_counter, 2, plot_enable)
					# allocate d_u with new path p_u
					print 'allocate d_u with new path p_u'
					[G_updated, sel_path, sel_paths_book] = gf.alloc_p(G_updated, d_list[d_u], p_u, sel_paths_book)
					# plot p_u with p_u allocated path
					[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[d_u], plot_pngs, plot_counter, 1, plot_enable)
					# try to allocate d_n
					[G_updated, paths_pack, sel_path, sel_paths_book]=gf.alloc(G_updated,d_list[i],path_selection_criterion, sel_paths_book)
					if paths_pack!=[]:
						number_of_rerouting_success+=1	
					# plot d_n
					[plot_pngs, plot_counter] = gf.ppng(G_updated, d_list[d_u], plot_pngs, plot_counter, 1, plot_enable)



							
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
	

