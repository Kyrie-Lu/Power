# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 11:27:41 2018

@author: Administrator
"""
import pandas_datareader.data as web  
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
from mpl_finance import candlestick_ohlc 
import matplotlib

def pandas_candlestick_ohlc(date, stick = "day", otherseries = None):
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays #设置主刻度
    alldays = DayLocator()              # minor ticks on the days  #设置次要刻度
    transdat = date.loc[:,['Open','High','Low','Close']]
    plotdat = transdat
    stick = 1
    fig,ax = plt.subplots()
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    ax.xaxis.set_major_locator(mondays)  #设置主刻度
    ax.xaxis.set_minor_locator(alldays)   #设置次要刻度
    ax.xaxis.set_major_formatter(weekFormatter) 
    candlestick_ohlc(ax, list(zip(list(matplotlib.dates.date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), 
                plotdat["High"].tolist(),plotdat["Low"].tolist(), plotdat["Close"].tolist())),colorup = "black", colordown = "red", width = stick * .4)
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        date.loc[:,otherseries].plot(ax=ax, lw = 1.3, grid = True)
    
    
    ax.xaxis_date() 
    ax.autoscale_view()   # 调节坐标范围使矩形能够完全显示
    plt.setp(plt.gca().get_xticklabels(), rotation=45) 
    plt.show()
    

start = datetime.datetime(2018,1,1)
end = datetime.datetime.today()

tsla = web.DataReader('TSLA','yahoo',start,end)
apple = web.DataReader('AAPL','yahoo',start,end)

#stocks = pd.DataFrame({'a':tsla['Adj Close'],'b':apple['Adj Close']})
stocks = pd.DataFrame({'TSLA':tsla['Adj Close'],'AAPL':apple['Adj Close']})
#stocks.head()  返回前n行数据
#print(stocks)
#stocks.plot(secondary_y = ["AAPL"], grid = True) #右边的刻度表示AAPL

# df.apply(arg) will apply the function arg to each column in df, and return a DataFrame with the result
# Recall that lambda x is an anonymous function accepting parameter x; in this case, x will be a pandas Series object
#stock_return = stocks.apply(lambda x: x / x[0])
#stock_return.head()
#stock_return.plot(grid = True).axhline(y = 1, color = "black", lw = 2)
#stock_change = stocks.apply(lambda x: np.log(x) - np.log(x.shift(1)))  # shift moves dates back by 1.
#print(stock_change)
#stock_change.plot(grid = True).axhline(y = 0, color = "black", lw = 2)    #lw表示直线宽度

apple["20d"] = np.round(apple["Close"].rolling(window = 20, center = False).mean(), 2)  #末尾添加一列 20d 数据
apple["50d"] = np.round(apple["Close"].rolling(window = 50, center = False).mean(), 2)
print(apple)
#print(apple.loc['2018-01-01':'2018-09-19',:])
pandas_candlestick_ohlc(apple.loc['2018-01-01':'2018-09-19',:], otherseries = ["20d", "50d"])
