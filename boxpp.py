## main source http://blog.bharatbhole.com/creating-boxplots-with-matplotlib/
## numpy is used for creating fake data
import numpy as np
import matplotlib as mpl
import time

def plot(lpt,gnt,title):
	## agg backend is used to create plot as a .png file

	mpl.use('agg')

	import matplotlib.pyplot as plt

	## Create data
	'''
	np.random.seed(10)
	collectn_1 = np.random.normal(100, 10, 200)
	collectn_2 = np.random.normal(80, 30, 200)
	collectn_3 = np.random.normal(90, 20, 200)
	collectn_4 = np.random.normal(70, 25, 200)
	

	lpt=[2,1,4,34,14,5,24,2,23,23,13,23,5,56,13,4,56,34,46,1,5,25,26,4,26,235,235]
	lpt=[0.1*i for i in lpt]
	gnt=[12,2,35,1,5,4,2,31,5,3,2,1,5,4,2,3,5,5,5,232,1,5,4,2,32,54,58]*10
	gnt=[0.1*i for i in gnt]
	'''

	print 'boxx got lpt values:'
	print lpt

	print 'boxx got gnt values:'
	print gnt

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
	ax.set_xticklabels(['LP Gurobi', 'Genetic Algorithm'])

	## Remove top axes and right axes ticks
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

	## Title
	ax.set_title(title)

	# Save the figure
	time_now= (time.strftime("%H%M%S"))
	date_now= (time.strftime("%d%m%Y"))
	filename=title+'_'+date_now+'_'+time_now
	fig.savefig(filename, bbox_inches='tight')

	print 'Boxplot done.'


