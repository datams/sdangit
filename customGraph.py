import networkx as nx


def make(name):
	if name=='eight':
		G=nx.Graph()

		# add nodes and edges to the graph
		G.add_edge(0,1, bw=5, lat=1)
		G.add_edge(0,2, bw=5, lat=1)
		G.add_edge(1,3, bw=5, lat=0.4)
		G.add_edge(2,3, bw=5, lat=1)
		G.add_edge(3,4, bw=5, lat=1)
		G.add_edge(3,5, bw=5, lat=0.2)
		G.add_edge(4,6, bw=5, lat=0.5)
		G.add_edge(5,6, bw=5, lat=1)
	return G
