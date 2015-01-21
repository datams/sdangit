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

'''
########################## experiment ##############################

# Create records variable
records = []

# Create parameters pool
param_container = gp.gen_param()
#repeats = param_container.size()
repeats = 1
exp_times = []
graphtype='srg_multiple'
repetitions=100
time_now= (time.strftime("%H%M%S"))
date_now= (time.strftime("%d%m%Y"))

exp_name=graphtype+' k='+str(repetitions)+'_'+date_now+'_'+time_now

exp_start_time = time.time()
for expnum in range(repeats):

	tic = time.time()
	#param=param_container.next()
	param=[20, 0, 0, 0, 0, 3, 50, 0.9, 1]

	# Graph and demand creation
	[G, d_list] = ds.get_std_d_list(graphtype)
	#[G, d_list] = ds.get_rnd_d_list('srg', 15)

	for rep in range(repetitions):

		# LP solve
		[lp_time, lp_ratio, lp_sel_paths]=su.linp(G, d_list)

		# Gen solve
		[gen_time, gen_ratio, gen_sel_paths]=su.ga_multicore(G, d_list, param, lp_ratio)

		# Greedy solve
		#[greed_time, greed_ratio, greed_sel_paths]=su.greed(G, d_list, 10)
		
		
		# Record outcome
		records.append([lp_time, lp_ratio, gen_time, gen_ratio, param])

	lpt=[lp_time for [lp_time, lp_ratio, gen_time, gen_ratio, param] in records]
	gnt=[gen_time for [lp_time, lp_ratio, gen_time, gen_ratio, param] in records]

	avg_lpt=sum(lpt)/len(lpt)
	std_lpt=numpy.std(lpt)
	avg_gnt=sum(gnt)/len(gnt)
	std_gnt=numpy.std(gnt)

	boxpp.plot(lpt,gnt,exp_name)

	# write avg and std to file
	gf.write2file(exp_name+'_log', [avg_lpt, std_lpt, avg_gnt, std_gnt, param])

	# time calculations
	toc = time.time()
	exp_time = toc - tic
	exp_times.append(exp_time)
	avg_exp_time = sum(exp_times)/len(exp_times)
	past_time_calc=avg_exp_time*expnum
	past_time_real=toc-exp_start_time
	remaining_time=(repeats-expnum)*avg_exp_time
	gf.write2file(exp_name+'_time', 'n='+str(expnum)+'/'+str(repeats)+' time past: '+gp.sec2timestr(past_time_real)+\
	' time past calc: '+gp.sec2timestr(past_time_calc)+' time remaining calc: '+gp.sec2timestr(remaining_time))

# sort ALL records and print to file
gf.write2file(exp_name+'_log',	'\n\n\n\nSorted Records:')
sorted_records = sorted(records, key=operator.itemgetter(1))
for record in sorted_records:
	gf.write2file(exp_name+'_log',	record)














































########################## experiment ##############################

# Create records variable
records = []

# Create parameters pool
param_container = gp.gen_param()
#repeats = param_container.size()
repeats = 1
exp_times = []
graphtype='srg_multiple5'
repetitions=100
time_now= (time.strftime("%H%M%S"))
date_now= (time.strftime("%d%m%Y"))

exp_name=graphtype+' k='+str(repetitions)+'_'+date_now+'_'+time_now

exp_start_time = time.time()
for expnum in range(repeats):

	tic = time.time()
	#param=param_container.next()
	param=[20, 0, 0, 0, 0, 3, 50, 0.9, 1]

	# Graph and demand creation
	[G, d_list] = ds.get_std_d_list(graphtype)
	#[G, d_list] = ds.get_rnd_d_list('srg', 15)

	for rep in range(repetitions):

		# LP solve
		[lp_time, lp_ratio, lp_sel_paths]=su.linp(G, d_list)

		# Gen solve
		[gen_time, gen_ratio, gen_sel_paths]=su.ga_multicore(G, d_list, param, lp_ratio)

		# Greedy solve
		#[greed_time, greed_ratio, greed_sel_paths]=su.greed(G, d_list, 10)
		
		
		# Record outcome
		records.append([lp_time, lp_ratio, gen_time, gen_ratio, param])

	lpt=[lp_time for [lp_time, lp_ratio, gen_time, gen_ratio, param] in records]
	gnt=[gen_time for [lp_time, lp_ratio, gen_time, gen_ratio, param] in records]

	avg_lpt=sum(lpt)/len(lpt)
	std_lpt=numpy.std(lpt)
	avg_gnt=sum(gnt)/len(gnt)
	std_gnt=numpy.std(gnt)

	boxpp.plot(lpt,gnt,exp_name)

	# write avg and std to file
	gf.write2file(exp_name+'_log', [avg_lpt, std_lpt, avg_gnt, std_gnt, param])

	# time calculations
	toc = time.time()
	exp_time = toc - tic
	exp_times.append(exp_time)
	avg_exp_time = sum(exp_times)/len(exp_times)
	past_time_calc=avg_exp_time*expnum
	past_time_real=toc-exp_start_time
	remaining_time=(repeats-expnum)*avg_exp_time
	gf.write2file(exp_name+'_time', 'n='+str(expnum)+'/'+str(repeats)+' time past: '+gp.sec2timestr(past_time_real)+\
	' time past calc: '+gp.sec2timestr(past_time_calc)+' time remaining calc: '+gp.sec2timestr(remaining_time))

# sort ALL records and print to file
gf.write2file(exp_name+'_log',	'\n\n\n\nSorted Records:')
sorted_records = sorted(records, key=operator.itemgetter(1))
for record in sorted_records:
	gf.write2file(exp_name+'_log',	record)





'''











































