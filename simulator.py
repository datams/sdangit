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
all_eval_records = []

# Create parameters pool
param_container = gp.gen_param()
#repeats = param_container.size()
repeats = 1
exp_times = []
graphtype='srg'
repetitions=1

# get time
time_now= (time.strftime("%H%M%S"))
date_now= (time.strftime("%d%m"))
exp_start_time = time.time()

for expnum in range(repeats):

	exp_name=graphtype+'_k'+str(repetitions)+'_'+date_now+'_'+time_now
	exp_name_numbered=graphtype+'_k'+str(repetitions)+'_'+date_now+'_'+time_now+'_'+str(expnum)

	tic = time.time()
	#param=param_container.next()
	#param=[20, 0, 0, 0, 0, 3, 50, 0.9, 1]
	param=[200, 0, 0, 0, 0, 80, 60, 0.9, 2]
	#[pop_size, clergy_size, clergy_children, nobility_size, nobility_children, start_mut, non_prob, weight_ac, mut_method]

	# Graph and demand creation
	[G, d_list] = ds.get_std_d_list(graphtype)
	#[G, d_list] = ds.get_rnd_d_list('srg', 15)

	# Create per experiment records variable
	current_records=[]

	for rep in range(repetitions):

		# LP solve
		print 'Run LP'
		[lp_time, lp_ratio, lp_sel_paths]=su.linp(G, d_list)
		print 'LP done with acc. ratio: '+str(lp_ratio)+'\n\n'

		# Gen solve
		print 'Run GA'
		[gen_time, gen_ratio, gen_sel_paths]=su.ga_multicore(G, d_list, param, lp_ratio)
		gen_time_tot=gen_time[0]
		gen_time_findpaths=gen_time[1]
		print 'GA done with acc. ratio: '+str(gen_ratio)+'\n\n'

		# Greedy solve
		print 'Run Greedy'
		[greed_time, greed_ratio, greed_sel_paths]=su.greed(G, d_list, 10)
		print 'Greedy done with acc. ratio: '+str(greed_ratio)+'\n\n'
		
		# Record outcome
		all_records.append([lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio])
		current_records.append([lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio])
		gf.write2file('data/'+exp_name+'_runlog', [lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio])	

	# LP runtime
	lpt=[lp_time for [lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio] in current_records]
	avg_lpt=numpy.mean(lpt)
	avg_lpt=round(avg_lpt,4)
	std_lpt=numpy.std(lpt)
	std_lpt=round(std_lpt,4)
	# LP ratio
	lpr=[lp_ratio for [lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio] in current_records]
	avg_lpr=numpy.mean(lpr)
	avg_lpr=round(avg_lpr,4)

	# GA runtime
	gnt=[gen_time_tot for [lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio] in current_records]
	gntf=[gen_time_findpaths for [lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio] in current_records]
	avg_gnt=numpy.mean(gnt)
	avg_gnt=round(avg_gnt,4)
	std_gnt=numpy.std(gnt)
	std_gnt=round(std_gnt,4)
	avg_gntf=numpy.mean(gntf)
	avg_gntf=round(avg_gntf,4)
	std_gntf=numpy.std(gntf)
	std_gntf=round(std_gntf,4)
	# GA ratio
	gnr=[gen_ratio for [lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio] in current_records]
	avg_gnr=numpy.mean(gnr)
	avg_gnr=round(avg_gnr,4)

	# Greedy runtime
	grt=[greed_time for [lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio] in current_records]
	avg_grt=numpy.mean(grt)
	avg_grt=round(avg_grt,4)
	std_grt=numpy.std(grt)
	std_grt=round(std_grt,4)
	# Greedy ratio
	grr=[greed_ratio for [lp_time, lp_ratio, gen_time_tot, gen_time_findpaths, gen_ratio, param, greed_time, greed_ratio] in current_records]
	avg_grr=numpy.mean(grr)
	avg_grr=round(avg_grr,4)

	lp_ratio=round(lp_ratio,5)
	gen_ratio=round(gen_ratio,5)
	greed_ratio=round(greed_ratio,5)	


	# Boxplot
	boxpp.plot(lpt, avg_lpr, gnt, avg_gnr, gntf, grt, avg_grr, 'data/'+exp_name_numbered)

	# write avg and std to file
	all_eval_records.append([avg_lpt, std_lpt, lp_ratio, avg_gnt, std_gnt, avg_gntf, std_gntf, gen_ratio, param, avg_grt, std_grt, greed_ratio])
	gf.write2file('data/'+exp_name+'_log', '\n\nAvg and Std over reps\n'+str([avg_lpt, std_lpt, lp_ratio, avg_gnt, std_gnt, avg_gntf, std_gntf, gen_ratio, param, avg_grt, std_grt, greed_ratio]))

	# time to go prediction
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
sorted_records = sorted(all_eval_records, key=operator.itemgetter(3))
for record in sorted_records:
	gf.write2file('data/'+exp_name+'_log',	record)



