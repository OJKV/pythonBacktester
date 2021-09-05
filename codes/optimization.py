import numpy as np
import pandas as pd
import pandas_datareader.data as web  
import datetime
import matplotlib.pyplot as plt
import math
from strategy2 import strategy
from main import * #setting period of study and ticker in main file


def optimization():
   
 print('What strategy you want to optimize')
 print('If you want to optimize Moving Averages, type "1"')
 print('If you want to optimize Filtering strategy, type "2"')
 t=int(input())
 
 
 
 if t == 1:
   l=int(input('type "1" if you want to optimize P&L, type "2" if you want to optimize Sharpe Ratio'))
   s1=int(input('Starting point for short MA'))
   s2=int(input('Ending point for short MA'))
   l1=int(input('Starting point for long MA'))
   l2=int(input('Ending point for long MA'))
   
   short=range(s1,s2)
   long=range(l1,l2)
   
   results_pnl=np.zeros((len(short),len(long)))#creating zero matrix for pnl values
   results_sharpe=np.zeros((len(short),len(long)))
   
   for i in short:
       for j in long:
           
           pnl, sharpe=s.ma(i,j)
           results_pnl[i-s1,j-l1]=pnl #filling pnl matrix; using first values of long and short ranges we model position of "i" for iteration 
           results_sharpe[i-s1,j-l1]=sharpe 

   
   
   if l ==1:# if user wants to optimize P%L
    plt.pcolor(short,long,results_pnl)
    plt.colorbar()
    plt.title('P&L')
    return plt.show()
   elif l==2:# if user wants to optimize Sharpe ratio
    plt.pcolor(short,long,results_sharpe)
    plt.colorbar()
    plt.title('Sharpe Ratio')    
    return plt.show()
   
  
 if t == 2:# if user wants to optimize Filtering strategy
   a=[0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01]# range of parameters for optimization; we use this list for iteration
   a2=np.array([0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01])# we use numpy array for pandas data frame
   
   s1=pd.Series(a2,name='parameters')#table of parameters
   df=pd.DataFrame(s1)#create pandas Dataframe
   results_pnl=np.zeros(len(a)) #zero matrix for pnl values
   results_sharpe=np.zeros(len(a))
   
   for i in range(len(a)):  
    pnl, sharpe=s.filtering(a[i])#implement filter class, calculating filtering  pnl and Sharpe ratio for every given parameter 
    results_pnl[i]=pnl #filling pnl matrix
    results_sharpe[i]=sharpe 
    
   s2=pd.Series(results_pnl,name='P&L') #creating pandas Series for pnl values
   s3=pd.Series(results_sharpe,name='Sharpe Ratio')
   df=df.join(s2)
   df3=df.join(s3)#table with pnl and Sharpe Ratios, joined together
   

   return df3




  
