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

# Create record variable
record = []

# Graph and demand creation
#[G, d_list] = ds.get_std_d_list('srg')
[G, d_list] = ds.get_rnd_d_list('srg', 15)

# LP solve
[lp_time, lp_ratio, lp_sel_paths]=su.linp(G, d_list)

# Gen solve
gen_param=[50, 20, 0.2, 3, 0.1, 2, 3, 1, 20, 0.9, lp_ratio]
[gen_time, gen_ratio, gen_sel_paths]=su.ga(G, d_list, gen_param)

# Greedy solve
#[greed_time, greed_ratio, greed_sel_paths]=su.greed(G, d_list)

# Record outcome
record.append([lp_time, gen_time, gen_param])

# Print results
for rec in record:
	print rec
