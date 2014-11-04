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

    # random choice of two distinct graph nodes as source / target
    def make_choice(self):
	self.bw=random.choice(self.bw_variants)
	self.lat=random.choice(self.lat_variants)
	temp_n=self.nodes
	self.source = random.choice(temp_n)
	source_index = temp_n.index(self.source)
	temp_n.pop(source_index)
	self.target = random.choice(temp_n)
	print '\nDemand: '
	print 'Path to find: '+str(self.source)+' ==> '+str(self.target)
	print "bw req: "+str(self.bw)
	print "lat req: "+str(self.lat)

    # sets user source and target according to user definition
    def make_choice_concrete(self,x,y):
	self.bw=random.choice(self.bw_variants)
	self.lat=random.choice(self.lat_variants)
	self.source = x
	self.target = y
	print '\nDemand: '
	print 'Path to find: '+str(self.source)+' ==> '+str(self.target)
	print "bw req.: "+str(self.bw)
	print "lat req: "+str(self.lat)