########################## experiment ##############################

# Create records variable
records = []

# Create parameters pool
param_container = gp.gen_param()
#repeats = param_container.size()
repeats = 1
exp_times = []
graphtype='srg'
repetitions=100
time_now= (time.strftime("%H%M%S"))
date_now= (time.strftime("%d%m%Y"))

exp_name=graphtype+' k='+str(repetitions)+'_'+date_now+'_'+time_now

exp_start_time = time.time()
for expnum in range(repeats):

	tic = time.time()
	#param=param_container.next()
	param=[20, 0, 0, 0, 0, 3, 50, 0.9, 1]

	# Graph and demand creation
	[G, d_list] = ds.get_std_d_list(graphtype)
	#[G, d_list] = ds.get_rnd_d_list('srg', 15)

	for rep in range(repetitions):

		# LP solve
		[lp_time, lp_ratio, lp_sel_paths]=su.linp(G, d_list)

		# Gen solve
		[gen_time, gen_ratio, gen_sel_paths]=su.ga_multicore(G, d_list, param, lp_ratio)

		# Greedy solve
		#[greed_time, greed_ratio, greed_sel_paths]=su.greed(G, d_list, 10)
		
		
		# Record outcome
		records.append([lp_time, lp_ratio, gen_time, gen_ratio, param])

	lpt=[lp_time for [lp_time, lp_ratio, gen_time, gen_ratio, param] in records]
	gnt=[gen_time for [lp_time, lp_ratio, gen_time, gen_ratio, param] in records]

	avg_lpt=sum(lpt)/len(lpt)
	std_lpt=numpy.std(lpt)
	avg_gnt=sum(gnt)/len(gnt)
	std_gnt=numpy.std(gnt)

	boxpp.plot(lpt,gnt,exp_name)

	# write avg and std to file
	gf.write2file(exp_name+'_log', [avg_lpt, std_lpt, avg_gnt, std_gnt, param])

	# time calculations
	toc = time.time()
	exp_time = toc - tic
	exp_times.append(exp_time)
	avg_exp_time = sum(exp_times)/len(exp_times)
	past_time_calc=avg_exp_time*expnum
	past_time_real=toc-exp_start_time
	remaining_time=(repeats-expnum)*avg_exp_time
	gf.write2file(exp_name+'_time', 'n='+str(expnum)+'/'+str(repeats)+' time past: '+gp.sec2timestr(past_time_real)+\
	' time past calc: '+gp.sec2timestr(past_time_calc)+' time remaining calc: '+gp.sec2timestr(remaining_time))

# sort ALL records and print to file
gf.write2file(exp_name+'_log',	'\n\n\n\nSorted Records:')
sorted_records = sorted(records, key=operator.itemgetter(1))
for record in sorted_records:
	gf.write2file(exp_name+'_log',	record)

