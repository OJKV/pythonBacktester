import numpy as np
import pandas as pd
import pandas_datareader.data as web  
import datetime
import matplotlib.pyplot as plt

class plot(object):

 def __init__(self, ticker, y1, m1, d1, y2, m2, d2):#choosing stock and period of backtesting, y1 - year of start date
    self.ticker=ticker
    self.y1=y1
    self.m1=m1
    self.d1=d1
    self.y2=y2
    self.m2=m2
    self.d2=d2

 def ma(self,s,l):

  start = datetime.datetime(self.y1,self.m1,self.d1)
 
  end = datetime.datetime(self.y2,self.m2,self.d2)

  dates=pd.date_range(start,end)
  df1=pd.DataFrame(index=dates)
 
 

  stock = web.DataReader(self.ticker, "yahoo", start, end)
 
  
   
  stock['short']=np.round(stock['Adj Close'].rolling(window=s).mean(),2)
  stock['long']=np.round(stock['Adj Close'].rolling(window=l).mean(),2)
  
  stock[['Adj Close','short','long']].plot(grid=True,figsize=(13,8))#employing plot function
  
  return plt.show()

 def stochastic(self):#check
     
  start = datetime.datetime(self.y1,self.m1,self.d1)
 
  end = datetime.datetime(self.y2,self.m2,self.d2)

  dates=pd.date_range(start,end)
  df1=pd.DataFrame(index=dates)
 
 

  stock = web.DataReader(self.ticker, "yahoo", start, end)
  
  df1=df1.join(stock)

 

  stock['LL']=np.round(stock['Low'].rolling(window=14).min(),2) #Min of last 14 values of Low
  stock['HH']=np.round(stock['High'].rolling(window=14).max(),2)#Max of last 14 of High
 
               
  stock['K']=100*(stock['Adj Close'][13:]-stock['LL'][13:])/(stock['HH'][13:]-stock['LL'][13:]) #calculating K

  df2=stock['K'].dropna() # drop missing data


  D=np.round(df2.rolling(window=3).mean(),2).dropna()# calcualtio of D by given formula; dropping mising data

  #stock['Adj Close'].plot(grid=True,figsize=(10,6))
  D.plot(grid=True,figsize=(13,8))
  
  return plt.show()   
