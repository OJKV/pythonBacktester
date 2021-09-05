import numpy as np
import pandas as pd
import pandas_datareader.data as web  
import datetime
import matplotlib.pyplot as plt
import math

class strategy(object):

 def __init__(self, ticker, y1, m1, d1, y2, m2, d2):#choosing stock and period of backtesting, y1 - year of start date
    self.ticker=ticker
    self.y1=y1
    self.m1=m1
    self.d1=d1
    self.y2=y2
    self.m2=m2
    self.d2=d2

 def ma(self,s,l):

  start = datetime.datetime(self.y1,self.m1,self.d1)#start of the period
 
  end = datetime.datetime(self.y2,self.m2,self.d2)# end of the period

  dates=pd.date_range(start,end)#generate date values
  df1=pd.DataFrame(index=dates)# create pandas Dataframe indexed by dates; it can contain several different time-series, in our case stock series and its modifications
 


  stock = web.DataReader(self.ticker, "yahoo", start, end)
 

   

  stock['short']=np.round(stock['Adj Close'].rolling(window=s).mean(),2)#computing short MA
  stock['long']=np.round(stock['Adj Close'].rolling(window=l).mean(),2)

  #stock.tail(5)

  df1=df1.join(stock) #join stock time series to Dataframe




  condlist=[(stock['short']>stock['long'])&(stock['short'].shift()<stock['long'].shift()),(stock['short']<stock['long'])&(stock['short'].shift()>stock['long'].shift())]#Generating MA crossover signals
  choicelist=[1,-1]#  1 stands for buy, -1 stands for sell, and 0 in either case
  stock['signals']=np.select(condlist,choicelist)# generating buy and sell signals, the element of array is 1 when there is  short MA cross long MA  from below

  df1=df1.join(stock['signals'])
 
 
    
  

  prices=[] #list of future prices of buy and sell signals
  signals=[]
  returns=[]
  logreturns=[]
  s=0


  for i in range(0,len(df1)):     
     if df1.at[dates[i],'signals']==1 :
         signals.append(df1.at[dates[i],'signals'])#adding 1 to signals list if buy signal observed
         prices.append(df1.at[dates[i],'Adj Close'])#adding price of the stock to price list when buy signal observed               
         s=s+1
     if df1.at[dates[i],'signals']==-1 :
        signals.append(df1.at[dates[i],'signals'])
        prices.append(df1.at[dates[i],'Adj Close'])               
        s=s+1
         
     

  for i in range(0,len(signals)-1):#we can't employ n+1 or len(signals)+1

   if signals[i]==1:
      returns.append(prices[i+1]-prices[i]) #substract current price from future price to calculate returns(profit)  
      logreturns.append(math.log(prices[i+1]/prices[i])) # calculating log returns for sharpe ratio calculation


  

  pnl=0
  p=0
  n=0
 
  for i in range(0,len(returns)):
   pnl=pnl+returns[i]
  
   if returns[i]>0:
    p=p+1
   
   else:
    n=n+1
  
  sharpe_ratio=np.sqrt(252) * (np.mean(logreturns)) / np.std(logreturns)
  
  return pnl, sharpe_ratio
  

 def filtering(self,x):
  start = datetime.datetime(self.y1,self.m1,self.d1)
 
  end = datetime.datetime(self.y2,self.m2,self.d2)

  dates=pd.date_range(start,end)
  df1=pd.DataFrame(index=dates)
 
 
  stock = web.DataReader(self.ticker, "yahoo", start, end)
 
  df1=df1.join(stock)
 




  condlist=[(1-(stock['Adj Close']/stock['Adj Close'].shift()))>x,(1-(stock['Adj Close']/stock['Adj Close'].shift()))<-x]
  choicelist=[1,-1]# 1 stands for buy, -1 stands for sell
  stock['signals']=np.select(condlist,choicelist)

  df1=df1.join(stock['signals'])
 
 
  

  prices=[]
  signals=[]
  returns=[]
  logreturns=[]
  s=0


  for i in range(0,len(df1)):     
     if df1.at[dates[i],'signals']==1 :
         signals.append(df1.at[dates[i],'signals'])
         prices.append(df1.at[dates[i],'Adj Close'])               
         s=s+1
     if df1.at[dates[i],'signals']==-1 :
        signals.append(df1.at[dates[i],'signals'])
        prices.append(df1.at[dates[i],'Adj Close'])               
        s=s+1
         
     

  for i in range(0,len(signals)-1):#we can't employ n+1

   if signals[i]==1:
      returns.append(prices[i+1]-prices[i]) #substract current price from future price to calculate returns(profit)
      logreturns.append(math.log(prices[i+1]/prices[i])) # calculating log returns for sharpe ratio

    
  

  pnl=0
  p=0
  n=0
 
  for i in range(0,len(returns)):
   pnl=pnl+returns[i]
  



  sharpe_ratio=np.sqrt(252) * (np.mean(logreturns)) / np.std(logreturns)  
  return pnl, sharpe_ratio


 def stochastic(self):
     
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

  
  df1=df1.join(D) #dataframe for calling Adj Close values, for Prices array
  DD=df1.dropna() #dropping missing data
  s=0
  signals=[]
  prices=[]
  for i in range(1,len(D)):
        
   if D[i]>80 and D[i-1]<=80:
      s=1# signal for catching overbought area. if  s==1 , we expect indicator fall less than 50
         #it is in turn give us a signal for selling the asset     
   if s==1 and D[i]<50 and D[i-1]>=50: # if fals below 50
      signals.append(-1)
      prices.append(DD.iloc[i,5])#add Adj prices to the array when we have signal for selling, 
                                 # 5 stands for Adj close
      s=0
  
   if D[i]>20 and D[i-1]<=20:
      s=1# signal for catching overbought area. if  s==1 , we expect indicator fall less than 50
         #it is in turn give us a signal for selling the asset     
   if s==1 and D[i]>50 and D[i-1]<=50:#if rises above 50
      signals.append(1)
      prices.append(DD.iloc[i,5])
      s=0

  returns=[]
  logreturns=[]
  
  for i in range(0,len(signals)-1):#we can't employ n+1

   if signals[i]==1:
      returns.append(prices[i+1]-prices[i]) #substract current price from future price to calculate returns(profit)
      logreturns.append(math.log(prices[i+1]/prices[i])) # calculating log returns for sharpe ratio

    
  
  
  pnl=0
  p=0
  n=0
 
  for i in range(0,len(returns)):
   pnl=pnl+returns[i]
  
  if returns[i]>0:
    p=p+1
   
  else:
    n=n+1
   
  accuracy=p/(p+n)*100



  sharpe_ratio=np.sqrt(252) * (np.mean(logreturns)) / np.std(logreturns)  
  return pnl, sharpe_ratio


 