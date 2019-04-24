import pandas as pd
import acf_plot as ap
from pmdarima.arima.auto import auto_arima
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

dateParser = lambda x: pd.datetime.strptime(x,'%d-%m-%Y') if pd.notna(x) else nan
salesData = pd.read_excel('total12345.xls',skiprows = [0], 
						 usecols = ['date','maxtemp','mdsetotal'], 
						 parse_dates=['date'],
						 date_parser=dateParser)#Read data from file
salesData.dropna(how = 'all',inplace = True)#Drop all empty rows
#print(salesData.columns.values)
salesData.columns = ['date','mdsetotal','maxtemp']#Change column names
salesData.set_index('date',inplace = True)
#print(salesData)
#print(salesData[pd.datetime.strptime('13-03-2016','%d-%m-%Y').strftime('%Y-%m-%d')])

dailySales = pd.Series(salesData.loc[:,'mdsetotal'],index = salesData.index)
weeklySales = dailySales.resample('W').mean()
monthlySales = dailySales.resample('M').mean()

result = seasonal_decompose(dailySales, model='multiplicative')
#print(result)
result.plot()
plt.savefig('SeasonalDecompose.png')
#print(weeklySales.values)
#print(monthlySales.index)

#ap.plotacf(weeklySales,'WeeklySales',show=False,save=True)
#ap.plotacf(monthlySales,'MonthlylySales',show=False,save=True)

stepwise_model = auto_arima(dailySales, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
print(stepwise_model.aic())