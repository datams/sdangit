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
import greedy as gr

####################################################################
########################## parameters ##############################
####################################################################

repeats				= 1
plot_enable			= True
show_enable			= False
gr_enable			= False
lp_enable			= False
cli				= True
cli_lp				= True
number_of_demands		= 8
path_selection_criterion	= 'hops'
graph_type			= 'deight'
bw_variants			= [1,3,5]
lat_variants			= [1,2,4]


####################################################################
######################## main program ##############################
####################################################################

# instantiate a graph
G=customGraph.make(graph_type)
G=G.to_directed()

# clear terminal
print chr(27) + "[2J"

# delete pngs (do not do when eog always open)
if cli==False:
	os.system('rm *.png')

# over repeats stats vars
acceptance_ratio_pool=[]
successful_rerouting_fraction_pool=[]
number_of_rerouting_attempts_pool=0

for j in range(repeats):

	# get working copy of graph
	G_updated=copy.deepcopy(G)

	# keep track of plots
	plot_pool=gf.plot_pool('topo')

	# plot original graph
	plot_pool.plot(G_updated, None, 1, plot_enable)

	# counters	
	number_of_rerouting_attempts=0
	number_of_rerouting_success=0

	# create all demands
	if lp_enable or gr_enable:
		d_list=[]
		for k in range(number_of_demands):
			temp_dem = dem.demand(G.nodes(),bw_variants,lat_variants)
			temp_dem.make_choice()
			d_list.append(temp_dem)
			# 4Debug: print demands
			print 'demand '+str(k)+': '+str(d_list[k].source)+' ==> '+str(d_list[k].target)
	# cli mode	
	if cli:
		os.system('eog topo0.png &')
		d_list=[]
		i=0
		number_of_demands=0
		print 'Please open png file'
		leave=False
		while(True):
			print '\nPlease choose from nodes '+str(G.nodes())
			while(True):
				f=input('Please enter from node (888 for ending): ')
				if f in G.nodes() or f==888: break
				print 'Please enter a valid node'
			if f==888:
				leave=True
				break
			if leave==True: break
			while(True):
				t=input('Please enter to node: ')
				if t in G.nodes(): break
				print 'Please enter a valid node'
			bwreq=input('Please enter bw req: ')
			latreq=input('Please enter lat req: ')
			# create demand
			temp_dem = dem.demand(G.nodes(),None,None)
			temp_dem.make_choice_concrete(f,t,bwreq,latreq)
			d_list.append(temp_dem)
			number_of_demands+=1
			[G_updated, plot_pool, number_of_demands, number_of_rerouting_attempts, number_of_rerouting_success]=\
			gr.finder(G, G_updated, d_list, number_of_demands, i, plot_pool, path_selection_criterion,\
			number_of_rerouting_attempts, number_of_rerouting_success, plot_enable)
			i+=1

	# greedy solver
	if gr_enable:
		i = 0
		while(True):
			print '\n \n########### \n'+str(i)+'th iteration'

			[G_updated, plot_pool, number_of_demands, number_of_rerouting_attempts, number_of_rerouting_success]=\
			gr.finder(G, G_updated, d_list, number_of_demands, i, plot_pool, path_selection_criterion,\
			number_of_rerouting_attempts, number_of_rerouting_success, plot_enable)
							
			i+=1
			if i==number_of_demands:
				break
	
		# print out result stats
		print '\n\n\n%%%%% END STATS %%%%%\n'
		print 'Total demands: '+str(number_of_demands)
		acceptance_counter = sum([d.x for d in d_list])
		print 'Allocated demands: '+str(acceptance_counter)
		print 'Rejected demands: '+str(number_of_demands-acceptance_counter)
		print 'Rerouting attempts: '+str(number_of_rerouting_attempts)
		number_of_rerouting_attempts_pool+=number_of_rerouting_attempts
		print 'Successful reroutings '+str(number_of_rerouting_success)
		if number_of_rerouting_attempts>0:
			print 'Successful rerouting fraction '+str(float(number_of_rerouting_success)/float(number_of_rerouting_attempts))
			successful_rerouting_fraction_pool.append(float(number_of_rerouting_success)/float(number_of_rerouting_attempts))
		acceptance_ratio = float(acceptance_counter)/float(number_of_demands)
		acceptance_ratio_pool.append(acceptance_ratio)
		print 'Acceptance ratio: '+str(acceptance_ratio*100)+'%'
		print 'Link utilization: '+str(gf.link_util(G,G_updated))
		# saves link utilization to l_util.png
		gf.util_histo(G, G_updated, plot_enable)
		print 'sel path book:\n'+str(gf.sel_paths(d_list))

	# gurobi solver
	if lp_enable or cli_lp:
		print '\n\nRun Gurobi Solver \n'
		print '########################'
		[lp_result,lp_sel_paths,lp_accepted,lp_rejected,lp_ratio,lp_x]=lp.solve(G,d_list)
		print '########################'
		print '\nGurobi Solver complete\n'
		

	# print out gurobi stats
	if lp_enable or cli_lp:
		print '\nGurobi accepted '+str(lp_accepted)
		print 'Gurobi acceptance ratio '+str(lp_ratio*100)+'%'
		print 'Gurobi sel path book:\n'+str(lp_sel_paths)+'\n'

	
	# print comparison
	if lp_enable and gr_enable:
		print 'lp is '+str(lp_ratio*100-acceptance_ratio*100)+'% points better than greedy'
		greedy_al=list(gf.sel_paths(d_list).keys())
		lp_al=list(lp_sel_paths.keys())
		for re in lp_al:
			if not re in greedy_al:
				print str(re)+' is not in greedy but in LP'

	# plot
	if plot_enable:
		# plot greedy
		if gr_enable:
			os.system('convert ' + plot_pool.plot_pngs + ' +append '+str(plot_pool.prefix)+'.png')
			os.system('rm ' + plot_pool.plot_pngs)
		# plot lp
		if lp_enable:
			lp_plot_pool=gf.plot_pool('lopo')
			G_lp=copy.deepcopy(G)
			lp_plot_pool.plotpa(G_lp, None, 1, plot_enable)
			for key in (lp_sel_paths):
				lp_p=lp_sel_paths[key][0]
				lp_bw=lp_sel_paths[key][1]
				G_lp = gf.update_edges(G_lp, lp_p, lp_bw)
				lp_plot_pool.plotpa(G_lp, lp_p, 1, plot_enable)
			os.system('convert ' + lp_plot_pool.plot_pngs + ' +append '+str(lp_plot_pool.prefix)+'.png')
			os.system('rm ' + lp_plot_pool.plot_pngs)
			os.system('convert ' + str(plot_pool.prefix)+'.png '+str(lp_plot_pool.prefix)+'.png -append total.png')

	# show plot	
	if show_enable and plot_enable and gr_enable and lp_enable:
			os.system('eog total.png')

# print out stats for repeats
if repeats>1 and gr_enable:
	print '\n \n \nnumber of rerouting attempts: '+str(number_of_rerouting_attempts_pool)
	print '\navg acceptance ratio: '+str(sum(acceptance_ratio_pool)/len(acceptance_ratio_pool))
	if len(successful_rerouting_fraction_pool)>0:
		print '\navg Successful rerouting fraction: '+str(sum(successful_rerouting_fraction_pool)/len(successful_rerouting_fraction_pool))
	

