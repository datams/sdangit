####################################################################
########################## classes #################################
####################################################################

import random
import graphFunctions as gf

# demand class reflects a flow demand with source, target, bw and lat req.
class demand:
    def __init__(self, nodi, bw_variants, lat_variants):
	# source ID for a flow in the graph
	self.source = None
	# target ID for a flow in the graph
	self.target = None
	# graph's nodes (potential sources and targets)
	self.nodes = nodi
	self.bw = None
	self.lat = None
	self.bw_variants = bw_variants
	self.lat_variants = lat_variants
	# reflects allocation status: 0=not allocated, 1=allocated	
	self.x=0
	self.path=[]
	self.paths_pack=[]
	#self.priority=1
	self.group=None
	# status reflects rerouting permissions
	# 1=reroutable (used, not live), 2=blocked (live)
	# 0=cancellable not used anymore
	self.status=1
    def set_source(self, s):
        self.source=s
    def get_source(self):
        return self.source
    def set_target(self, t):
        self.target=t
    def get_target(self):
        return self.target
    def set_nodes(self, n):
	self.nodes=n
    def get_nodes(self):
	return self.nodes
    def get_bw(self):
	return self.bw
    def get_lat(self):
	return self.lat
    def set_allocated(self):
	self.x=1
    def set_unallocated(self):
	self.x=0
    def set_path(self,path2set):
	self.path=path2set
    def get_path(self):
	return self.path
    def get_alternative_paths(self):
	all_paths=gf.pack2p(self.paths_pack)
	popped=all_paths.pop(all_paths.index(self.path))
	alternative_paths=all_paths
	return alternative_paths
    def add_to_paths_pack(self,G,sel_path):
	current_pack=self.paths_pack
	current_paths=[element[0] for element in current_pack]
	if sel_path not in current_paths:
		path_elist=gf.n2e_list(sel_path)
		path_lat=gf.path_len(G,path_elist)
		path_hops=len(path_elist)
		self.paths_pack.append((sel_path,path_lat,path_hops))
    def set_paths_pack(self,pack2set):
	self.paths_pack=pack2set
    #def get_priority(self):
	#return self.priority
    #def set_priority(self,priority2set):
	#self.priority=priority2set
    def get_group(self):
	return self.group
    def set_group(self,group2set):
	self.group=group2set
    def block(self):
	self.status=2
    def unblock(self):
	self.status=1

    # random choice of two distinct graph nodes as source / target
    # bw and lat choice out of a list of possible values
    def make_random_choice(self):
	self.bw=random.choice(self.bw_variants)
	self.lat=random.choice(self.lat_variants)
	temp_n=self.nodes
	self.source = random.choice(temp_n)
	source_index = temp_n.index(self.source)
	temp_n.pop(source_index)
	self.target = random.choice(temp_n)

    # random choice of two distinct graph nodes as source / target
    # bw and lat choice by random uniform choice
    def make_total_random_choice(self, bw_lowest, bw_highest, lat_lowest, lat_highest):
	self.bw=random.uniform(bw_lowest, bw_highest)
	self.lat=random.uniform(lat_lowest, lat_highest)
	temp_n=self.nodes
	self.source = random.choice(temp_n)
	source_index = temp_n.index(self.source)
	temp_n.pop(source_index)
	self.target = random.choice(temp_n)

    # sets user source and target according to user definition
    def make_choice_concrete(self,x,y,bw,lat):
	self.bw=bw
	self.lat=lat
	self.source = x
	self.target = y
