#!/usr/bin/env python

####################################################################
######################## python imports ############################
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
import time

####################################################################
####################### modules imports ############################
####################################################################
import demand as dem
import customGraph
import graphFunctions as gf
import lpsolv as lp
import greedy as gr
import genetic2 as gen
import gen_param as gp

####################################################################
########################## parameters ##############################
####################################################################

mode='genetic_opt'

if mode=='ran':
	plot_enable			= False
	show_enable			= False
	gr_enable			= True
	lp_enable			= True
	cli				= False
	cli_lp				= False
	gen_enable			= False
	repeats				= 40
	number_of_demands		= 14
	path_selection_criterion	= 'hops'
	graph_type			= 'deight'
	bw_variants			= [1,2,4]
	lat_variants			= [4,8,10,20]

if mode=='cli':
	plot_enable			= True
	show_enable			= True
	gr_enable			= False
	lp_enable			= False
	cli				= True
	cli_lp				= True
	gen_enable			= False
	repeats				= 1
	number_of_demands		= 12
	path_selection_criterion	= 'hops'
	graph_type			= 'deight'
	bw_variants			= [1,2,3]
	lat_variants			= [4,8]

if mode=='genetic':
	plot_enable			= False
	show_enable			= False
	gr_enable			= False
	lp_enable			= True
	cli				= False
	cli_lp				= False
	gen_enable			= True
	repeats				= 1
	number_of_demands		= 15
	path_selection_criterion	= 'hops'
	graph_type			= 'srg'
	bw_variants			= [1,2,3]
	lat_variants			= [4,8]
	# pos. int population size (number of genomes in one generation)
	pop_size=15
	# pos. int maximum number of iterations resp. generations
	maxgenerations=15
	# decimal amount of number of high society genomes in a population
	clergy_size=0.2
	# pos. int (smaller than pop_size) number of children of high society genomes
	clergy_children=2
	# decimal amount of number of middle class genomes in a population
	nobility_size=0.2
	# pos. int (smaller than pop_size) number of children of middle class genomes
	nobility_children=2
	# pos. int (smaller than nr of demands) mutation rate at beginning
	start_mut=4
	# pos. int (smaller than nr of demands) mutation rate at the end
	end_mut=1
	# non-allocated choice probability percentage
	non_prob=10
	# weight of acceptance in fitness function		
	weight_ac=0.9

if mode=='genetic_opt':
	plot_enable			= False
	show_enable			= False
	gr_enable			= False
	lp_enable			= True
	cli				= False
	cli_lp				= False
	gen_enable			= True
	repeats				= 1
	number_of_demands		= 15
	path_selection_criterion	= 'hops'
	graph_type			= 'srg'
	bw_variants			= [1,2,3]
	lat_variants			= [4,8]
	min_gen_time=None

####################################################################
######################## main program ##############################
####################################################################

# instantiate a graph
G=customGraph.make(graph_type)
G=G.to_directed()

# clear terminal
print chr(27) + "[2J"

# delete pngs (do not do when eog always open)
os.system('rm *.png')

# over repeats stats vars
acceptance_ratio_pool=[]
successful_rerouting_fraction_pool=[]
number_of_rerouting_attempts_pool=0

# create all demands
bw_lowest=gf.minimum_bw(G)
bw_highest=gf.maximum_bw(G)

lat_lowest=gf.minimum_lat(G)*3
lat_highest=gf.maximum_lat(G)*20

print bw_lowest
print bw_highest
print lat_lowest
print lat_highest

if lp_enable or gr_enable or gen_enable:
	d_list=[]
	for k in range(number_of_demands):
		while(True):
			print 'Create demand Nr. '+str(k)
			# initialize demand
			temp_dem = dem.demand(G.nodes(),bw_variants,lat_variants)
			# make random choice
			#temp_dem.make_random_choice()
			temp_dem.make_total_random_choice(bw_lowest, bw_highest, lat_lowest, lat_highest)
			# check feasibility
			if gf.is_feasible(G,temp_dem,path_selection_criterion):
				d_list.append(temp_dem)
				break
		# 4Debug: print demands
		print 'demand '+str(k)+': '+str(d_list[k].source)+' ==> '+str(d_list[k].target)

