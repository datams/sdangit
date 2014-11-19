##### imports #####
from gurobipy import *
import demand as dem
import customGraph as gc

# finds last occurence of el in li
def flast(li,el):
	l=None
	for j in range(len(li)):
		if li[j]==el:
			l=j
	return l

# removes loops out of list
def deloop(e_list):
	de_list=[]
	k=0
	maxk=len(e_list)-1
	while(True):
		currentElement=e_list[k]
		if e_list.count(currentElement)>1:
			lastPos=flast(e_list,currentElement)
			de_list.append(currentElement)
			k=lastPos+1
			if k>maxk:
				break
		else:
			de_list.append(currentElement)
			k+=1
			if k>maxk:
				break
	return de_list
	

def solve(G,d_list):

	# convert to a directed graph
	#H=G.to_directed()
	H=G

	number_of_demands=len(d_list)
	H_nodes=H.nodes()
	H_nodes=[str(n) for n in H_nodes]
	H_edges=H.edges()
	H_edges=[(str(e),str(w)) for e,w in H_edges]

	nodes = H_nodes
	bw_e={}
	lat_e={}
	for e,w in H_edges:
		bw_e[(e,w)]=H[int(e)][int(w)]['bw']
		lat_e[(e,w)]=H[int(e)][int(w)]['lat']
	edges = tuplelist(H_edges)

	# convert to gurobi requests
	Requests=[]
	s={}
	t={}
	bw_r={}
	lat_r={}
	for k in range(len(d_list)):
		Requests.append(k)
		s[k]=str(d_list[k].source)
		t[k]=str(d_list[k].target)
		bw_r[k]=d_list[k].bw
		lat_r[k]=d_list[k].lat

	# 4Debug: print requests
	#for r in Requests:
		#print 'Request: '+str(r)+' from '+str(s[r])+' to '+str(t[r])+' with bw_r '+str(bw_r[r])+' and lat_r '+str(lat_r[r])
	
	##### Create optimization model #####
	m = Model('sdan')

	# Create x[request_nr]=embedded boolean variable
	x = {}
	for r in Requests:
	    x[r] = m.addVar(vtype=GRB.BINARY, name='x%s' % (r))

	# Create P[request_nr, from_node, to_node]=part_of_sol boolean variables for in_edges
	P = {}
	for r in Requests:
	    for i,j in edges:
		P[r,i,j] = m.addVar(vtype=GRB.BINARY, name='P%s_%s_%s' % (r, i, j))

	# update variables
	m.update()

	# set maximize objective
	acceptance = quicksum(x[r] for r in Requests)
	m.setObjective(acceptance, GRB.MAXIMIZE)

	# subject to Nr 1
	for r in Requests:
		outgoing=quicksum(P[r,e,w] for e,w in edges.select(s[r],'*'))
		incoming=quicksum(P[r,e,w] for e,w in edges.select('*',s[r]))
		m.addConstr(x[r] == outgoing - incoming)

	# subject to Nr 2
	for r in Requests:
		for k in nodes:
			if k!=s[r] and k!=t[r]:
				outgoing=quicksum(P[r,e,w] for e,w in edges.select(k,'*'))
				incoming=quicksum(P[r,e,w] for e,w in edges.select('*',k))
				m.addConstr(0 == outgoing - incoming)

	# subject to Nr 3
	for e,w in edges:
		m.addConstr(bw_e[e,w] >= quicksum(bw_r[r]*[P[r,e,w]][0] for r in Requests))

	# subject to Nr 4
	for r in Requests:
		m.addConstr(lat_r[r] >= quicksum(lat_e[e,w]*[P[r,e,w]][0] for e,w in edges))

	##### Compute optimal solution ##### 
	m.optimize()

	# 4Debug: check solution
	'''	
	# Check if all bw_e constraints are held
	all_bw_held=True
	for e,w in edges:
		if (bw_e[e,w] < quicksum(bw_r[r]*[P[r,e,w]][0].x for r in Requests)):
			all_bw_hold=False
	print '\nAll bw constraints held: '+str(all_bw_held)

	# Check if all lat_e constraints are held
	all_lat_held=True
	for r in Requests:
		if (lat_r[r] < quicksum(lat_e[e,w]*[P[r,e,w]][0].x for e,w in edges)):
			all_lat_held=False
	print 'All lat constraints held: '+str(all_lat_held)
	'''

	##### Produce solution vars #####
	accepted=acceptance.getValue()
	rejected=number_of_demands-accepted
	ratio=float(accepted)/float(number_of_demands)

	x_sol={}
	for v in m.getVars():
		if v.varName.startswith('x'):
			x_sol[int(v.varName[1])]=float(v.x)

	paths={}
	for r in Requests:
		temp_path=[]
		for v in m.getVars():
			varName=v.varName
			varValue=v.x
			# get all P vars
			if varName.startswith('P'+str(r)) and varValue==1:
				P=varName
				# find underscore position 
				u1=P.find('_')
				u2=P.find('_', u1+1)
				u3=P.find('_', u2+1)
				# get node IDs
				from_node=str(P[u1+1:u2])
				to_node=str(P[u2+1:])
				temp_path.append((from_node,to_node))
		paths[r, s[r], t[r]]=temp_path
	# 4Debug: print paths
	# print 'paths '+str(paths)
	
	result=[]
	sel_paths={}
	for r in Requests:
		pp=[]
		e_list=tuplelist(paths[r, s[r], t[r]]) # select path for request and convert to tuplelist
		# 4Debug: print selected request with path
		#print 'r:'+str(r)+' s[r]:'+str(s[r])+' t[r]:'+str(t[r])+' paths[r, s[r], t[r]]:'+str(paths[r, s[r], t[r]])
		if e_list.select(s[r],'*')!=[]: # if there really is a path, continue
			temp_edge= e_list.select(s[r],'*')[0] # take start edge
			pp.append(temp_edge[0]) # write first node
			pp.append(temp_edge[1]) # write second node
			if temp_edge[1]!=t[r]:
				for j in range(1,len(e_list)): # write all other nodes
					temp_edge= e_list.select(pp[j],'*')[0] # select following edge
					pp.append(temp_edge[1]) # append second node of edge (first one has already been added before)
					# for the case the path has loops and not the full paths is taken
					# e.g. (2,3),(3,2),(2,0),(0,1),(1,4) the path could be shorter: [2,0,1,4] causing index error
					if pp[-1]==t[r]:
						break
			# 4Debug: print results (paths for demands)
			# print 'Request: '+str(r)+' from '+str(s[r])+' to '+str(t[r])+' has path '+str([int(z) for z in pp])
			# there could still be loops in the path which sould be deleted			
			pp=deloop(pp)
			result.append([int(z) for z in pp])
			sel_paths[(int(s[r]),int(t[r]))]=[int(z) for z in pp]

	return [result,sel_paths,accepted,rejected,ratio,x_sol]
