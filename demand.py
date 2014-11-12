####################################################################
########################## classes #################################
####################################################################

import random

# demand class reflects a flow demand with source, target, bw and lat req.
class demand:
    def __init__(self, nodi, bw_variants, lat_variants):
	self.source = None
	# reflects the source ID for a flow in the graph
	self.target = None
	# reflects the target ID for a flow in the graph
	self.nodes = nodi
	# reflects the graph's nodes (potential sources and targets)
	self.bw = None
	self.lat = None
	self.bw_variants = bw_variants
	self.lat_variants = lat_variants
	self.x=0
	self.path=[]
	self.paths_pack=[]
	self.priority=None
	self.group=None
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
    def set_paths_pack(self,pack2set):
	self.paths_pack=pack2set
    def get_priority(self):
	return self.priority
    def set_priority(self,priority2set):
	self.priority=priority2set
    def get_group(self):
	return self.group
    def set_group(self,group2set):
	self.group=group2set

    # random choice of two distinct graph nodes as source / target
    def make_choice(self):
	self.bw=random.choice(self.bw_variants)
	self.lat=random.choice(self.lat_variants)
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
