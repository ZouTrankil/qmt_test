#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/1/14.
@author: Air.Zou
"""
import matplotlib
import pandas as pd
import talib
from datetime import datetime
import backtrader as bt
import matplotlib.pyplot as plt
import akshare as ak
import numpy as np

#正常显示画图时出现的中文和负号
from pylab import mpl

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

# 创建一个简单的策略
class MyStrategy(bt.Strategy):
    def __init__(self):
        # 添加一个简单移动平均线指标
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=15)

    def next(self):
        # 如果当前价格高于移动平均线，买入
        if self.data.close[0] > self.sma[0]:
            self.buy()
        # 如果当前价格低于移动平均线，卖出
        elif self.data.close[0] < self.sma[0]:
            self.sell()

class my_strategy2(bt.Strategy):
    #全局设定交易策略的参数

    def __init__(self):
        # 初始化交易指令、买卖价格和手续费
        self.order = None

    def next(self):
        # 检查是否持仓
        if not self.position: # 没有持仓
            #self.order = self.buy(size=500)
            #self.order_target_value(target=10000)
            #self.order_target_size(target=10000)(佣金)
            self.order_target_percent(target=0.99)
            #print(self.datetime.date(0),self.position)

# 创建 Cerebro 引擎
cerebro = bt.Cerebro()

# 添加策略
cerebro.addstrategy(my_strategy2)

# 加载数据
def get_data(symbol,start_date,end_date):
    stock_pinan = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
    stock_pinan.columns=['date','股票代码',"open","close","high","low","volume",'成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
    stock_pinan["date"]=pd.to_datetime(stock_pinan["date"])
    stock_pinan['openinterest']=0
    stock_pinan.set_index("date",inplace=True)
    return stock_pinan[["open","high","low","close","volume","openinterest"]]
start="20180101"
end='20240331'
stock_pinan=get_data("002594",start,end)

s = datetime.strptime(start, "%Y%m%d")
e = datetime.strptime(end, "%Y%m%d")
cerebro.adddata(bt.feeds.PandasData(dataname=stock_pinan,fromdate=s,todate=e))

# 设置初始资金
cerebro.broker.set_cash(10000.0)

# 设置交易手续费
cerebro.broker.setcommission(commission=0.002)

# 运行回测
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('最终资金: %.2f' % cerebro.broker.getvalue())
# 绘制结果
cerebro.plot(style='candlestick', iplot=False, block=True)
