import time
import lpsolv as lp
import greedy as gr
import graphFunctions as gf
import genetic2 as gen
import multiprocessing
from multiprocessing import Manager

def linp(G, d_list):
	print '\nRun LP Solver'
	lptic = time.time()

	[lp_result,lp_sel_paths,lp_accepted,lp_rejected,lp_ratio,lp_x]=lp.solve(G,d_list)

	lptoc = time.time()
	lp_time = lptoc - lptic
	'''	
	print 'lp ratio '+str(lp_ratio)
	print 'lp sel paths'+str(print lp_sel_paths)
	print 'LP is sane: '+str(gf.is_sane(G, lp_sel_paths))
	input(5)
	'''
	return [lp_time, lp_ratio, lp_sel_paths]

def ga(G, d_list, gen_param):
	print '\nRun Genetic Algorithm'
	[pop_size, clergy_size, clergy_children, nobility_size,\
	nobility_children, start_mut, non_prob, weight_ac,lp_ratio]=gen_param
	tic = time.time()
	
	# dummy state	
	e = multiprocessing.Event()
	[result, gen_sel_paths, gen_ratio, gen_cycles]=gen.paraevolution\
	(G, d_list, pop_size,\
	clergy_size, clergy_children, nobility_size, nobility_children, start_mut, non_prob, weight_ac,lp_ratio, e)
	
	toc = time.time()
	gen_time = toc - tic
	# print 'Iterations: '+str(gen_cycles+1)
	return [gen_time, gen_ratio, gen_sel_paths]


# one instance of the GA that determines on e.is_set()
def ga_coreelement(G, d_list, gen_param, lp_ratio, e, return_ratio,  return_paths, ga_thread):

	[pop_size, clergy_size, clergy_children, nobility_size,\
	nobility_children, start_mut, non_prob, weight_ac, mut_method]=gen_param
	tic = time.time()
	
	[result, gen_sel_paths, gen_ratio, gen_cycles]=gen.paraevolution\
	(G, d_list, pop_size,\
	clergy_size, clergy_children, nobility_size, nobility_children, start_mut, non_prob, weight_ac, mut_method, lp_ratio, e, return_ratio, return_paths, ga_thread)
	
	print 'Instance '+str(ga_thread)+' reached target'

	return [gen_ratio, gen_sel_paths]

def ga_multicore(G, d_list, gen_param, lp_ratio):
	print '\nRun multiple process Genetic Algorithm'
	tic = time.time()
	

	#gf.write2file('GAGARATE', 'vor feasible paths')

	print 'Determine all feasible paths'
	for i in range(len(d_list)):
		#G_prune=copy.deepcopy(G)
		G_prune=G.copy()
		G_prune=gf.prune_bw(G_prune, d_list[i].get_bw())
		pathpack=gf.shortest_p(G_prune,d_list[i].source,d_list[i].target,d_list[i].lat)
		d_list[i].set_paths_pack(pathpack)
		print 'added packs'
	

	#gf.write2file('GAGARATE', 'nach feasible paths')
	print 'Find all paths'
	e = multiprocessing.Event()
	manager = Manager()
	return_ratio = manager.dict()
	return_paths = manager.dict()

	w1 = multiprocessing.Process(name='GA1', target=ga_coreelement, args=(G, d_list, gen_param, lp_ratio, e, return_ratio, return_paths, 1))
	w2 = multiprocessing.Process(name='GA2', target=ga_coreelement, args=(G, d_list, gen_param, lp_ratio, e, return_ratio, return_paths, 2))
	w3 = multiprocessing.Process(name='GA3', target=ga_coreelement, args=(G, d_list, gen_param, lp_ratio, e, return_ratio, return_paths, 3))
	w4 = multiprocessing.Process(name='GA4', target=ga_coreelement, args=(G, d_list, gen_param, lp_ratio, e, return_ratio, return_paths, 4))

	print 'Start GA process 1'
    	w1.start()
	print 'Start GA process 2'
    	w2.start()
	print 'Start GA process 3'
    	w3.start()
	print 'Start GA process 4'
    	w4.start()
	print 'GA processes running'
	w1.join()
	w2.join()
	w3.join()
	w4.join()
	print 'All processes ended'
	
	gen_ratio=return_ratio[0][0]
	gen_sel_paths=return_paths[0]

	toc = time.time()
	ga_multicore_time = toc - tic
	
	if gen_ratio>lp_ratio:
		print 'gen acc ratio '+str(gen_ratio)
		#print 'gen sel paths'+str(gen_sel_paths)
		print 'GA is sane: '+str(gf.is_sane(G, gen_sel_paths[0]))
		input(5)
	
	return [ga_multicore_time, gen_ratio, gen_sel_paths]


def greed(G, d_list, n_LP):
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
		number_of_rerouting_attempts, number_of_rerouting_success, plot_enable, n_LP)
		i+=1

	toc = time.time()
	greed_time = toc - tic

	greed_ratio = float(gf.get_num_alloc_d(d_list))/(len(d_list))
	greed_sel_paths = gf.get_all_sel_paths(d_list)

	return [greed_time, greed_ratio, greed_sel_paths]
