#!/usr/bin/python

##### imports #####
from gurobipy import *
import demand as dem
import customGraph as gc
import lpsolv as lp

##### parameters #####
number_of_demands		= 3
graph_type			= 'deight'
bw_variants			= [1]
lat_variants			= [10]

##### produce graph #####
# produce graph and convert to digraph
G=gc.make(graph_type)
H=G.to_directed()

# create all demands
d_list=[]
for k in range(number_of_demands):
	temp_dem = dem.demand(H.nodes(),bw_variants,lat_variants)
	temp_dem.make_choice()
	d_list.append(temp_dem)

# convert to gurobi graph

[result,accepted,rejected,ratio,x_sol, P_sol] = lp.solve(H, d_list)
