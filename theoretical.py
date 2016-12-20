# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 11:36:27 2016

@author: liang.kuang
"""
import Quandl
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
matplotlib.style.use('ggplot')

date1 = datetime.datetime.today()
delta = relativedelta(years=1)
date2 = date1 + delta*21

dates = [date1 + n*delta for n in np.arange(21)]

principle = 1000

assumedStockRate1 = 10*[0.1,-0.1]
assumedStockRate1.insert(0,0)
assumedStockRate2 = 10 * [0.2,-0.1]
assumedStockRate2.insert(0,0)
assumedIULRate1 = 10 * [0.1,0.0075]
assumedIULRate2 = 10 * [0.15,0.0075]
assumedIULRate1.insert(0,0)
assumedIULRate2.insert(0,0) 
#datelist = pd.date_range(pd.datetime(2000,1,1),pd.datetime(2020,1,1),period=10).tolist()
stockReturnList1 = np.zeros(21)
stockReturnList2 = np.zeros(21)
stockReturnList1[0] = principle
stockReturnList2[0] = principle

IULReturnList1 = np.zeros(21)
IULReturnList2 = np.zeros(21)
IULReturnList1[0] = principle
IULReturnList2[0] = principle

for i in np.arange(1,21):
    stockReturnList1[i] =stockReturnList1[i-1] * (1+assumedStockRate1[i])
    stockReturnList2[i] =stockReturnList2[i-1] * (1+assumedStockRate2[i])
    IULReturnList1[i] = IULReturnList1[i-1] * (1+assumedIULRate1[i])
    IULReturnList2[i] = IULReturnList2[i-1] * (1+assumedIULRate2[i])
# %%    
h1 = plt.figure(1,figsize=(12,8),dpi=120)
h1.clf()
ax1 = plt.subplot(221)
plt.plot_date(dates,assumedStockRate1,'r--',label='stock1 ROI')
plt.plot_date(dates,assumedStockRate2,'r',label='stock2 ROI')
plt.title('Hypothetical Rate of Investment for Stocks',fontsize = 10)
ax1.legend(loc='best')
ax1.set_ylim([-0.3,0.3])
plt.setp(ax1.get_xticklabels(),visible=False)

ax2 = plt.subplot(222)
plt.plot_date(dates,assumedIULRate1,'g--',label='IUL1 ROI')
plt.plot_date(dates,assumedIULRate2,'g',label='IUL2 ROI')
plt.title('Hypothetical Rate of Investment for IUL',fontsize = 10)
ax2.legend(loc='best')
ax2.set_ylim([-0.3,0.3])
plt.setp(ax2.get_xticklabels(), visible =False)


ax3 = plt.subplot(223)
plt.plot_date(dates,stockReturnList1,'r--',label='stock1 return')
plt.plot_date(dates,stockReturnList2,'r-',label='stock2 return')
plt.title('Return of Investment (Stock)',fontsize = 10)
ax3.legend(loc='best')
ax3.set_ylim([0,5000])


ax4 = plt.subplot(224)
plt.plot_date(dates,IULReturnList1,'g--',label='IUL1 return')
plt.plot_date(dates,IULReturnList2,'g',label='IUL2 return')
plt.title('Return of Investment (IUL)',fontsize = 10)
ax4.legend(loc='best')
ax4.set_ylim([0,5000])
plt.savefig('Hypothetical_run')





    
    
    
