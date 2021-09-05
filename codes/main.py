import numpy as np
import pandas as pd
import pandas_datareader as web  
import datetime
import matplotlib.pyplot as plt
from strategy2 import strategy
from optimization import *
from plot import *
s=strategy("^GSPC",2013,1,1,2017,1,1)
k=plot("^GSPC",2005,1,1,2013,1,1)
#optimization()


pnl1,sharpe1=s.ma(22,58)#calculation of pnl and sharpe ratio for MA
pnl2,sharpe2=s.filtering(0.01)
pnl3,sharpe3=s.stochastic()
pnl4,sharpe4=s.end_month()

#df=pd.DataFrame({'Sharpe Ratio':[sharpe1,sharpe2,sharpe3,sharpe4],
              #  'P&L':[pnl1,pnl2,pnl3,pnl4]},
      #          index=['MA crossover','Filtering strategy', 'Stochastic', 'End of the month'])#table of final results
 
 