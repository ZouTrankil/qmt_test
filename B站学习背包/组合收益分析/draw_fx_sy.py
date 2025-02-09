#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/1/12.
@author: Air.Zou
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import talib
from streamlit_echarts import st_pyecharts, st_echarts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Kline
import streamlit as st
import akshare as ak

title = st.text_input('股票代码', key='code', placeholder='000001,000063')
st.write("输入的股票代码是：", title)
st.date_input('开始日期', key='start_date', value=pd.to_datetime('20210101'))
st.date_input('结束日期', key='end_date', value=pd.to_datetime('20241231'))

if str(title) == '':
    title = '300059,601319,300124,600519,603583'
stock_set = title.split(',')
p0 = ak.stock_zh_a_hist(
    symbol=stock_set[0],
    start_date="20210101",
    end_date="20241231", adjust="hfq")[["日期", "收盘"]]
p0.set_index("日期", inplace=True)

for i in stock_set[1:]:
    p1 = ak.stock_zh_a_hist(
        symbol=i,
        start_date=st.session_state.start_date.strftime('%Y%m%d'),
        end_date=st.session_state.end_date.strftime('%Y%m%d'), adjust="hfq")[["日期", "收盘"]]
    p1.set_index("日期", inplace=True)
    p0 = pd.concat([p0, p1], axis=1)

p0.columns = stock_set
p0 = p0.fillna(method='ffill')

r = (p0/p0.shift(1)-1).dropna()

data=[]
for i in range(1000):
    w0 = np.random.random(len(stock_set))
    w0 = w0/w0.sum()
    r_n_0 = np.dot(r, w0)
    data.append([r_n_0.std(), r_n_0.sum()])


option = {
    "xAxis": {
        "name": "",
        "nameLocation": 'middle',
        "nameGap": 30,
        "nameTextStyle": {
            "fontSize": 16,
        },
    },
    "yAxis": {
        "name": "Total Return",
        "nameLocation": 'middle',
        "nameGap": 30,
        "nameTextStyle": {
            "fontSize": 16,
        },
    },
    "type": 'scatter',
    "series": [
        {
            "data": data,
            "type": "scatter",
            "symbolSize": 5,
            "encode": {
                "x": 0,
                "y": 1,
            },
        }
    ]
}

st_echarts(option)