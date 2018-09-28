#项目网站下载数据与形成K线图代码
import pandas as pd
import pandas_datareader.data as web   # Package and modules for importing data;
# this code may change depending on pandas version
import datetime
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
from mpl_finance import candlestick_ohlc   #用于形成K线图
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2016, 1, 1)
#end = datetime.datetime(2016, 12, 31)
end = datetime.date.today()

# Let's get Apple stock data; Apple's ticker symbol is AAPL
# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance),
# third is the start date, fourth is the end date
apple = web.DataReader("AAPL", "yahoo", start, end)  #利用模块网页获取数据


 
def pandas_candlestick_ohlc(dat, stick = "day", otherseries = None):
    """
    :param dat: pandas DataFrame object with datetime64 index, and float columns "Open", "High", "Low", and "Close", likely created via DataReader from "yahoo"
    :param stick: A string or number indicating the period of time covered by a single candlestick. Valid string inputs include "day", "week", "month", and "year", ("day" default), 
    and any numeric input indicates the number of trading days included in a period
    :param otherseries: An iterable that will be coerced into a list, containing the columns of dat that hold other series to be plotted as lines
 
    This will show a Japanese candlestick plot for stock data stored in dat, also plotting other series if passed.
    """
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays #设置主刻度
    alldays = DayLocator()              # minor ticks on the days  #设置次要刻度
    dayFormatter = DateFormatter('%d')      # e.g., 12
 
    # Create a new DataFrame which includes OHLC data for each period specified by stick input
    transdat = dat.loc[:,["Open", "High", "Low", "Close"]]  #取出四列数据
    if (type(stick) == str):
        if stick == "day":
            plotdat = transdat
            stick = 1 # Used for plotting

        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) # Identify weeks
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) # Identify months
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) # Identify years
            grouped = transdat.groupby(list(set(["year",stick]))) # Group by year and other appropriate variable
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                            "High": max(group.High),
                                            "Low": min(group.Low),
                                            "Close": group.iloc[-1,3]},
                                           index = [group.index[0]]))
            if stick == "week": stick = 5
            elif stick == "month": stick = 30
            elif stick == "year": stick = 365
 
    elif (type(stick) == int and stick >= 1):
        transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                        "High": max(group.High),
                                        "Low": min(group.Low),
                                        "Close": group.iloc[-1,3]},
                                       index = [group.index[0]]))
 
    else:
        raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

 
    # Set plot parameters, including the axis object ax used for plotting
    fig, ax = plt.subplots(figsize=(15,8))   #创建一个图表对象
    fig.subplots_adjust()  #用来调整轴与底边的距离
    print(plotdat.index[-1])   #输出时间索引
    #print(plotdat)
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)  #设置主刻度
        ax.xaxis.set_minor_locator(alldays)   #设置次要刻度
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)  #设定格式
 
    ax.grid(True)
 
    # Create the candelstick chart

    candlestick_ohlc(ax, list(zip(list(matplotlib.dates.date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), 
                plotdat["High"].tolist(),plotdat["Low"].tolist(), plotdat["Close"].tolist())),colorup = "black", colordown = "red", width = stick * .4)
    #tolist数字转列表，date2num将日期时间转化为point number
   # candlestick_ohlc(ax,plotdat,colorup = "black", colordown = "red", width = stick * .4)
 
    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)
 
    ax.xaxis_date()   #tell matplotlib模块将x轴数值转化为日期
    ax.autoscale_view()   # 调节坐标范围使矩形能够完全显示
    plt.setp(plt.gca().get_xticklabels(), rotation=45)  #plt.gca().get_xticklabels()为需要设置的object，set properties 对图像设定属性，rotation为X轴字体斜度
   # plt.setp(rotation=45, horizontalalignment='right') 
   #当前的图表和子图可以使用plt.gcf()和plt.gca()获得，分别表示"Get Current Figure"和"Get Current Axes"。在pyplot模块中，许多函数都是对当前的Figure或Axes对象进行处理，比如说：
   #plt.plot()实际上会通过plt.gca()获得当前的Axes对象ax，然后再调用ax.plot()方法实现真正的绘图。
    plt.show()


#pylab.rcParams['figure.figsize'] = (15, 8)   # 用来改变出现图表的大小 rcParams为修改配置文件
#pylab.rcParams['savefig.dpi'] = 100    #图片像素
#pylab.rcParams['figure.dpi'] = 100     #分辨率
 
pandas_candlestick_ohlc(apple)
