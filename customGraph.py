import networkx as nx


def make(name):
	if name=='eight':
		G=nx.Graph()

		# add nodes and edges to the graph
		G.add_edge(0,1, bw=3, lat=1)
		G.add_edge(0,2, bw=3, lat=1)
		G.add_edge(1,3, bw=3, lat=1)
		G.add_edge(2,3, bw=3, lat=1)
		G.add_edge(3,4, bw=3, lat=1)
		G.add_edge(3,5, bw=3, lat=1)
		G.add_edge(4,6, bw=3, lat=1)
		G.add_edge(5,6, bw=3, lat=1)
		return G

	elif name=='deight':
		G=nx.Graph()

		# add nodes and edges to the graph
		G.add_edge(0,1, bw=4, lat=1)
		G.add_edge(0,2, bw=4, lat=1)
		G.add_edge(1,3, bw=8, lat=1)
		G.add_edge(2,3, bw=4, lat=1)
		G.add_edge(3,4, bw=4, lat=1)
		G.add_edge(3,5, bw=10, lat=1)
		G.add_edge(4,6, bw=4, lat=1)
		G.add_edge(5,6, bw=4, lat=1)
		G.add_edge(1,4, bw=4, lat=1)
		return G

	elif name=='diamond':
		G=nx.Graph()

		# add nodes and edges to the graph
		G.add_edge(0,1, bw=1, lat=1)
		G.add_edge(0,2, bw=1, lat=1)
		G.add_edge(2,3, bw=1, lat=1)
		G.add_edge(1,3, bw=1, lat=1)
		return G

	elif name=='richer1':
		G=nx.Graph()
		# add nodes and edges to the graph
		G.add_edge(0, 1, bw=1, lat=5)
		G.add_edge(0, 2, bw=1, lat=5)
		G.add_edge(2, 13, bw=1, lat=2)
		G.add_edge(13, 14, bw=1, lat=4)
		G.add_edge(14, 12, bw=1, lat=8)
		G.add_edge(12, 3, bw=1, lat=4)
		G.add_edge(3, 2, bw=1, lat=3)
		G.add_edge(3, 1, bw=1, lat=10)
		G.add_edge(1, 4, bw=1, lat=10)
		G.add_edge(1, 10, bw=1, lat=8)
		G.add_edge(10, 11, bw=1, lat=2)
		G.add_edge(11, 8, bw=1, lat=3)
		G.add_edge(8, 4, bw=1, lat=5)
		G.add_edge(4, 3, bw=1, lat=11)
		G.add_edge(4, 6, bw=1, lat=4)
		G.add_edge(8, 9, bw=1, lat=5)
		G.add_edge(9, 7, bw=1, lat=10)
		G.add_edge(6, 7, bw=1, lat=6)
		G.add_edge(6, 5, bw=1, lat=4)
		G.add_edge(7, 5, bw=1, lat=7)
		G.add_edge(7, 12, bw=1, lat=14)
		G.add_edge(5, 3, bw=1, lat=5)
		return G
	
	elif name=='srg':
		G=nx.Graph()

		# add nodes and edges to the graph
		# bw: line thickness
		# latency unit: 10e-4 seconds (geo distance / light)
		G.add_edge(1,2, bw=5, lat=2.515)
		G.add_edge(1,4, bw=5, lat=4.591)
		G.add_edge(1,9, bw=5, lat=1.317)
		G.add_edge(2,11, bw=5, lat=2.076)
		G.add_edge(2,10, bw=5, lat=0.897)
		G.add_edge(2,7, bw=5, lat=3.162)
		G.add_edge(2,15, bw=5, lat=1.333)
		G.add_edge(2,3, bw=15, lat=3.207)
		G.add_edge(2,6, bw=15, lat=5.182)
		G.add_edge(3,12, bw=5, lat=1.033)
		G.add_edge(3,16, bw=15, lat=0.922)
		G.add_edge(4,16, bw=15, lat=1.708)
		G.add_edge(8,14, bw=5, lat=1.69)
		G.add_edge(14,5, bw=5, lat=3.574)
		G.add_edge(13,4, bw=5, lat=2.819)
		G.add_edge(4,5, bw=5, lat=1.685)
		G.add_edge(4,6, bw=15, lat=6.258)
		G.add_edge(5,17, bw=5, lat=4.303)
		G.add_edge(17,2, bw=5, lat=3.236)
		G.add_edge(5,19, bw=5, lat=3.102)
		G.add_edge(5,18, bw=5, lat=2.368)
		G.add_edge(19,20, bw=5, lat=1.634)
		G.add_edge(20,6, bw=5, lat=2.702)
		G.add_edge(6,21, bw=5, lat=0.733)
		G.add_edge(6,7, bw=5, lat=3.496)
		G.add_edge(6,11, bw=5, lat=5.41)
		G.add_edge(6,15, bw=5, lat=3.866)
		return G
	else:
		print 'entered graph type unknown'


node2city={1: 'Basel', 2: 'Zurich', 3: 'Bern', 4: 'Lausanne', 5: 'Genf', 6: 'Lugano', 7: 'Chur', 8: 'Delemont', 9: 'Aarau', 10: 'Rapperswil', 11: 'St. Gallen', 12: 'Solothurn', 13: 'Biel', 14: 'Neuenburg', 15: 'Luzern', 16: 'Friburg', 17: 'Thun', 18: 'Martigny', 19: 'Sion', 20: 'Brig', 21: 'Locarno'}


