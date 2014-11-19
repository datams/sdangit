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
import lpsolv as lp

####################################################################
########################## parameters ##############################
####################################################################

repeats				= 1
plot_enable			= False
number_of_demands		= 10
path_selection_criterion	= 'hops'
graph_type			= 'deight'
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

	# get working copy of graph
	G_updated=copy.deepcopy(G)

	# keep track of plots
	plot_pool=gf.plot_pool()

	# plot original graph
	#[plot_pngs, plot_counter] = gf.ppng(G_updated, None, plot_pngs, plot_counter, 1, plot_enable)
	plot_pool.plot(G_updated, None, 1, plot_enable)

	# counters	
	number_of_rerouting_attempts=0
	number_of_rerouting_success=0

	# create all demands
	d_list=[]
	for k in range(number_of_demands):
		temp_dem = dem.demand(G.nodes(),bw_variants,lat_variants)
		temp_dem.make_choice()
		d_list.append(temp_dem)
		# 4Debug: print demands
		# print 'demand '+str(k)+': '+str(d_list[k].source)+' ==> '+str(d_list[k].target)

	# gurobi solver
	print '\n\nRun Gurobi Solver \n'
	print '########################'
	[lp_result,lp_accepted,lp_rejected,lp_ratio,lp_x, lp_P]=lp.solve(G,d_list)
	print '########################'
	print '\nGurobi Solver complete\n'

	i = 0
	while(True):
		print '\n \n########### \n'+str(i)+'th iteration'

		# try to find and allocate path in graph	
		[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[i],path_selection_criterion)

		# if successful, plot the chosen path
		if sel_path!=[]:
			plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
		
		##### CONSIDER REROUTE #####
		else:
			print 'No path found, looking now at previous allocations..\n'
			# check if demand could be allocated in empty graph
			path_pack_in_empty_graph=gf.shortest_p(G,d_list[i].get_source(),d_list[i].get_target(),d_list[i].get_lat())
			
			##### D_N NOT POSSIBLE EVER #####
			if path_pack_in_empty_graph == []:
				# demand can never be allocated
				print 'There is really no path for this demand, no chance!'

			else:
				#### FIND D_N TO REROUTE #####
				# plot d_n e.g. the current demand, which no path could be found for
				plot_pool.plot(G_updated, d_list[i], 1, plot_enable)

				# calculate best path p_n for d_n in empty graph
				optimal_path = gf.select_path(path_pack_in_empty_graph, path_selection_criterion)
				print 'The best path in the empty graph would be: '+str(optimal_path)

				# find the shoretst intersection (but it must intersect! thresh=1) path of optimal path with previous allocated paths p_u (according to d_u)			
				shortest_intersect=gf.check_setintersect(optimal_path, gf.sel_paths(d_list).values(),1)
				print 'having the shortest intersection path: of optimal path with previous allocated paths p_u (according to d_u) '+str(shortest_intersect)

				# if intersections found, try to reroute
				if shortest_intersect!=[]:

					# find critical (corresponding) demand
					for k in range(len(d_list)):
						if d_list[k].path == shortest_intersect:			
							d_u=k

					# look for paths for d_u that do not intersect with optimal_path
					d_u_paths=gf.pack2p(d_list[d_u].paths_pack)
					# remove already taken path
					d_u_paths.pop(d_u_paths.index(d_list[d_u].path))

					#### REROUTE #####
					if len(d_u_paths)>0:
						print 'corresponds to demand number: '+str(d_u)+' to the demand: '+str(d_list[d_u].source)+' ==> '+str(d_list[d_u].target)
						print 'which has the following alternative paths stored: '+str(d_u_paths)
						p_u=gf.check_setintersect(optimal_path, d_u_paths,0)
						print 'the least intersecting with p_n of d_n is '+str(p_u)

						# plot path to be deallocated
						plot_pool.plot(G_updated, d_list[d_u], 2, plot_enable)
						number_of_rerouting_attempts+=1
						# store old d_u path
						old_p_u=d_list[d_u].path
						# deallocate d_u
						[G_updated] = gf.dealloc(G_updated, d_list[d_u])
						# plot un-allocated graph
						plot_pool.plot(G_updated, None, 2, plot_enable)
						# allocate d_u with new path p_u
						print 'allocate d_u with new path p_u: '+str(p_u)
						[G_updated, sel_path] = gf.alloc_p(G_updated, d_list[d_u], p_u)

						# check if it was possible to allocate p_u without having negative bw
						if sel_path!=[]:
							print 'successful rerouting of p_u'
							# plot d_u with p_u allocated path
							plot_pool.plot(G_updated, d_list[d_u], 3, plot_enable)
					
							# try to allocate d_n
							[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[i],path_selection_criterion)
							if paths_pack!=[]:
								number_of_rerouting_success+=1
								print 'successful routing of p_n'
							else:
								print 'not possible to allocate p_n'
								print 'roll back d_u'
								[G_updated, sel_path] = gf.alloc_p(G_updated, d_list[d_u], old_p_u)
								plot_pool.plot(G_updated, d_list[d_u], 3, plot_enable)
							# plot d_n
							plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
						#### REVERT IF NO SUCCESS aber auch nur dann, wenn nicht etwa die priority hoeher ist bei d_n!! #####
						else:
							print 'rerouting was not possible, p_u was not allocatable'
							print 'roll back d_u'
							[G_updated, sel_path] = gf.alloc_p(G_updated, d_list[d_u], old_p_u)
							plot_pool.plot(G_updated, d_list[d_u], 3, plot_enable)
				else:
					print 'there was no rerouting alternative'


							
		i+=1
		if i==number_of_demands or number_of_rerouting_success>0:
			break
	
	# print out result stats
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
	gf.util_histo(G, G_updated, plot_enable)
	print 'sel path book:\n'+str(gf.sel_paths(d_list))


	# plot
	if plot_enable:
		os.system('convert ' + plot_pool.plot_pngs + ' +append topo.png')
		os.system('rm ' + plot_pool.plot_pngs)
		os.system('eog topo.png')

	
# print out stats for repeats
if repeats>1:
	print '\n \n \nnumber of rerouting attempts: '+str(number_of_rerouting_attempts_pool)
	print '\navg acceptance ratio: '+str(sum(acceptance_ratio_pool)/len(acceptance_ratio_pool))
	if len(successful_rerouting_fraction_pool)>0:
		print '\navg Successful rerouting fraction: '+str(sum(successful_rerouting_fraction_pool)/len(successful_rerouting_fraction_pool))
	

