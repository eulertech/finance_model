# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 20:11:47 2016

@author: liang
"""
import Quandl
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime
from datetime import timedelta
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

matplotlib.style.use('ggplot')
startTime = datetime.datetime.now()

class seed(object):
    def __init__(self,deposit,isDepleted,curBal,isParticipated,age):
        self.deposit = deposit
        self.isDepleted = isDepleted
        self.curBal = curBal
        self.stockBal = curBal
        self.isParticipated = isParticipated
        self.age = age
        
    def description(self):
            print ("I'm a seed with deposit of %f and current balance of %f." % (self.deposit, self.curBal))
            if(self.curBal>0) :
                print("I still have money left, Yeah!")
########
def costOfInsurance(time):
    COI = 100 * np.exp(0.05*time/12)
    return COI

def adjustDate(dateObj):
    if(dateObj.weekday()==5):
        dateObj = dateObj + timedelta(days=2)        
    elif (dateObj.weekday() == 6):
        dateObj = dateObj + timedelta(days=1)        
    else:
        dateObj = dateObj            
    return dateObj      

def findIndex(sp500,date):
    idx = 0
    for item_date in sp500.index:
        if item_date == date:
            return idx
        idx = idx + 1

def updateStatementDate(effectiveDate,t):
    months = np.concatenate([np.arange(effectiveDate.month,13),np.arange(1,effectiveDate.month)])
    yr = effectiveDate.year + int((t+effectiveDate.month-1)/12)
#    mo = effectiveDate.month + np.mod(t,12)
    mo = months[np.mod(t,12)]
    return datetime.datetime(yr,mo,effectiveDate.day)
 
def previousYear(date):
    oldYear = datetime.datetime(date.year-1,date.month,date.day)       
    return oldYear
#retrieve historical daily s&p index                        
#sp500 = Quandl.get("YAHOO/INDEX_GSPC")
sp500= pd.read_csv('YAHOO-INDEX_GSPC.csv',index_col=0,parse_dates=True)
#plt.figure(1,figsize=(5,5))
plt.close('all')
#f1, ax1 = plt.subplots()
sp500.plot(y='Close',figsize=(15,6))
plt.savefig('s&p 500 historical index')

#######input
mininum_rate = 0.0075
max_rate = 0.15
beginningBalance = 0
monthlyDeposit = 1000
effectiveDate = datetime.datetime(2000,4,8)  # Friday
stopDate = datetime.datetime(2013,1,5)  #Friday
effectiveDate = datetime.datetime(1995,1,2)  # Friday
stopDate = datetime.datetime(2016,4,1)  #Friday
#effectiveDate = datetime.datetime(2007,7,20)  # Friday
#stopDate = datetime.datetime(2009,3,10)  #Friday
#effectiveDate = datetime.datetime(1970,1,2)  # Friday
#stopDate = datetime.datetime(2016,4,2)  #Friday




# effectiveDate = input('Enter the effective date:')
# effectiveDate = 'Hello, {}!'.format(effectiveDate)
#adjust date to following Monday if it falls at weekend
effectiveDate = adjustDate(effectiveDate)
stopDate = adjustDate(stopDate)
numDeposits = (stopDate.year - effectiveDate.year-1) * 12 + (12-effectiveDate.month+1 + stopDate.month)

seedList = []
# initialize all object
for count in np.arange(numDeposits):
    x = seed(monthlyDeposit,False,0,False,0)
    x.curBal = x.curBal + x.deposit
    x.stockBal = x.stockBal + x.deposit
    seedList.append(x)

#account = [seed(500,False,0,False) for i in range(5)]
statementDateList = []
insuranceCostToDate = []
rateList = []
stockRateList = []
depositToDate = []
accumulatedDeposit = beginningBalance;
balanceArray = np.zeros(numDeposits)
stockReturnArray = np.zeros(numDeposits)

#Hypothesis 1: if there is an existing starting fund made on the effective date
seedList[0].curBal = seedList[0].curBal + beginningBalance

for t in np.arange(numDeposits):      #loop every month and update balance of each seed
    print("update the %d the month statement of toal %d periods" % (t,numDeposits) )
    statementDate = adjustDate(updateStatementDate(effectiveDate,t))
    print(statementDate)
    index = findIndex(sp500,statementDate)
    if(index is None):
        print(statementDate)
        while (index is None) :
            statementDate = adjustDate(statementDate + timedelta(days=1))
            index = findIndex(sp500,statementDate ) 
            print("New Statement Date is: %s" %statementDate)
            
    statementDateList.append(statementDate)
    seedList[t].age = statementDate
#    print("index located at %d" %index)
    sp500_now = sp500.ix[index].Close
    prevYear = adjustDate( previousYear(statementDate))
    index = findIndex( sp500, prevYear)

    if(index is None):
        print(statementDate)
        while (index is None) :
            prevYear = adjustDate(prevYear + timedelta(days=1))
            index = findIndex(sp500,prevYear ) 
            
    sp500_previous = sp500.ix[index].Close
    rate = (sp500_now - sp500_previous)/sp500_previous
    stockRateList.append(100*rate)
    if  rate <= mininum_rate:
        rate = mininum_rate
    else:
        rate = min(rate,max_rate)            
    rateList.append(100*rate)    
    print("Applied rate is %5.3f" %rate)
    
    # pay insurance premium first
    # get cost of insurance at current year defined in function costOfInsurance
    COI = costOfInsurance(t) * 0.0    
    insuranceCostToDate.append(COI)
    insuranceBal = COI
    #deposit array
    accumulatedDeposit = accumulatedDeposit + seedList[t].deposit
    depositToDate.append(accumulatedDeposit)
    # get s&p 500 now and 12 month ahead
    
    cnt = 0 
    while insuranceBal > 0 :  # may need to move out of loop n : 1 to t-1
        
        if(cnt > t):
            print("sorry, all your money is gone now :( :( BAD INVESTMENT!!")
            sys.exit()
        else:    
            if(seedList[cnt].curBal <= 0):
                print("Fund in seed %d is gone" %cnt)
            else:
                insuranceBal = COI - seedList[cnt].curBal
                seedList[cnt].curBal = seedList[cnt].curBal - COI
                seedList[cnt].curBal = seedList[cnt].curBal * ( np.sign(seedList[cnt].curBal) + 1 * abs(np.sign(seedList[cnt].curBal)) )/2
                print ("insuranceBal is %f" %insuranceBal)
                print("seed [%d].cubal is :%f" %(cnt,seedList[cnt].curBal))
                if(seedList[cnt].curBal <= 0):                    
                    seedList[cnt].isDepleted = True
                else:
                    seedList[cnt].isDepleted = False                        
        cnt = cnt + 1


    
    for n in np.arange(0,t+1):   #only one  series of seeds qualify for new balance update at each t statement (e.g. 1,13,25 etc)

        if(not seedList[n].isDepleted):
            if(t%12 == 0):
                seedList[n].isParticipated = True
            else:
                seedList[n].isParticipated = False
            
            seedList[n].curBal  = seedList[n].curBal +  seedList[n].curBal * rate * seedList[n].isParticipated
            balanceArray[t] = balanceArray[t] + seedList[n].curBal
#Stock performance use seed.deposit
    for m in np.arange(0,t+1):   #all qualified, no seed will go to zero 
        investDate =  seedList[m].age  #birthday per se
        sp500_rate_investDate = sp500.Close[investDate]
        stock_rate = (sp500_now - sp500_rate_investDate) / sp500_rate_investDate
        print("stock earning rate is %f" %stock_rate)
        stockReturnArray[t] = stockReturnArray[t] + seedList[m].stockBal * (1+stock_rate) 
# %% generate plots
index = findIndex(sp500,effectiveDate)
if(index is None): 
    while (index is None) :
        effectiveDate = adjustDate(effectiveDate + timedelta(days=1))
        index = findIndex(sp500,effectiveDate) 
     
startIndex = index

index = findIndex(sp500,stopDate)
if(index is None): 
    while (index is None) :
        stopDate = adjustDate(stopDate + timedelta(days=1))
        index = findIndex(sp500,stopDate) 
endIndex = index      
        
        
            
h2=plt.figure(2,figsize=(14,9),dpi=120)
h2.clf()        
ax1 = plt.subplot(311)
ax1.plot(sp500.index[startIndex:endIndex:-1],sp500.Close[startIndex:endIndex:-1])
plt.setp(ax1.get_xticklabels(),rotation=0, fontsize=8,visible=False)
plt.title('Historical S&P 500 Index', fontsize = 10)

ax2= plt.subplot(312)
ax2.plot(statementDateList,rateList,'g-',label='IUL')
ax2.plot(statementDateList,stockRateList,'r-',label='Stock Gap-12')
#ax2.set_ylim([-100,100])
legend = ax2.legend(loc='best',shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.90')
for label in legend.get_texts():
    label.set_fontsize('small')
for label in legend.get_lines():
    label.set_linewidth(1.0)    
plt.setp(ax2.get_xticklabels(),rotation=0, fontsize=8,visible=False)    
plt.title('Rate appplied by month (%)',fontsize = 10)
  
ax3=plt.subplot(313)
ax3.plot_date(statementDateList,balanceArray,'g-', label = 'IUL')
ax3.plot_date(statementDateList,depositToDate,'k-',mew=1,ms=2,linewidth='1',label = 'Principle')
ax3.plot_date(statementDateList,stockReturnArray, 'r-',mew=1,ms=2,linewidth='1', label = 'Stock Return') 
ax3.set_ylim( [int(balanceArray.min()), max(int(balanceArray.max()),depositToDate[-1],max(stockReturnArray))] )
legend=ax3.legend(loc='best', shadow = True)
frame = legend.get_frame()
frame.set_facecolor('0.90')
for label in legend.get_texts():
    label.set_fontsize('small')
for label in legend.get_lines():
    label.set_linewidth(1.0)    
    
plt.title('Balance,deposit and stock investment return over time ($)',fontsize=10)    
plt.show()
picname = str(monthlyDeposit)+'_HindcastSceN01_from_' + str(statementDateList[0])[0:10] + 'to_'+str(statementDateList[-1])[0:10]
plt.savefig(picname)
 
elapsedTime = datetime.datetime.now() - startTime
print("Total elapsed time is %s !" %elapsedTime)
                

