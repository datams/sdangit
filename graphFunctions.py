import matplotlib.pyplot as plt
import matplotlib.colors as colors
import networkx as nx
import random
import copy
#import matplotlib.cm as cmx
#import numpy as np
import pygraphviz
import os
import operator

####################################################################
########################## functions ###############################
####################################################################

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
				print 'removed edge: '+str(n)+','+str(nbr)
	return G

# returns link utilization
def link_util(G,F):

	orig_bw=[]
	for n,nbrs in G.adjacency_iter():
		for nbr,eattr in nbrs.items():
		        orig_bw.append(eattr['bw'])

	end_bw=[]
	for n,nbrs in F.adjacency_iter():
		for nbr,eattr in nbrs.items():
		        end_bw.append(eattr['bw'])

	usage=[]
	for i in end_bw:
		if end_bw[i]!=orig_bw[i]:
			available_bw=float(orig_bw[i])
			used_bw=float(orig_bw[i])-float(end_bw[i])
			partial_util=float(used_bw)/float(available_bw)
			usage.append(partial_util)
	if len(usage)>0:
		utilization=sum(usage)/len(usage)
	else:
		utilization=0
	
	return  utilization

# returns updated graph based on path allocation
def update_edges(G, path, bwreq):
	path=n2e_list(path)
	for i,k in path:
		old_bw = G[i][k]['bw']
		G[i][k]['bw'] = old_bw - bwreq
	return G

# plots (graphviz) graph with demand d and path p
def plot_graphviz(G,demand,path,k):
	
	# get edge labels
	for u,v,d in G.edges(data=True):
		l = d.get('lat','')
		b = d.get('bw','')
		d['label'] = str(l)+' / '+str(b)

	# returns pygraphviz graph A from NetworkX graph G
	A = nx.to_agraph(G)

	# colorize source and target
	if demand!=None:
		n=A.get_node(demand.get_source())
		n.attr['color']='red'
		n=A.get_node(demand.get_target())
		n.attr['color']='green'

	# colorize path
	if path!=None:
		path_edges=n2e_list(path)
		for i in range(0,len(path_edges)):
			edge=path_edges[i]
			e=A.get_edge(edge[0],edge[1])
			e.attr['color']='blue'

	# plot
	A.layout(prog='dot')
	topo_name='topo'+str(k)+'.png'
	A.draw(topo_name)
	return topo_name

def select_path(paths_pack, criterion):
	# take minimum lat path or minimum hop path
	if criterion=='lat':
		selected_path = min(paths_pack, key=operator.itemgetter(1))
		min_lat=selected_path[1]
		selected_path=selected_path[0]
		print 'selected_path:\n'+str(selected_path)
	if criterion=='hops':
		selected_path = min(paths_pack, key=operator.itemgetter(2))
		min_hop=selected_path[2]
		selected_path=selected_path[0]
		print 'min_hops_path:\n'+str(selected_path)
	return selected_path

