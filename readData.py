import pandas as pd
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from pandas.plotting import autocorrelation_plot

salesData = pd.read_excel('total12345.xls',skiprows = [0], usecols = ['date','maxtemp','mdsetotal'])#Read data from file
salesData.dropna(how = 'all',inplace = True)#Drop all empty rows
#print(salesData.columns.values)
salesData.columns = ['date','mdsetotal','maxtemp']#Change column names
#print(salesData)
#Set figure parameters
rcParams['figure.figsize'] = 18, 9
rcParams['figure.dpi'] = 200
fig, ax1 = pyl.subplots()
color = 'tab:red'
ax1.set_xlabel('Date')
####
lns1 = ax1.plot(salesData.loc[:,'date'], salesData.loc[:,'mdsetotal'], color=color,label='Sales')#Plot sales data
#Show and save plot
#pyl.show()
pyl.savefig('Sales.png')
#Plot acf
plt.figure()
autocorrelation_plot(salesData['mdsetotal'])
#plt.show()
plt.savefig('Correlation.png')