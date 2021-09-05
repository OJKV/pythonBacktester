import numpy as np
import pandas as pd
import pandas_datareader as web  
import datetime
import matplotlib.pyplot as plt 
import strategy2
import optimization
import plot

s=strategy2.strategy("^GSPC",2013,1,1,2017,1,1)
k=plot.plot("^GSPC",2005,1,1,2013,1,1)
 


pnl1,sharpe1=s.ma(22,58) #calculation of pnl and sharpe ratio for MA
pnl2,sharpe2=s.filtering(0.01)
pnl3,sharpe3=s.stochastic()
 

df=pd.DataFrame({'Sharpe Ratio':[sharpe1,sharpe2,sharpe3],
               'P&L':[pnl1,pnl2,pnl3]},
            index=['MA crossover','Filtering strategy', 'Stochastic'])#table of final results
 
print(df) 

 