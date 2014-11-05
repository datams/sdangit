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
	
	elif name=='srf':
		G=nx.Graph()

		# add nodes and edges to the graph
		G.add_edge(1,2, bw=5, lat=2.515)
		G.add_edge(1,4, bw=5, lat=1)
		G.add_edge(1,3, bw=5, lat=0.4)
		G.add_edge(2,3, bw=5, lat=1)
		G.add_edge(3,4, bw=5, lat=1)
		G.add_edge(3,5, bw=5, lat=0.2)
		G.add_edge(4,6, bw=5, lat=0.5)
		G.add_edge(5,6, bw=5, lat=1)
		return G


{1: 'Basel', 2: 'Zürich', 3: 'Bern', 4: 'Lausanne', 5: 'Genf', 6: 'Lugano', 7: 'Chur', 8: 'Delemont', 9: 'Aarau', 10: 'Rapperswil', 11: 'St. Gallen', 12: 'Solothurn', 13: 'Biel', 14: 'Neuenburg', 15: 'Luzern', 16: 'Friburg', 17: 'Thun', 18: 'Martigny', 19: 'Sion', 20: 'Brig', 21: 'Locarno'}

#lat einheit 10e-4 sec speed of light
