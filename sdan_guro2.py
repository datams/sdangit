#!/usr/bin/python

##### imports #####
from gurobipy import *
import demand as dem
import customGraph as gc
print chr(27) + "[2J"

##### functions #####
def new_request(s2set, t2set, bw2set, lat2set, s ,t ,bw_r ,lat_r ,Requests):
	a=len(Requests)+1
	Requests.append(a)
	s[a]=s2set
	t[a]=t2set
	bw_r[a]=bw2set
	lat_r[a]=lat2set
	return s,t,bw_r,lat_r,Requests

##### produce graph #####
G=gc.make('eight')
H=G.to_directed()
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

# create all demands
number_of_demands=3
bw_variants=[1]
lat_variants=[10]
d_list=[]
Requests=[]
s={}
t={}
bw_r={}
lat_r={}
for k in range(number_of_demands):
	temp_dem = dem.demand(H.nodes(),bw_variants,lat_variants)
	temp_dem.make_choice()
	d_list.append(temp_dem)
	Requests.append(k)
	s[k]=str(temp_dem.source)
	t[k]=str(temp_dem.target)
	bw_r[k]=temp_dem.bw
	lat_r[k]=temp_dem.lat

for r in Requests:
	print 'Request: '+str(r)+' from '+str(s[r])+' to '+str(t[r])+' with bw_r '+str(bw_r[r])+' and lat_r '+str(lat_r[r])
print '\n'



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

##### Print solution ##### 

# Check if all bw_e constraints are held
all_bw_hold=True
for e,w in edges:
	for r in Requests: 
		ca = bw_e[e,w]
		pa = bw_r[r]*[P[r,e,w]][0].x
		if not ca>=pa:
			all_bw_hold=False
print '\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
print '\nAll bw constraints held: '+str(all_bw_hold)
print('acceptance: %g \n' % acceptance.getValue())

for v in m.getVars():
	if v.varName.startswith('x'):
		print 'Status request '+str(v.varName)+' '+str(v.x)
	if v.varName.startswith('P') and v.x > 0:
		print 'Taken pathlet '+str(v.varName)+' '+str(v.x)

paths={}
for r in Requests:
	temp_path=[]
	for v in m.getVars():
		varName=v.varName
		varValue=v.x
		if varName.startswith('P'+str(r)) and varValue==1:
	    		from_node=str(varName[3])
			to_node=str(varName[5])
			temp_path.append((from_node,to_node))
	paths[r, s[r], t[r]]=temp_path

print '\n'
for r in Requests:
	e_list=tuplelist(paths[r, s[r], t[r]])
	pp=[]
	temp_edge= e_list.select(s[r],'*')[0]
	pp.append(temp_edge[0])
	pp.append(temp_edge[1])
	for j in range(1,len(e_list)):
		temp_edge= e_list.select(pp[j],'*')[0]
		pp.append(temp_edge[1])
	print 'Request: '+str(r)+' from '+str(s[r])+' to '+str(t[r])+' has path '+str(pp)




