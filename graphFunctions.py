import matplotlib.pyplot as plt
import matplotlib.colors as colors
import networkx as nx
import random
import copy
import pylab as pl
#import numpy as np
import pygraphviz
import os
import operator

####################################################################
########################## functions ###############################
####################################################################

# allocates a paths
def alloc(G, d, path_selection_criterion, sel_paths_book):
	# copy of graph for pruning and updating
	G_prune=copy.deepcopy(G)
	G_updated=copy.deepcopy(G)

	path_pack=[]
	sel_path=[]

	print '\nDemand: '
	print 'Path to find: '+str(d.source)+' ==> '+str(d.target)
	print "bw req: "+str(d.bw)
	print "lat req: "+str(d.lat)

	# pruning
	G_prune=prune_bw(G_prune, d.get_bw())

	# path finding
	paths_pack = shortest_p(G_prune,d.get_source(),d.get_target(),d.get_lat())
	print '\nPaths (with lat.) found: \n'+str(paths_pack)

	if paths_pack!=[] and paths_pack!=None:
		# store found paths in demand
		d.set_paths_pack(paths_pack)
		# path selection
		sel_path = select_path(paths_pack, path_selection_criterion)
		# store sel path in demand
		d.set_allocated()
		d.set_path(sel_path)
		print 'd.path is '+str(d.path)
		# update graph
		G_updated=update_edges(G_updated, sel_path, d.get_bw())
		# store sel path in dictionary book
		sel_paths_book[(d.get_source(),d.get_target())]=sel_path


	return [G_updated, paths_pack, sel_path, sel_paths_book]

# un-allocates a paths
def unalloc(G_updated, d, sel_paths_book):
	# update graph
	G_updated=update_edges(G_updated, d.get_path(), -d.get_bw())
	# delete entry in sel path dictionary
	sel_paths_book.pop((d.get_source(),d.get_target()))
	# delete allocation in demand
	d.set_unallocated()
	d.set_path([])

	return [G_updated, sel_paths_book]

# returns shortest paths that fit lat req.
def shortest_p(G,s,t,lat):
	if nx.has_path(G,s,t)==True:
		intelli_cutoff = lat/minimum_lat(G)
		paths_found_gen = nx.all_simple_paths(G, s, t, cutoff=intelli_cutoff)
		paths_found_list=[p for p in paths_found_gen]
		paths_pack=[]
		for path in paths_found_list[:]:
			path_elist=n2e_list(path)
			path_lat=path_len(G,path_elist)
			path_hops=len(path_elist)
			if path_lat<=lat:
				paths_pack.append((path,path_lat,path_hops))
		return paths_pack
	else:
		print 'There is no path'
		return []

# returns minimum latency in graph
def minimum_lat(G):
	min_weight=None
	for n,nbrs in G.adjacency_iter():
		for nbr,eattr in nbrs.items():
		        temp_weight=eattr['lat']
		        if temp_weight<min_weight or min_weight==None:
		                min_weight=temp_weight
	return min_weight

# returns a list of edges from a list of nodes
def n2e_list(path):
	elist=[]
	
	for i in range(0,len(path)-1):
		if path[i]<path[i+1]:
			elist.append((path[i],path[i+1]))
		else:
			elist.append((path[i+1],path[i]))
	return elist

# returns the length (in terms of latency) of a path
def path_len(G,path):
	len=0
	for a, b in path:
		len += G.get_edge_data(a, b, {"lat":0})["lat"]
	return len

# returns a pruned graph based on bandwidth req
def prune_bw(G, bandwidth):
	for n,nbrs in G.adjacency_iter():
		for nbr,eattr in nbrs.items():
			bw=eattr['bw']
			if bw<bandwidth:
				G.remove_edge(n,nbr)
				print 'prune edge: '+str(n)+','+str(nbr)
	return G

# returns link utilization
def link_util(G,F):

	orig_bw=[]
	for n,nbrs in G.adjacency_iter():
		print 'n: '+str(n)+' nbrs: '+str(nbrs)
		for nbr,eattr in nbrs.items():
		        orig_bw.append(eattr['bw'])
			print "eattr['bw']"+str(eattr['bw'])

	end_bw=[]
	for n,nbrs in F.adjacency_iter():
		for nbr,eattr in nbrs.items():
		        end_bw.append(eattr['bw'])

	usage=[]
	if len(orig_bw)==len(end_bw) and len(orig_bw)>0:
		for i in range(len(end_bw)):
			available_bw=float(orig_bw[i])
			used_bw=float(orig_bw[i])-float(end_bw[i])
			partial_util=float(used_bw)/float(available_bw)
			usage.append(partial_util)

	if len(usage)>0:
		utilization=sum(usage)/len(usage)
	else:
		utilization=0

	return  utilization


