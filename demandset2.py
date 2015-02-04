#!/usr/bin/env python

####################### modules imports ############################
import demand as dem
import customGraph
import graphFunctions as gf
import solverunit as su
import numpy
import networkx as nx

######################### functions ################################

# runs build_d_params for graph_typ and n demands
def run_build(graph_type, ratio):
	
	# produce graph
	G = customGraph.make(graph_type)

	# calculate number of demands
	number_of_demands = int(float(0.4)*float(G.number_of_edges()))
	
	# set bw variants
	bw_variants = [0.2, 0.2, 0.4, 0.6, 1]

	# calculate lat variants
	min_lat=gf.minimum_lat(G)
	max_lat=gf.maximum_lat(G)
	mean_lat=int((min_lat+max_lat)/2)
	lat_variants = numpy.linspace(5, nx.diameter(G)*mean_lat, 5)
	#lat_variants = [1 ,2 ,3]
	lat_variants = lat_variants.tolist()

	build_d_params(number_of_demands, G, ratio, bw_variants, lat_variants)

# prints a list of random demands [source, target, bw, lat]
def build_d_params(number_of_demands, G, ratio, bw_variants, lat_variants):
	while(True):


		bw_lowest		=	gf.minimum_bw(G)/10
		bw_highest		=	gf.maximum_bw(G)
		lat_lowest		=	gf.minimum_lat(G)*20
		lat_highest		=	gf.maximum_lat(G)*20
		
		path_selection_criterion = 'hops'
		d_list=[]
		for k in range(number_of_demands):
			while(True):
				print 'Create demand Nr. '+str(k)
				# initialize demand
				temp_dem = dem.demand(G.nodes(), bw_variants, lat_variants)
				# make random choice
				temp_dem.make_random_choice()
				#temp_dem.make_total_random_choice(bw_lowest, bw_highest, lat_lowest, lat_highest)
				# check feasibility
				if gf.is_feasible2(G, temp_dem, path_selection_criterion):
					d_list.append(temp_dem)
					break

		#for (q,k) in G.edges():
			#print str((q,k))+' '+str(G[q][k])


		print 'Running LP'
		[lp_time, lp_ratio, lp_sel_paths]=su.linp(G, d_list)
		print 'lp_sel_paths '+str(lp_sel_paths)
		print 'lp_ratio '+str(lp_ratio)
		#input(5)
		break
		#if lp_ratio>ratio:
			#break

	for d in d_list:
		gf.write2file_pure('d_lists', '['+str(d.source)+','+str(d.target)+','+str(d.bw)+','+str(d.lat)+'],\\')
	gf.write2file_pure('d_lists', 'lp_ratio: '+str(lp_ratio)+'\n\n')	
	return


########################## build data ###############################

m=70
gf.write2file_pure('d_lists', "\n\n\nrun_build('srg', 14, m) for ratio: "+str(m))
print 'd_lists', "\n\n\nrun_build('srg', 14, m) for ratio: "+str(m)
run_build('switch', m)





########################## help function ############################

# converts params to d_list
def build_d_list(G,d_params):
	d_list=[]
	for d in d_params:
		# initialize demand
		temp_dem = dem.demand(G.nodes(),88,88)
		# set fields
		temp_dem.make_choice_concrete(d[0],d[1],d[2],d[3])
		# add to list
		d_list.append(temp_dem)
	return d_list


##################### data out of build #############################

def get_std_d_list(graph_type):

	
	d_params_srg=[\
	[6,2,8.29221446513,65.7834691962],\
	[4,2,6.01901435229,177.951162664],\
	[2,4,8.84723301878,95.1377893186],\
	[16,4,13.1140795065,70.6748229498],\
	[6,2,13.246727625,55.9361252412],\
	[6,3,12.7800538138,98.5313248055],\
	[16,2,11.6138911825,162.627359859],\
	[4,3,6.48471978893,159.777507539],\
	[16,2,11.3011846929,107.655937609],\
	[3,2,12.8492335435,122.003454927],\
	[3,16,5.87814920034,177.57822566],\
	[4,16,13.2379293068,22.4956931629],\
	[2,16,5.26350258858,5.6304064309],\
	[16,6,9.76385640111,135.213284538],\
	[2,3,13.7785166894,80.1619045641]]
	
	if graph_type=='srg':
		G = customGraph.make('srg')
		return [G,build_d_list(G,d_params_srg)]
	elif graph_type=='srg_multiple':
		G = customGraph.make('srg_multiple')
		return [G,build_d_list(G,d_params_srg_multiple)]
	elif graph_type=='srg_multiple5':
		G = customGraph.make('srg_multiple5')
		return [G,build_d_list(G,d_params_srg_multiple5)]
	else:
		print 'invalid graph_type'


