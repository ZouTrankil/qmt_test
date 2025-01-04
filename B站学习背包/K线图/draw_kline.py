#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/1/4.
@author: Air.Zou
"""
import talib
import akshare as ak
import pandas as pd
import pyecharts
from pyecharts.charts import Kline

## test
stock_liantong = ak.stock_zh_a_hist(
    symbol="600050",
    start_date="20210101",
    end_date="20241231", adjust="")

stock_liantong.set_index('日期', inplace=True)

stock_liantong['ma5'] = talib.MA(stock_liantong['收盘'], timeperiod=5)
stock_liantong['ma10'] = talib.MA(stock_liantong['收盘'], timeperiod=10)
stock_liantong['ma20'] = talib.MA(stock_liantong['收盘'], timeperiod=20)

c5 = pyecharts.charts.Line()
c5.add_xaxis(stock_liantong.index.tolist())
c5.add_yaxis("ma5", stock_liantong['ma5'].tolist(),
                linestyle_opts=pyecharts.options.LineStyleOpts(opacity=0.5,color='blue'),
                label_opts=pyecharts.options.LabelOpts(is_show=False),
              )
c10 = pyecharts.charts.Line()
c10.add_xaxis(stock_liantong.index.tolist())
c10.add_yaxis("ma10", stock_liantong['ma10'].tolist(),
                linestyle_opts=pyecharts.options.LineStyleOpts(opacity=0.5,color='red'),
                label_opts=pyecharts.options.LabelOpts(is_show=False),
              )

c20 = pyecharts.charts.Line()
c20.add_xaxis(stock_liantong.index.tolist())
c20.add_yaxis("ma20", stock_liantong['ma20'].tolist(),
                linestyle_opts=pyecharts.options.LineStyleOpts(opacity=0.5,color='green'),
                label_opts=pyecharts.options.LabelOpts(is_show=False),
              )



c = Kline()
c.add_xaxis(stock_liantong.index.tolist())
c.add_yaxis("K线图", stock_liantong[['开盘', '收盘', '最低', '最高']].values.tolist())
c.set_global_opts(
    xaxis_opts=dict(is_scale=True),
    yaxis_opts=dict(
        is_scale=True,
        splitarea_opts=dict(
            is_show=True, areastyle_opts=dict(opacity=1)
        ),
    ),
    datazoom_opts=[
        dict(
            type="inside", xaxis_index=[0, 0], range_start=99.9, range_end=100
        ),
        dict(xaxis_index=[0, 0], type="slider", pos_top="99%", range_start=99.9, range_end=100),
    ]
)

c.overlap(c5)
c.overlap(c10)
c.overlap(c20)
c.render()


