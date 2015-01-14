#!/usr/bin/env python

######################## python imports ############################
import networkx as nx
import random
import copy
import pygraphviz
import os
import time

####################### modules imports ############################
import demand as dem
import customGraph
import graphFunctions as gf
import lpsolv as lp
import greedy as gr
import genetic2 as gen
import gen_param as gp
import demandset as ds
import solverunit as su

########################## parameters ##############################


########################## experiment ##############################

# Create records variable
records = []

# Create parameters pool
param_container=gp.gen_param()
repeats=param_container.size()

for q in range(repeats):

	param=param_container.next()

	for rep in range(40):

		# Graph and demand creation
		#[G, d_list] = ds.get_std_d_list('srg')
		[G, d_list] = ds.get_rnd_d_list('srg', 15)

		# LP solve
		[lp_time, lp_ratio, lp_sel_paths]=su.linp(G, d_list)

		# Gen solve
		[gen_time, gen_ratio, gen_sel_paths]=su.ga_multicore(G, d_list, param, lp_ratio)

		# Greedy solve
		#[greed_time, greed_ratio, greed_sel_paths]=su.greed(G, d_list)

		# Record outcome
		records.append([lp_time, gen_time, param])

	# Print results
	#for rec in record:
	#	print rec

	lpt=[lp_time for [lp_time, gen_time, param] in records]
	gnt=[gen_time for [lp_time, gen_time, param] in records]

	avg_lpt=sum(lpt)/len(lpt)
	avg_gnt=sum(gnt)/len(gnt)

	gf.write2file('experi',	[avg_lpt, avg_gnt, param])

	 

