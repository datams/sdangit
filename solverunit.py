import time
import lpsolv as lp
import greedy as gr
import genetic2 as gen

def linp(G, d_list):
	print '\nRun LP Solver'
	lptic = time.time()

	[lp_result,lp_sel_paths,lp_accepted,lp_rejected,lp_ratio,lp_x]=lp.solve(G,d_list)

	lptoc = time.time()
	lp_time = lptoc - lptic
	return [lp_time, lp_ratio, lp_sel_paths]

def ga(G, d_list, gen_param):
	print '\nRun Genetic Algorithm'
	[pop_size, maxgenerations, clergy_size, clergy_children, nobility_size,\
	nobility_children, start_mut, end_mut, non_prob, weight_ac,lp_ratio]=gen_param
	tic = time.time()
	
	[result, gen_sel_paths, gen_ratio, gen_cycles]=gen.paraevolution\
	(G, d_list, pop_size, maxgenerations,\
	clergy_size, clergy_children, nobility_size, nobility_children, start_mut, end_mut, non_prob, weight_ac,lp_ratio)
	
	toc = time.time()
	gen_time = toc - tic
	# print 'Iterations: '+str(gen_cycles+1)
	return [gen_time, gen_ratio, gen_sel_paths]



