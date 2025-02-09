#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/1/12.
@author: Air.Zou
"""
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

stock_pinan = ak.stock_zh_a_hist(
    symbol=stock_set[0],
    start_date=st.session_state.start_date.strftime('%Y%m%d'),
    end_date=st.session_state.end_date.strftime('%Y%m%d'), adjust="hfq")[["收盘"]]

r_pinan = stock_pinan['收盘']/stock_pinan['收盘'].shift(1)-1
r_pinan = r_pinan.dropna()

st.line_chart(r_pinan)


feng_xian = ((r_pinan-r_pinan.mean())**2).mean()**0.5
st.write("风险：",feng_xian)

xia_feng_xian = (((r_pinan[r_pinan<r_pinan.mean()]-r_pinan.mean())**2).sum()/len(r_pinan))**0.5

st.write("下行风险：",xia_feng_xian)

hui_ce = stock_pinan.max()-stock_pinan.iloc[-1]
st.write("回撤：",hui_ce)

hui_ce_lv = (stock_pinan.max()-stock_pinan.iloc[-1])/stock_pinan.max()

st.write("回撤率：",hui_ce_lv)

