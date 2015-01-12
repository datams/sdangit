import time
import lpsolv as lp
import greedy as gr
import graphFunctions as gf
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


def greed(G, d_list):
	G_updated=G.copy()
	plot_enable=False
	path_selection_criterion = 'hops'
	plot_pool=gf.plot_pool('topo')
	plot_pool.plot(G_updated, None, 1, plot_enable)
	number_of_rerouting_attempts=0
	number_of_rerouting_success=0
	complete_d_list=d_list
	d_list=[]
	i=0
	number_of_demands=0
	tic = time.time()

	for d in complete_d_list:
		d_list.append(d)
		number_of_demands+=1
		[G_updated, plot_pool, number_of_demands, number_of_rerouting_attempts, number_of_rerouting_success]=\
		gr.finder(G, G_updated, d_list, number_of_demands, i, plot_pool, path_selection_criterion,\
		number_of_rerouting_attempts, number_of_rerouting_success, plot_enable)
		i+=1

	toc = time.time()
	greed_time = toc - tic

	greed_ratio = float(gf.get_num_alloc_d(d_list))/(len(d_list))
	greed_sel_paths = gf.get_all_sel_paths(d_list)

	return [greed_time, greed_ratio, greed_sel_paths]