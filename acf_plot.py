import pandas as pd
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from pandas.plotting import autocorrelation_plot

def plotacf(data,parameter,show=True,save=False):
	#Set figure parameters
	rcParams['figure.figsize'] = 18, 9
	rcParams['figure.dpi'] = 200
	fig, ax1 = pyl.subplots()
	color = 'tab:red'
	ax1.set_xlabel('Date')
	####
	lns1 = ax1.plot(data.index.values, data.values, color=color,label='Sales')#Plot sales data
	if show:
		pyl.show()
	if save:
		pyl.savefig(parameter+'.png')
	#Calculate and plot acf
	plt.figure()
	autocorrelation_plot(data)
	if show:
		plt.show()
	if save:
		plt.savefig(parameter+'_Correlation.png')