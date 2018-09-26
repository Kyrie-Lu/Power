# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 12:48:44 2018

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

#1.获得K线与移动线函数
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
    
#2.添加数据
start = datetime.datetime(2015,1,1)
end = datetime.datetime.today()

tsla = web.DataReader('TSLA','yahoo',start,end)
apple = web.DataReader('AAPL','yahoo',start,end)

apple["20d"] = np.round(apple["Close"].rolling(window = 20, center = False).mean(), 2)  #末尾添加一列 20d 数据
apple["50d"] = np.round(apple["Close"].rolling(window = 50, center = False).mean(), 2)
apple['20d-50d'] =apple['20d'] -apple['50d']

# np.where() is a vectorized if-else function, where a condition is checked for each component of a vector, and the first argument passed is used when the condition holds, and the other passed if it does not
apple["Regime"] = np.where(apple['20d-50d'] > 0, 1, 0)
# We have 1's for bullish regimes and 0's for everything else. Below I replace bearish regimes's values with -1, and to maintain the rest of the vector, the second argument is apple["Regime"]
apple["Regime"] = np.where(apple['20d-50d'] < 0, -1, apple["Regime"])
#apple.loc['2017-01-01':'2018-09-19',"Regime"].plot(ylim = (-2,2)).axhline(y = 0, color = "black", lw = 2)

#pandas_candlestick_ohlc(apple.loc['2017-01-01':'2018-09-19',:], otherseries = ["20d", "50d"])

#3.添加信号
# To ensure that all trades close out, I temporarily change the regime of the last row to 0
regime_orig = apple.iloc[-1,-1]    #iloc索引只能进行整数索引，即进行位置索引，不能进行label索引，而loc基于label索引
#regime_orig = apple.ix[-100,'Regime']
#print(regime_orig)
#print(apple["Regime"])

apple.iloc[-1, -1] = 0
apple["Signal"] = np.sign(apple["Regime"] - apple["Regime"].shift(1))
#print(apple["Signal"])
#apple["Signal"].plot(ylim = (-2,2)).axhline(y = 0, color = "black", lw = 2)
# Restore original regime data
apple.iloc[-1,-1] = regime_orig
#apple.tail()

#print(apple.loc[apple["Signal"] ==1,"Close"])   #输出每次买入股票时的股价

# Create a DataFrame with trades, including the price at the trade and the regime under which the trade is made.

apple_signals = pd.concat([
        pd.DataFrame({"Price": apple.loc[apple["Signal"] == 1, "Close"],
                     "Regime": apple.loc[apple["Signal"] == 1, "Regime"],
                     "Signal": "Buy"}),
        pd.DataFrame({"Price": apple.loc[apple["Signal"] == -1, "Close"],
                     "Regime": apple.loc[apple["Signal"] == -1, "Regime"],
                     "Signal": "Sell"}),
    ])   #对数据进行合并
apple_signals.sort_index(inplace = True)   #inplace = True 表示直接对apple_signals变量进行修改
#print(aa)
#print(apple_signals)



#4.查看利润情况Let's see the profitability of long trades

apple_long_profits = pd.DataFrame({
        "Price": apple_signals.loc[(apple_signals["Signal"] == "Buy") &
                                  apple_signals["Regime"] == 1, "Price"],
        "Profit": pd.Series(apple_signals["Price"] - apple_signals["Price"].shift(1)).loc[apple_signals.loc[(apple_signals["Signal"].shift(1) == "Buy") & (apple_signals["Regime"].shift(1) == 1)].index].tolist(),
        "End Date": apple_signals.loc[(apple_signals["Signal"].shift(1) == "Buy") & (apple_signals["Regime"].shift(1) == 1)].index
    })
#print(apple_long_profits)


#print(apple_signals.loc[(apple_signals["Signal"] == "Buy") & apple_signals["Regime"] == 1, "Price"])
#print(pd.Series(apple_signals["Price"] - apple_signals["Price"].shift(1)).loc[apple_signals.loc[(apple_signals["Signal"].shift(1) == "Buy") & (apple_signals["Regime"].shift(1) == 1)].index].tolist())
#print(apple_signals.loc[(apple_signals["Signal"].shift(1) == "Buy") & (apple_signals["Regime"].shift(1) == 1)].index)

#4.账户进行回测

# 获得每个交易时期的最低价
tradeperiods =pd.DataFrame({"Start": apple_long_profits.index,
                            "End": apple_long_profits["End Date"]})
apple_long_profits["Low"] =tradeperiods.apply(lambda x: min(apple.loc[x["Start"]:x["End"], "Low"]), axis =1)
#print(apple_long_profits)

# Now we have all the information needed to simulate this strategy in apple_adj_long_profits
cash =1000000
apple_backtest =pd.DataFrame({"Start Port. Value": [],
                         "End Port. Value": [],
                         "End Date": [],
                         "Shares": [],
                         "Share Price": [],
                         "Trade Value": [],
                         "Profit per Share": [],
                         "Total Profit": [],
                         "Stop-Loss Triggered": []})
#print(apple_backtest)

port_value =.5# Max proportion of portfolio bet on any trade
batch =100# Number of shares bought per batch
stoploss =.2# % of trade loss that would trigger a stoploss
for index, row in apple_long_profits.iterrows():   #iterrows用来遍历dataframe，row表示每个列的值
    #print(index,'\n')
    #print(type(index))
    #print(row,'\n')

    #np.floor:返回不大于x的最大整数，np.ceil返回值大于x一点的整数
    batches =np.floor(cash *port_value) // np.ceil(batch *row["Price"]) # Maximum number of batches of stocks invested in买了batches手股票
    trade_val =batches *batch *row["Price"] # How much money is put on the line with each trade每次交易花了多少钱
    if row["Low"] < (1-stoploss) *row["Price"]:   # Account for the stop-loss
        #此行应该是0.2
        share_profit =np.round((1-stoploss) *row["Price"], 2) 
        stop_trig = True
    else:
        share_profit = row["Profit"]
        stop_trig =False
    profit = share_profit *batches *batch # Compute profits
    # Add a row to the backtest data frame containing the results of the trade
    apple_backtest =apple_backtest.append(pd.DataFrame({
                "Start Port. Value": cash,
                "End Port. Value": cash +profit,
                "End Date": row["End Date"],
                "Shares": batch *batches,
                "Share Price": row["Price"],
                "Trade Value": trade_val,
                "Profit per Share": share_profit,
                "Total Profit": profit,
                "Stop-Loss Triggered": stop_trig
            }, index = [index])) #, index = [index] ???????????????????
    cash = max(0, cash + profit)   
pd.set_option('display.max_columns', None) 
print(apple_backtest,'\n')
#print(cash)
apple_backtest['End Port. Value'].plot()
