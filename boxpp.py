## main source http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
## numpy is used for creating fake data
import numpy as np
import matplotlib as mpl
import time

def plot(lpt, lp_ratio, gnt, gen_ratio, filename):
	## agg backend is used to create plot as a .png file

	mpl.use('agg')

	import matplotlib.pyplot as plt

	## data
	#print 'boxx got lpt values:'
	#print lpt
	#print 'boxx got gnt values:'
	#print gnt

	## combine these different collections into a list    
	data_to_plot = [lpt, gnt]

	# Create a figure instance
	fig = plt.figure(1, figsize=(9, 6))

	# Create an axes instance
	ax = fig.add_subplot(111)

	# Create the boxplot
	bp = ax.boxplot(data_to_plot)

	## add patch_artist=True option to ax.boxplot() 
	## to get fill color
	bp = ax.boxplot(data_to_plot, patch_artist=True)

	## change outline color, fill color and linewidth of the boxes
	for k in range(len(bp['boxes'])):
	    box=bp['boxes'][k]
	    # change outline color
	    box.set( color='#7570b3', linewidth=2)
	    box.set( facecolor = '#1b9e77' )
	    if k % 2 == 0:
	   	 box.set( facecolor = '#9e361b' )

	'''for box in bp['boxes']:
	    # change outline color
	    box.set( color='#7570b3', linewidth=2)
	    # change fill color
	    box.set( facecolor = '#1b9e77' )
	'''

	## change color and linewidth of the whiskers
	for whisker in bp['whiskers']:
	    whisker.set(color='#7570b3', linewidth=2)

	## change color and linewidth of the caps
	for cap in bp['caps']:
	    cap.set(color='#7570b3', linewidth=2)

	## change color and linewidth of the medians
	for median in bp['medians']:
	    median.set(color='#b2df8a', linewidth=2)

	## change the style of fliers and their fill
	for flier in bp['fliers']:
	    flier.set(marker='o', color='#e7298a', alpha=0.5)

	## Custom x-axis labels
	ax.set_xticklabels(['LP Gurobi '+str(round(lp_ratio,3)), 'Genetic Algorithm '+str(round(gen_ratio,3))], fontsize=20)

	## Remove top axes and right axes ticks
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	ax.set_ylabel('time [s]', fontsize=20)
	ax.set_xlabel('acc. ratio', fontsize=20)

	## Title
	ax.set_title(filename, fontsize=20)

	# Save the figure
	fig.savefig(filename, bbox_inches='tight')

	ax.set_yscale('log')

	fig.savefig(filename+'_log', bbox_inches='tight')

	print 'Boxplot done.'


