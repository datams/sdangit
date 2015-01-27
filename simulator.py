#!/usr/bin/env python

######################## python imports ############################
import networkx as nx
import random
import copy
import pygraphviz
import os
import time
import numpy
import operator

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
import boxpp

########################## experiment ##############################

# Create records variable
all_records = []

# Create parameters pool
param_container = gp.gen_param()
#repeats = param_container.size()
repeats = 1
exp_times = []
graphtype='srg'
repetitions=10
time_now= (time.strftime("%H%M%S"))
date_now= (time.strftime("%d%m%Y"))

exp_start_time = time.time()
for expnum in range(repeats):

	exp_name=graphtype+' k='+str(repetitions)+'_'+date_now+'_'+time_now
	exp_name_numbered=graphtype+' k='+str(repetitions)+'_'+date_now+'_'+time_now+'_'+str(expnum)

	tic = time.time()
	#param=param_container.next()
	#param=[20, 0, 0, 0, 0, 3, 50, 0.9, 1]
	param=[200, 0, 0, 0, 0, 80, 60, 0.9, 1]
	#[pop_size, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, non_prob, weight_ac, mut_method]

	# Graph and demand creation
	[G, d_list] = ds.get_std_d_list(graphtype)
	#[G, d_list] = ds.get_rnd_d_list('srg', 15)

	# Create per experiment records variable
	current_records=[]

	for rep in range(repetitions):

		# LP solve
		[lp_time, lp_ratio, lp_sel_paths]=su.linp(G, d_list)
		#print 'max length of selected LP paths'
		#print max([len(kk) for (kk,ll) in lp_sel_paths.values()])
		#print lp_sel_paths
		#input(8)
		print 'LP done.'
		print 'LP acc. ratio: '+str(lp_ratio)
		if gf.is_sane(G.copy(), lp_sel_paths)==False:
			print 'LP insane'
			input(99)

		# Gen solve
		[gen_time, gen_ratio, gen_sel_paths]=su.ga_multicore(G, d_list, param, lp_ratio)

		# Greedy solve
		#[greed_time, greed_ratio, greed_sel_paths]=su.greed(G, d_list, 10)
		
		
		# Record outcome
		all_records.append([lp_time, lp_ratio, gen_time, gen_ratio, param])
		current_records.append([lp_time, lp_ratio, gen_time, gen_ratio, param])
		gf.write2file('data/'+exp_name+'_log', [lp_time, lp_ratio, gen_time, gen_ratio, param])	

	lpt=[lp_time for [lp_time, lp_ratio, gen_time, gen_ratio, param] in current_records]
	lpr=[lp_ratio for [lp_time, lp_ratio, gen_time, gen_ratio, param] in current_records]
	gnt=[gen_time for [lp_time, lp_ratio, gen_time, gen_ratio, param] in current_records]
	gnr=[gen_ratio for [lp_time, lp_ratio, gen_time, gen_ratio, param] in current_records]

	# LP time
	#avg_lpt=sum(lpt)/len(lpt)
	avg_lpt=numpy.mean(lpt)
	std_lpt=numpy.std(lpt)
	# LP ratio
	#avg_lpr=sum(lpr)/len(lpr)
	avg_lpr=numpy.mean(lpr)

	# GA time
	#avg_gnt=sum(gnt)/len(gnt)
	avg_gnt=numpy.mean(gnt)
	std_gnt=numpy.std(gnt)
	# GA ratio
	avg_gnr=sum(gnr)/len(gnr)
	avg_gnr=numpy.mean(gnr)

	boxpp.plot(lpt, avg_lpr, gnt, avg_gnr, 'data/'+exp_name_numbered)

	# write avg and std to file
	gf.write2file('data/'+exp_name+'_log', '\n\nAvg and Std over reps\n'+str([avg_lpt, std_lpt, lp_ratio, avg_gnt, std_gnt, gen_ratio, param]))

	# time calculations
	toc = time.time()
	exp_time = toc - tic
	exp_times.append(exp_time)
	avg_exp_time = sum(exp_times)/len(exp_times)
	past_time_calc=avg_exp_time*expnum
	past_time_real=toc-exp_start_time
	remaining_time=(repeats-expnum)*avg_exp_time
	gf.write2file('data/'+exp_name+'_time', 'n='+str(expnum)+'/'+str(repeats)+' time past: '+gp.sec2timestr(past_time_real)+\
	' time past calc: '+gp.sec2timestr(past_time_calc)+' time remaining calc: '+gp.sec2timestr(remaining_time))

# sort ALL records and print to file
gf.write2file('data/'+exp_name+'_log',	'\n\n\n\nSorted Records:')
sorted_records = sorted(all_records, key=operator.itemgetter(3))
for record in sorted_records:
	gf.write2file('data/'+exp_name+'_log',	record)



