#简化版日线K线图
import datetime
import pandas_datareader.data as web
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
from mpl_finance import candlestick_ohlc   #用于形成K线图

start = datetime.datetime(2018,1,1)
#print(start)
end = datetime.datetime.today()
#print(end)
tsla = web.DataReader('TSLA','yahoo',start,end)
#tsla['Adj Close'].plot(grid = True)
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
    ax.xaxis_date() 
    ax.autoscale_view()   # 调节坐标范围使矩形能够完全显示
    plt.setp(plt.gca().get_xticklabels(), rotation=45) 
    plt.show()
pandas_candlestick_ohlc(tsla)
