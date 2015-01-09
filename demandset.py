####################### modules imports ############################
import demand as dem
import customGraph
import graphFunctions as gf

######################### functions ################################
# returns a d_list with d_params [source, target, bw, lat]
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

# prints a list of random demands [source, target, bw, lat]
def build_d_params(number_of_demands, G, bw_lowest, bw_highest, lat_lowest, lat_highest):
	path_selection_criterion = 'hops'
	d_list=[]
	for k in range(number_of_demands):
		while(True):
			print 'Create demand Nr. '+str(k)
			# initialize demand
			temp_dem = dem.demand(G.nodes(),88,88)
			# make random choice
			#temp_dem.make_random_choice()
			temp_dem.make_total_random_choice(bw_lowest, bw_highest, lat_lowest, lat_highest)
			# check feasibility
			if gf.is_feasible(G,temp_dem,path_selection_criterion):
				d_list.append(temp_dem)
				break
	for d in d_list:
		print '['+str(d.source)+','+str(d.target)+','+str(d.bw)+','+str(d.lat)+']'+','+'\\'

# runs build_d_params for graph_typ and n demands
def run_build(graph_type,number_of_demands):
	G			=	customGraph.make(graph_type)
	bw_lowest		=	gf.minimum_bw(G)
	bw_highest		=	gf.maximum_bw(G)
	lat_lowest		=	gf.minimum_lat(G)
	lat_highest		=	gf.maximum_lat(G)*30
	build_d_params(number_of_demands, G, bw_lowest, bw_highest, lat_lowest, lat_highest)

########################## build data ###############################

#run_build('srg',15)
#run_build('srg_multiple',50)

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

	d_params_srg_multiple=[\
	[274,288,6.25609563163,54.8997570784],\
	[170,330,5.52749109725,71.9302899754],\
	[162,138,11.3205171264,150.410968586],\
	[149,110,10.7923356722,28.076263011],\
	[325,276,8.97425806788,43.1811296486],\
	[170,318,5.13514045664,89.488450494],\
	[275,183,13.3835389085,76.3119397374],\
	[148,1,7.69044974185,87.5087569465],\
	[246,234,6.80515402572,164.185324249],\
	[89,87,11.927734889,30.7313138537],\
	[199,180,13.5291620774,17.2170068184],\
	[21,45,8.56717573156,86.9098446577],\
	[131,128,5.25665635072,90.1374285747],\
	[325,274,11.0028334834,53.2331813518],\
	[226,173,6.21939911779,37.1113834482],\
	[296,309,13.3124661516,124.387333983],\
	[320,288,5.40874027456,28.6674245695],\
	[267,310,13.6367158286,26.0714748278],\
	[66,65,8.82409636431,100.081380182],\
	[170,330,12.8334018839,128.900646846],\
	[169,274,12.804398673,178.109768932],\
	[106,3,10.0884765047,23.6214811196],\
	[36,23,12.4791021575,155.520431135],\
	[173,202,7.04512512612,177.864049923],\
	[3,107,14.0131302339,154.743912999],\
	[308,218,10.635755691,148.151586272],\
	[170,317,9.05900627036,79.688820709],\
	[5,58,8.1165458133,83.2169349519],\
	[138,157,14.808862755,123.738466773],\
	[275,170,6.36681945788,139.871800804],\
	[47,45,9.72344288069,167.540697944],\
	[43,21,5.6235690593,134.717705869],\
	[288,306,11.9795997111,12.0839992154],\
	[26,54,11.5806318847,148.574300331],\
	[78,64,7.57303086555,125.194041119],\
	[191,194,13.8659108313,176.909605671],\
	[320,169,12.1906471131,30.9455172469],\
	[24,22,11.7223164499,111.17196094],\
	[216,251,12.1253110473,169.508662189],\
	[43,45,7.75825731285,32.4471638481],\
	[328,309,12.9704029511,126.618613672],\
	[121,98,13.7495844662,68.3072140919],\
	[275,330,14.4679405671,73.996991727],\
	[47,57,5.92483774855,176.723896891],\
	[309,299,7.39328865786,118.513027682],\
	[316,202,11.9946266695,21.693325424],\
	[320,306,10.4993674228,37.7509811811],\
	[316,288,8.4045978571,97.8206348072],\
	[106,5,7.8575364661,131.749556486],\
	[108,5,11.2385349201,46.3472002127]]

	if graph_type=='srg':
		G = customGraph.make('srg')
		return [G,build_d_list(G,d_params_srg)]
	elif graph_type=='srg_multiple':
		G = customGraph.make('srg_multiple')
		return [G,build_d_list(G,d_params_srg_multiple)]
	else:
		print 'invalid graph_type'


def get_rnd_d_list(graph_type, number_of_demands):
	G = customGraph.make(graph_type)

	bw_lowest		=	gf.minimum_bw(G)
	bw_highest		=	gf.maximum_bw(G)
	lat_lowest		=	gf.minimum_lat(G)
	lat_highest		=	gf.maximum_lat(G)*30

	path_selection_criterion = 'hops'
	d_list=[]
	for k in range(number_of_demands):
		while(True):
			print 'Create demand Nr. '+str(k)
			# initialize demand
			temp_dem = dem.demand(G.nodes(),88,88)
			# make random choice
			#temp_dem.make_random_choice()
			temp_dem.make_total_random_choice(bw_lowest, bw_highest, lat_lowest, lat_highest)
			# check feasibility
			if gf.is_feasible(G,temp_dem,path_selection_criterion):
				d_list.append(temp_dem)
				break
		# 4Debug: print demands
		print 'demand '+str(k)+': '+str(d_list[k].source)+' ==> '+str(d_list[k].target)

	return [G, d_list]

