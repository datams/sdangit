import graphFunctions as gf

def finder(G, G_updated, d_list, number_of_demands, i, plot_pool, path_selection_criterion, \
	number_of_rerouting_attempts, number_of_rerouting_success, plot_enable):
	# try to find and allocate path in graph	
	[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[i],path_selection_criterion)

	# if successful, plot the chosen path
	if sel_path!=[]:
		plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
	
	##### CONSIDER REROUTE #####
	else:
		print 'No path found, looking now at previous allocations..\n'
		# check if demand could be allocated in empty graph
		path_pack_in_empty_graph=gf.shortest_p(G,d_list[i].get_source(),d_list[i].get_target(),d_list[i].get_lat())
		
		##### D_N NOT POSSIBLE EVER #####
		if path_pack_in_empty_graph == []:
			# demand can never be allocated
			print 'There is really no path for this demand, no chance!'
		else:
			#### FIND D_N TO REROUTE #####
			# plot d_n e.g. the current demand, which no path could be found for
			plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
			# calculate best path p_n for d_n in empty graph
			optimal_path = gf.select_path(path_pack_in_empty_graph, path_selection_criterion)
			print 'The best path in the empty graph would be: '+str(optimal_path)
			# find the shoretst intersection (but it must intersect! thresh=1) path of optimal path
		 	# with previous allocated paths p_u (according to d_u)			
			shortest_intersect=gf.check_setintersect(optimal_path, gf.sel_paths(d_list).values(),1)
			print 'having the shortest intersection path: '\
			+'of optimal path with previous allocated paths p_u (according to d_u) '+str(shortest_intersect)

			# if intersections found, try to reroute
			if shortest_intersect!=[]:
				# find critical (corresponding) demand
				for k in range(len(d_list)):
					if d_list[k].path == shortest_intersect:			
						d_u=k

				# look for paths for d_u that do not intersect with optimal_path
				d_u_paths=gf.pack2p(d_list[d_u].paths_pack)
				# remove already taken path
				d_u_paths.pop(d_u_paths.index(d_list[d_u].path))
				#### REROUTE #####
				if len(d_u_paths)>0:
					print 'corresponds to demand nr: '+str(d_u)+' to: '+str(d_list[d_u].source)+' ==> '+str(d_list[d_u].target)
					print 'which has the following alternative paths stored: '+str(d_u_paths)
					p_u=gf.check_setintersect(optimal_path, d_u_paths,0)
					print 'the least intersecting with p_n of d_n is '+str(p_u)
					# plot path to be deallocated
					plot_pool.plot(G_updated, d_list[d_u], 2, plot_enable)
					number_of_rerouting_attempts+=1
					# store old d_u path
					old_p_u=d_list[d_u].path
					# deallocate d_u
					[G_updated] = gf.dealloc(G_updated, d_list[d_u])
					# plot un-allocated graph
					plot_pool.plot(G_updated, None, 2, plot_enable)
					# allocate d_u with new path p_u
					print 'allocate d_u with new path p_u: '+str(p_u)
					[G_updated, sel_path] = gf.alloc_p(G_updated, d_list[d_u], p_u)

					# check if it was possible to allocate p_u without having negative bw
					if sel_path!=[]:
						print 'successful rerouting of p_u'
						# plot d_u with p_u allocated path
						plot_pool.plot(G_updated, d_list[d_u], 3, plot_enable)
					
						# try to allocate d_n
						[G_updated, paths_pack, sel_path]=gf.alloc(G_updated,d_list[i],path_selection_criterion)
						if paths_pack!=[]:
							number_of_rerouting_success+=1
							print 'successful routing of p_n'
						else:
							print 'not possible to allocate p_n'
							print 'roll back d_u'
							[G_updated, sel_path] = gf.alloc_p(G_updated, d_list[d_u], old_p_u)
							plot_pool.plot(G_updated, d_list[d_u], 3, plot_enable)
						# plot d_n
						plot_pool.plot(G_updated, d_list[i], 1, plot_enable)
						#### REVERT IF NO SUCCESS aber auch nur dann, wenn nicht etwa die priority hoeher ist bei d_n!! #####
					else:
						print 'rerouting was not possible, p_u was not allocatable'
						print 'roll back d_u'
						[G_updated, sel_path] = gf.alloc_p(G_updated, d_list[d_u], old_p_u)
						plot_pool.plot(G_updated, d_list[d_u], 3, plot_enable)
			else:
				print 'there was no rerouting alternative'

	return [G_updated, plot_pool, number_of_demands, number_of_rerouting_attempts, number_of_rerouting_success]