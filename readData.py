import matplotlib.pyplot as plt
import pandas as pd
from pmdarima.arima.auto import auto_arima
import statsmodels.api as sm
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
                           max_p=3, max_q=3, m=7,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=False,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
#print(stepwise_model.aic())
#print(stepwise_model.order)
#print(stepwise_model.seasonal_order)

model = sm.tsa.statespace.SARIMAX(dailySales,
                                order=stepwise_model.order,
                                seasonal_order=stepwise_model.seasonal_order,
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = model.fit()

#print(results.summary().tables[1])

pred = results.get_prediction(start=pd.to_datetime('2017-01-01'), dynamic=False)
pred_ci = pred.conf_int()
print(pred_ci)
plt.figure()
ax = dailySales['2016':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Date')
ax.set_ylabel('Sales')
plt.legend()
plt.savefig('Forecast.png')
plt.show()