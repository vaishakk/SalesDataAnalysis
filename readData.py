import pandas as pd
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from pandas.plotting import autocorrelation_plot
import acf_plot as ap

ndays = [31,28,31,30,31,30,31,31,30,31,30,31]
dateParser = lambda x: pd.datetime.strptime(x,'%d-%m-%Y') if pd.notna(x) else nan
salesData = pd.read_excel('total12345.xls',skiprows = [0], usecols = ['date','maxtemp','mdsetotal'], parse_dates=['date'],date_parser=dateParser)#Read data from file
salesData.dropna(how = 'all',inplace = True)#Drop all empty rows
#print(salesData.columns.values)
salesData.columns = ['date','mdsetotal','maxtemp']#Change column names
salesData.set_index('date',inplace = True)
#print(salesData)
#print(salesData[pd.datetime.strptime('13-03-2016','%d-%m-%Y').strftime('%Y-%m-%d')])

dailySales = pd.Series(salesData.loc[:,'mdsetotal'],index = salesData.index)
weeklySales = dailySales.resample('W').mean()
monthlySales = dailySales.resample('M').mean()
#print(weeklySales.values)
#print(monthlySales.index)

ap.plotacf(weeklySales,'WeeklySales',show=False,save=True)
ap.plotacf(weeklySales,'MonthlylySales',show=False,save=True)