# saves link utilization to l_util.png
def util_histo(G, G_updated):
	edges = G.edges()
	d = {}

	for edge in edges:
		from_node = edge[0]
		to_node = edge[1]
		orig_bw = G[from_node][to_node]['bw']
		end_bw = G_updated[from_node][to_node]['bw']
		used_bw=float(orig_bw)-float(end_bw)
		partial_util=float(used_bw)/float(orig_bw)
		d[from_node, to_node] = partial_util

	X = range(len(d))
	pl.bar(X, d.values(), align='center', width=0.5, color='orange')
	pl.xticks(X, d.keys())
	ymax = max(d.values())*1.1
	pl.ylim(0, ymax)
	pl.title('Link Utilization')
	pl.xlabel('Links')
	pl.ylabel('Utilization')
	pl.savefig('l_util.png')


# returns updated graph based on path allocation
def update_edges(G, path, bwreq):
	path=n2e_list(path)
	for i,k in path:
		old_bw = G[i][k]['bw']
		G[i][k]['bw'] = old_bw - bwreq
	return G

# plots (graphviz) graph with demand d and path p
def plot_graphviz(G,demand,plot_counter,colorscheme):
	
	colorpool={}
	colorpool[1]=['green','red','blue']
	colorpool[2]=['chartreuse4','brown4','darkorange']
	
	colors=colorpool[colorscheme]

	# get edge labels
	for u,v,d in G.edges(data=True):
		l = d.get('lat','')
		b = d.get('bw','')
		d['label'] = str(l)+' / '+str(b)

	# returns pygraphviz graph A from NetworkX graph G
	A = nx.to_agraph(G)

	path=None
	# colorize source and target
	if demand!=None:
		n=A.get_node(demand.get_source())
		n.attr['color']=colors[0]
		n=A.get_node(demand.get_target())
		n.attr['color']=colors[1]
		path=demand.get_path()

	# colorize path
	if path!=None:
		path_edges=n2e_list(path)
		for i in range(0,len(path_edges)):
			edge=path_edges[i]
			e=A.get_edge(edge[0],edge[1])
			e.attr['color']=colors[2]

	# plot
	A.layout(prog='dot')
	topo_name='topo'+str(plot_counter)+'.png'
	A.draw(topo_name)
	return topo_name

# produces a png of the plot
def ppng(G_updated, d, plot_pngs, plot_counter, colorscheme, enable):
	if enable:
		plot_pngs+=plot_graphviz(G_updated,d,plot_counter,colorscheme)+' '
		plot_counter+=1
		return [plot_pngs, plot_counter]
	else:
		return [0,0]

# select a path out of a path_pack based on criterion lat or hops
def select_path(paths_pack, criterion):
	# take minimum lat path or minimum hop path
	if criterion=='lat':
		sel_path = min(paths_pack, key=operator.itemgetter(1))
		min_lat=sel_path[1]
		sel_path=sel_path[0]
		# print 'min_lat_path:\n'+str(sel_path)

	if criterion=='hops':
		sel_path = min(paths_pack, key=operator.itemgetter(2))
		min_hop=sel_path[2]
		sel_path=sel_path[0]
		# print 'min_hops_path:\n'+str(sel_path)

	return sel_path

# compare tuple on equality (disregarding order)
def cmpT(tuple1, tuple2):
	if sorted(tuple1) == sorted(tuple2):
		return 1
	else:
		return 0

# check 1 path vs. a set of paths of having same edges
def check_setintersection(path, pathset):
	intersect_list={}
	for i in range(len(pathset)):
		degree = check_intersect(path,pathset[i])
		if degree>0:
			intersect_list[degree]=pathset[i]
	return intersect_list

# check 2 paths on having some of the same edges
def check_intersect(path1, path2):
	path1=n2e_list(path1)
	path2=n2e_list(path2)
	if len(path1)>len(path2):
		long_path=path1
		short_path=path2

	if len(path2)>len(path1):
		long_path=path2
		short_path=path1

	degree=0
	for edge in path1:
		for i in range(len(path2)):
			degree+=cmpT(edge, path2[i])

	return degree

# converts a path pack to a path list
def pack2p(path_pack):
	return [x[0] for x in path_pack]


# prints variable with it's name
def pv(text,var):
	print text+' : '+str(var)
