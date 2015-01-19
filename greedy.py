import graphFunctions as gf
import lpsolv as lp
import copy

def finder(G, G_updated, d_list, number_of_demands, i, plot_pool, path_selection_criterion, \
	number_of_rerouting_attempts, number_of_rerouting_success, plot_enable, n_LP):
	##### TRY TO FIND PATH FOR D_N AND ALLOCATE #####
	[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[i],path_selection_criterion)
	# if successful, plot the chosen path
	if sel_path!=[]:
		plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
	
	##### CONSIDER REROUTE #####
	else:
		##### LOOK FOR D_N PATH IN EMPTY GRAPH  #####
		print 'No path found for d_n, consider rerouting\n'
		# check if demand could be allocated in empty graph
		path_pack_in_empty_graph=gf.shortest_p(G,d_list[i].get_source(),d_list[i].get_target(),d_list[i].get_lat())
		print 'path_pack for empty graph: '+str(path_pack_in_empty_graph)

		old_reroute=False
		new_reroute=True
		##### D_N NOT POSSIBLE EVER #####
		if path_pack_in_empty_graph == []:
			# demand can never be allocated
			print 'There is really no path for this demand, no chance!'
			plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
		elif new_reroute:
			#### FIND BEST PATH FOR D_N IN EMPTY GRAPH #####
			print 'Start rerouting attempt'
			number_of_rerouting_attempts+=1
			# plot d_n e.g. the current demand, which no path could be found for
			plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
			# calculate best path p_n for d_n in empty graph
			optimal_path = gf.select_path(path_pack_in_empty_graph, path_selection_criterion)
			print 'The best path for empty graph: '+str(optimal_path)
			#### FIND D_U TO REROUTE #####
			# get all demands, whose path intersect with optimal path by at least one and are not blocked
			#d_u=gf.find_all_d_to_reroute(optimal_path, d_list[i].bw, d_list)
			#d_u=gf.find_all_d_to_reroute2(optimal_path, G_updated, d_list[i].bw, d_list)
			d_u=gf.find_all_d_to_reroute(optimal_path, G_updated, d_list[i].bw, d_list)
			print 'all d_u: '+str(d_u)
			# solve subproblem of [d_n and all d_u] in G_updated
			if d_u!=[]:
				# bound the number of d_u for LP
				number_of_du_bound=n_LP
				d_u=d_u[:number_of_du_bound]
				d_index_subset = d_u + [i]
				d_list_subset = [d_list[j] for j in d_index_subset]
				# produce graph without d_u's
				G_without_du=G_updated.copy()
				d_list_du=copy.deepcopy(d_list)
				for index in d_u:
					[G_without_du] = gf.dealloc(G_without_du, d_list_du[index])
				# LP solver for the sub problem
				lp_sel_paths=lp.solve(G_without_du,d_list_subset)[1]
				print '\n\nlp_sel_paths: '+str(lp_sel_paths)+'\n\n'
				# if path_found_for_all OR (path not found for all) but the demands_without_path_are_cancellable: go
				# therefore: nothing (blocked) live gets rerouted and reroutables don't get terminated
				# decision variables
				'''
				path_found_for_all=len(lp_sel_paths)==len(d_list_subset)
				demands_without_path_are_cancellable=True
				subproblem_d_index_path_found=lp_sel_paths.keys()
				d_index_path_found=[d_index_subset[i] for i in subproblem_d_index_path_found]
				for index in d_index_subset:
					if index not in d_index_path_found:
						if d_list[index].status!=0
							demands_without_path_are_cancellable=False
				if len(lp_sel_paths)==len(d_list_subset):
				'''
				# if path found for all: allocate
				if len(lp_sel_paths)==len(d_list_subset):
					number_of_rerouting_success+=1
					# dealloc d_u's
					for index in d_u:
						print 'd_u: '+str(d_u)+' zum dealloc'
						print 'index: '+str(index)
						print 'd_list[index].path '+str(d_list[index].source )
						plot_pool.plot(G_updated, d_list[index], 2, plot_enable)
						[G_updated] = gf.dealloc(G_updated, d_list[index])
						plot_pool.plot(G_updated, d_list[index], 2, plot_enable)
					# alloc rerouting solution
					for u in d_index_subset:
						print 'u='+str(u)
						print 'pfad ist: '+str(lp_sel_paths[d_index_subset.index(u)][0])
						[G_updated, sel_path]=gf.alloc_p(G_updated, d_list[u], lp_sel_paths[d_index_subset.index(u)][0])
						if sel_path==[]:
							print 'nicht gegangen'
						plot_pool.plot(G_updated, d_list[u], 3, plot_enable)
				else:
					print 'not possible to allocate all by rerouting'
			else:
				print 'no alternatives - not possible to allocate by rerouting'












		elif old_reroute:
			#### FIND BEST PATH FOR D_N IN EMPTY GRAPH #####
			print 'Start rerouting attempt'
			number_of_rerouting_attempts+=1
			# plot d_n e.g. the current demand, which no path could be found for
			plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
			# calculate best path p_n for d_n in empty graph
			optimal_path = gf.select_path(path_pack_in_empty_graph, path_selection_criterion)
			print 'The best path for empty graph: '+str(optimal_path)
			#### FIND D_U TO REROUTE #####
			# get all demands, whose path intersect with optimal path by at least one and are not blocked and would release enough bw and the most alternatives
			# IF A CERTAIN D_U REALLY WOULD RELEASE ENOUGH BANDWIDTH SHOULD ACTUALLY BE CHECKED ON EACH EDGE...... YET TO DO, IF NEEDED
			d_u=gf.find_d_to_reroute(optimal_path, d_list[i].bw, d_list)
			if d_u!=None:
				#### DEALLOCATE D_U #####
				print 'Found d_u: '+str(d_list[d_u].source)+' ==> '+str(d_list[d_u].target)+' demand Nr.'+str(d_u)
				# plot path to be deallocated
				plot_pool.plot(G_updated, d_list[d_u], 2, plot_enable)
				# store old d_u path
				old_p_u=d_list[d_u].path
				# deallocate d_u
				print 'Deallocate d_u'
				[G_updated] = gf.dealloc(G_updated, d_list[d_u])
				# plot deallocated graph
				plot_pool.plot(G_updated, None, 2, plot_enable)
				#### TRY TO ALLOCATE D_N #####
				print 'Try to allocate d_n'
				[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[i],path_selection_criterion)
				#### if no success #####
				# If no path for d_n found after deallocation of d_u, allocate d_u again
				if sel_path==[]:
					[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[d_u],path_selection_criterion)
				#### if success #####
				else:
					print 'Allocated d_n'
					plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
					#### TRY TO ALLOCATE D_U again #####
					print 'Try to allocate d_u'
					[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[d_u],path_selection_criterion)
					if sel_path!=[]:
						# if success, plot
						number_of_rerouting_success+=1
						print 'Successful rerouting of d_u to '+str(sel_path)
						plot_pool.plot(G_updated, d_list[d_u], 3, plot_enable)
					else:
						# if no success, go back if priority of d_u higher than d_n
						print 'Not possible to reroute d_u'
						if d_list[d_u].priority > d_list[i].priority:
							print 'Roll back because d_u has priority: '+str(d_list[d_u].priority)+' and d_n has: '+str(d_list[i].priority)
							# deallocate d_n
							[G_updated] = gf.dealloc(G_updated, d_list[i])
							print 'deallocated d_n again'
							[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[d_u],path_selection_criterion)
							print 'allocated d_u again'
							if sel_path==[]:
								print 'for some reason, d_u could not be rolled back...'
			else:
				print 'There was no rerouting alternative'





			


	return [G_updated, plot_pool, number_of_demands, number_of_rerouting_attempts, number_of_rerouting_success]
