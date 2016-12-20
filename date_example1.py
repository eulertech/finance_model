# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 22:19:45 2016

@author: liang
"""

import datetime
import matplotlib.pylab as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange

date1 = datetime.datetime(2000,3,2)
date2 = datetime.datetime(2000,3,6)
delta = datetime.timedelta(hours = 6)

dates=drange(date1, date2, delta)

y = arange(len(dates)*1.0)

fig, ax = plt.subplots()
ax.plot_date(dates,y*y)

ax.set_xlim(dates[0], dates[-1])
ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(arange(0,25,6)))
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()
plt.show()