if mode=='genetic_opt':
	gen_param=gp.gen_param()
	repeats=gen_param.size()
	best_param=None

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

	# cli mode	
	if cli:
		d_list=[]
		i=0
		number_of_demands=0
		print 'Please open png file'
		leave=False
		if show_enable:
			os.system('eog topo0.png &')
		while(True):
			print '\nAllocated demands'
			if len(d_list)>0:
				print gf.get_all_sel_paths(d_list)
			mode=input('remove=0, add=1, edit_state=2 leave=888: ')
			if mode==888:
				leave=True
				break
			if mode==0:
				d_remove=input('demand nr to remove: ')
				if d_remove < len(d_list):
					[G_updated]=gf.dealloc(G_updated, d_list[d_remove])
					temp=d_list.pop(d_remove)
					plot_pool.plot(G_updated, None, 2, plot_enable)
					i-=1
					print '\nAllocated demands'
					if len(d_list)>0:
						print gf.get_all_sel_paths(d_list)
			if mode==2:
				d_change=input('demand nr whose state should change: ')
				if d_change < len(d_list):
					action=input('block=1, unblock=0: ')
					if action==1:
						d_list[d_change].block()
					if action==0:
						d_list[d_change].unblock()

			if mode==1:
				while(True):
					f=input('Please enter source node: ')
					if f in G.nodes(): break
					print 'Please enter a valid node'
				if leave==True: break
				while(True):
					t=input('Please enter target node: ')
					if t in G.nodes(): break
					print 'Please enter a valid node'
				bwreq=input('Please enter bw req: ')
				latreq=input('Please enter lat req: ')
				block=input('Please enter 1 for block: ')
				# create demand
				temp_dem = dem.demand(G.nodes(),None,None)
				temp_dem.make_choice_concrete(f,t,bwreq,latreq)
				if block==1:
					print 'Blocking demand'
					temp_dem.block()
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

	# gurobi solver
	if lp_enable or cli_lp:
		print '\n\n---\nRun Gurobi Solver'
		if len(d_list)>0:
			lptic = time.time()
			[lp_result,lp_sel_paths,lp_accepted,lp_rejected,lp_ratio,lp_x]=lp.solve(G,d_list)
			lptoc = time.time()
			lp_time=lptoc - lptic
			print '\nGurobi Solver complete\n---'
		else:
			print 'no demands available'


	if mode=='genetic_opt':
		[pop_size, maxgenerations, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, end_mut, non_prob, weight_ac]=gen_param.next()

	# run genetic algorithm
	if gen_enable:
		print '\nRun Genetic Algorithm'
		tic = time.time()
		[result, gen_sel_paths, gen_ratio, gen_cycles]=gen.paraevolution\
		(G, d_list, pop_size, maxgenerations,\
		clergy_size, clergy_children, nobility_size, nobility_children, start_mut, end_mut, non_prob, weight_ac,lp_ratio)
		toc = time.time()
		gen_time=toc-tic
		print '\nGenetic:'
		print 'Acceptance ratio: '+str(gen_ratio*100)+'%'
		print 'Iterations: '+str(gen_cycles+1)
		print 'Gen Result: '+str(result)
		print 'Gen sel paths: '+str(gen_sel_paths)
		print 'Genetic Time: '+str(gen_time)

	# print 
	if gr_enable:
		# print out result stats
		print '\n\n######### End Stats ###############'
		print 'Greedy:'
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
		print 'sel path book:\n'+str(gf.get_all_sel_paths(d_list))

	# print out gurobi stats
	if lp_enable or cli_lp:
		print '\nGurobi:'
		print 'Acceptance ratio '+str(lp_ratio*100)+'%'
		print 'LP Result: '+str(lp_result)
		print 'LP sel paths:\n'+str(lp_sel_paths)
		#print 'Allocated demands: '+str(lp_accepted)
		print 'Gurobi Time: '+str(lp_time)
		print '\n'

	# print comparison
	if lp_enable and gr_enable:
		print '\n\n######### Comparison Stats ###############'
		print 'lp is '+str(lp_ratio*100-acceptance_ratio*100)+'% points better than greedy'
		print 'greedy paths: '+str(gf.get_all_sel_paths(d_list))
		print 'lp paths: '+str(lp_sel_paths)
		print '\n'

	# print graph info
	print 'Graph Type: '+graph_type
	print 'Number of Nodes: '+str(G.number_of_nodes())
	print 'Number of Edges: '+str(G.number_of_edges())

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
			
		# plot gen
		if gen_enable:
			gen_plot_pool=gf.plot_pool('gopo')
			G_gen=copy.deepcopy(G)
			gen_plot_pool.plotpa(G_gen, None, 1, plot_enable)
			for key in (gen_sel_paths):
				gen_p=gen_sel_paths[key][0]
				gen_bw=gen_sel_paths[key][1]
				G_gen = gf.update_edges(G_gen, gen_p, gen_bw)
				gen_plot_pool.plotpa(G_gen, gen_p, 1, plot_enable)
			os.system('convert ' + gen_plot_pool.plot_pngs + ' +append '+str(gen_plot_pool.prefix)+'.png')

	# show plot
	if show_enable and plot_enable:
		if gr_enable:
			os.system('eog '+str(plot_pool.prefix)+'.png')
		elif lp_enable:
			os.system('eog '+str(lp_plot_pool.prefix)+'.png')
		elif gen_enable:
			os.system('eog '+str(gen_plot_pool.prefix)+'.png')

	
	#if lp_ratio<gen_ratio:
		#print 'Ha! Genetic is better than LP'
		#print 'Sanity: '+str(gf.is_sane(G,gen_sel_paths))
		#break

	if mode=='genetic_opt':
		gf.write2file('experi',\
		[[pop_size, maxgenerations, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, end_mut, non_prob, weight_ac], lp_ratio, lp_time, gen_ratio, gen_time])


		if lp_ratio>gen_ratio-0.05 and lp_ratio<gen_ratio+0.05:
			if gen_time<min_gen_time or min_gen_time==None:
				best_param=[[pop_size, maxgenerations, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, end_mut, non_prob, weight_ac], lp_ratio, lp_time, gen_ratio, gen_time]


print best_param

# print out stats for repeats
if repeats>1 and gr_enable:
	print '\n \n \nnumber of rerouting attempts: '+str(number_of_rerouting_attempts_pool)
	print '\navg acceptance ratio: '+str(sum(acceptance_ratio_pool)/len(acceptance_ratio_pool))
	if len(successful_rerouting_fraction_pool)>0:
		print '\navg Successful rerouting fraction: '+str(sum(successful_rerouting_fraction_pool)/len(successful_rerouting_fraction_pool))
	

