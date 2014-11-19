#!/usr/bin/env python


f = open( 'newgraph', 'w' )


f.write("elif name=='richer1':\n")
f.write("\tG=nx.Graph()\n")
f.write("\t# add nodes and edges to the graph\n")

k=0
while(True):
	print '\nedge nr.'+str(k)+'\n(exit with s=888)'
	s=input('from: ')
	if s==888:
		break
	t=input('to: ')
	lat=input('lat: ')
	f.write('\tG.add_edge('+str(s)+', '+str(t)+', bw=1, lat='+str(lat)+')\n')
	k+=1

f.write('\treturn G\n')
f.close()




		
