#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 24/02/2025.
@author: Air.Zou
"""
import tushare as ts
import pandas as pd

import backtrader as bt
# 设置 tushare token
ts.set_token('2876ea85cb005fb5fa17c809a98174f2d5aae8b1f830110a5ead6211')
pro = ts.pro_api()

df = pro.fund_daily(ts_code='510880.SH', start_date='20210110', end_date='20250225')
# df = pro.daily(ts_code='601288.SH', start_date='20210110', end_date='20250225')

print(df.head())
# print data and compose
df["date"]=pd.to_datetime(df["trade_date"])
df['openinterest']=0
df.rename(columns={'amount':'volume'}, inplace=True)
df.set_index("date",inplace=True)
df.sort_index(inplace=True)
df = df[["open","high","low","close","volume","openinterest"]]
print(df.head())

# stategy
from datetime import datetime

class DynamicPositionStrategy2(bt.Strategy):
    def __init__(self):
        self.sma5 = bt.indicators.SimpleMovingAverage(self.data.close, period=5)
        self.sma10 = bt.indicators.SimpleMovingAverage(self.data.close, period=20)
        self.crossover = bt.indicators.CrossOver(self.sma5, self.sma10)
        # 假设使用波动率指标来动态调整仓位
        self.volatility = bt.indicators.StdDev(self.data.close, period=20)

    def next(self):
        # 获取当前日期
        current_date = self.data.datetime.date(0)
        # 获取当前可用资金
        available_cash = self.broker.get_cash()
        # 获取当前持仓数量
        position_size = self.position.size
        # 获取当前价格
        price = self.data.close[0]

        # 手动计算波动率的均值
        volatility_data = self.volatility.get(size=20)  # 获取最近 20 个周期的波动率数据
        if len(volatility_data) == 20:  # 确保有足够的数据来计算均值
            volatility_mean = sum(volatility_data) / len(volatility_data)
        else:
            # 如果数据不足，使用默认值，这里简单设为 0
            volatility_mean = 0

        # 判断是否没有持仓
        if position_size == 0:
            # 计算可买入数量（全仓买入）
            size = 0.8*(int((available_cash / price))//100)*100
            # 执行买入操作
            self.buy(size=size)
            print(f'买入信号触发，可用资金: {available_cash:.2f}，买入数量: {size:.2f} 价格: {price:.2f}')
        elif self.crossover > 0:
            # 计算可投资金比例
            if self.volatility[0] > volatility_mean:
                # 高波动率时使用 30% 的资金
                invest_ratio = 0.3
            else:
                # 低波动率时使用 70% 的资金
                invest_ratio = 0.7
            invest_amount = available_cash * invest_ratio

            if invest_amount > 0:
                # 计算可买入数量
                size = invest_amount / price
                self.buy(size=size)
                print(f'{current_date}: 买入信号触发，可用资金: {available_cash:.2f}，投资比例: {invest_ratio * 100:.2f}%，买入数量: {size:.2f} 买入: {price:.2f}')
            else:
                print(f'{current_date}: 买入信号触发，但可用资金不足')

        elif self.crossover < 0:
            if position_size > 0:
                self.sell(size=position_size)
                print(f'{current_date}: 卖出信号触发，卖出数量: {position_size:.2f} 卖出: {price:.2f}')
            else:
                print(f'{current_date}: 卖出信号触发，但没有持仓')


# backtrader

# 创建 Cerebro 引擎
cerebro = bt.Cerebro()

# 添加策略
cerebro.addstrategy(DynamicPositionStrategy2)

s = datetime.strptime("20210110", "%Y%m%d")
e = datetime.strptime("20250225", "%Y%m%d")
cerebro.adddata(bt.feeds.PandasData(dataname=df,fromdate=s,todate=e))

# 设置初始资金
cerebro.broker.set_cash(1000000.0)

# 设置仓位


# 设置交易手续费
cerebro.broker.setcommission(commission=0.002)

# 添加夏普比率分析器
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
# 添加回撤分析器
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

# 运行回测
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
results = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('最终资金: %.2f' % cerebro.broker.getvalue())
# 获取策略实例
strat = results[0]
# 打印夏普比率
sharpe_ratio = strat.analyzers.sharpe_ratio.get_analysis()
print(f"Sharpe Ratio: {sharpe_ratio['sharperatio']}")

# 打印回撤信息
drawdown = strat.analyzers.drawdown.get_analysis()
print(f"Max Drawdown: {drawdown['max']['drawdown']}%")
print(f"Max Drawdown Duration: {drawdown['max']['len']} periods")

# 绘制结果
cerebro.plot(style='candlestick', iplot=False, block=True)