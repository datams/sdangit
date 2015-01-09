#!/usr/bin/env python

######################## python imports ############################
import networkx as nx
import random
import copy
import pygraphviz
import os
import time

####################### modules imports ############################
import demand as dem
import customGraph
import graphFunctions as gf
import lpsolv as lp
import greedy as gr
import genetic2 as gen
import gen_param as gp
import demandset as ds

########################## parameters ##############################


########################## experiment ##############################

# demand creation
d_list = ds.get_d_list('srg')


