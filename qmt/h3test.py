#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 19/02/2025.
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

code = "510300.SH"
print(code)
# 创建一个简单的策略
# ... existing code ...
# 创建一个简单的策略
class MyStrategy(bt.Strategy):
    def __init__(self):
        # 添加 MA5 和 MA10 指标
        self.sma5 = bt.indicators.SimpleMovingAverage(self.data.close, period=5)
        self.sma10 = bt.indicators.SimpleMovingAverage(self.data.close, period=10)
        # 计算 MA5 和 MA10 的交叉信号
        self.crossover = bt.indicators.CrossOver(self.sma5, self.sma10)

    def next(self):
        # 如果 MA5 上穿 MA10，买入
        if self.crossover > 0:
            self.buy()
        # 如果 MA5 下穿 MA10，卖出
        elif self.crossover < 0:
            self.sell()


# 创建 Cerebro 引擎
cerebro = bt.Cerebro()

# 添加策略
cerebro.addstrategy(MyStrategy)

# 加载数据
def get_data(symbol,start_date,end_date):
    ETF300 = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
    ETF300.columns=['date','股票代码',"open","close","high","low","volume",'成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
    ETF300["date"]=pd.to_datetime(ETF300["date"])
    ETF300['openinterest']=0
    ETF300.set_index("date",inplace=True)
    return ETF300[["open","high","low","close","volume","openinterest"]]
start="20241008"
end='20250217'
ETF3=get_data(code,start,end)

s = datetime.strptime(start, "%Y%m%d")
e = datetime.strptime(end, "%Y%m%d")
cerebro.adddata(bt.feeds.PandasData(dataname=stock_pinan,fromdate=s,todate=e))

# 设置初始资金
cerebro.broker.set_cash(1000000.0)

# 设置交易手续费
cerebro.broker.setcommission(commission=0.002)

# 运行回测
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('最终资金: %.2f' % cerebro.broker.getvalue())
# 绘制结果
cerebro.plot(style='candlestick', iplot=False, block=True)
