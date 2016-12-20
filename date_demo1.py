# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 20:35:19 2016

@author: liang
"""

import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ochl
from matplotlib.dates import YearLocator,MonthLocator,DateFormatter
import datetime

date1 = datetime.date(2005,1,1)
date2 = datetime.date(2015,4,12)

years = YearLocator()  #every year
months = MonthLocator() #every month
yearsFmt = DateFormatter('%Y')

quotes = quotes_historical_yahoo_ochl('AMZN',date1,date2)

if len(quotes) ==0: 
    raise SystemExit
    
dates = [q[0] for q in quotes]
opens = [q[1] for q in quotes]

fig,ax = plt.subplots()
ax.plot_date(dates,opens,'-')

#format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.autoscale_view()

# format the coords message box

def price(x):
    return '%1.2f' % x
    
ax.fmt_xdata = DateFormatter('%Y-%m-%d')
ax.fmt_ydata = price
ax.grid(True)

fig.autofmt_xdate()
plt.show()












