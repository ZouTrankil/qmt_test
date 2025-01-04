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
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import numpy as np

st.title('股票K线图')

st.text_input('股票代码', key='code', placeholder='000001')
st.date_input('开始日期', key='start_date', value=pd.to_datetime('20210101'))
st.date_input('结束日期', key='end_date', value=pd.to_datetime('20241231'))

if st.session_state.code:
    stock = ak.stock_zh_a_hist(
        symbol=st.session_state.code,
        start_date=st.session_state.start_date.strftime('%Y%m%d'),
        end_date=st.session_state.end_date.strftime('%Y%m%d'), adjust="")

    stock.set_index('日期', inplace=True)
    stock['ma5'] = talib.MA(stock['收盘'], timeperiod=5)
    stock['ma10'] = talib.MA(stock['收盘'], timeperiod=10)
    stock['ma20'] = talib.MA(stock['收盘'], timeperiod=20)

    c5 = pyecharts.charts.Line()
    c5.add_xaxis(stock.index.tolist())
    c5.add_yaxis("ma5", stock['ma5'].tolist(),
                    linestyle_opts=pyecharts.options.LineStyleOpts(opacity=0.5, color='blue'),
                    label_opts=pyecharts.options.LabelOpts(is_show=False),
                  )
    c10 = pyecharts.charts.Line()
    c10.add_xaxis(stock.index.tolist())
    c10.add_yaxis("ma10", stock['ma10'].tolist(),
                    linestyle_opts=pyecharts.options.LineStyleOpts(opacity=0.5, color='red'),
                    label_opts=pyecharts.options.LabelOpts(is_show=False),
                  )

    c20 = pyecharts.charts.Line()
    c20.add_xaxis(stock.index.tolist())
    c20.add_yaxis("ma20", stock['ma20'].tolist(),
                    linestyle_opts=pyecharts.options.LineStyleOpts(opacity=0.5, color='green'),
                    label_opts=pyecharts.options.LabelOpts(is_show=False),
                  )
    c = pyecharts.charts.Kline()
    c.add_xaxis(stock.index.tolist())
    c.add_yaxis("K线图", stock[['开盘', '收盘', '最低', '最高']].values.tolist())
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
        ])
    c.overlap(c5)
    c.overlap(c10)
    c.overlap(c20)
    st_pyecharts(c)
