# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:04:41 2023

@author: wp
"""
import json
from streamlit_echarts import JsCode
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime

st.markdown("# 行业分析 🎉")

def line_muti(data):

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data.index.tolist()]
      },
      "yAxis": {
        "type": 'value'
      },
      "legend":{},
      "tooltip": {},
      "series": [
      ]
    }
    for i in data.columns:
        option["series"].append({"data":data[i].tolist(),"type":"line","name":i})
          
    return option


def cw_muti_index(cw_index):
    st.write(cw_index)
    cw_xx_hy_pivot=cw_xx_hy.pivot(index="报告期",values=cw_index, columns='股票简称').fillna(-1)
    st_echarts(line_muti(cw_xx_hy_pivot))

def line_muti_price(data):

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data.index.tolist()]
      },
      "yAxis": {
        "type": 'value'
      },
      "legend":{},
      "tooltip": {},
      "series": [
      ]
    }
    for i in data.columns:
        option["series"].append({"data":(data[i]/data[i].iloc[0]).tolist(),"type":"line","name":i})
          
    return option

stock_input = st.text_input('请输入股票列表,空格分割', '格力电器 比亚迪')
stock_list=stock_input.split(" ")

cw_xx=pd.merge(st.session_state.cwzbsj,st.session_state.stock_xx,on="股票代码")
cw_xx_hy=cw_xx[cw_xx["股票简称"].isin(stock_list)]

stock_list_price=st.session_state.stock_daily[st.session_state.stock_daily["股票简称"]
          .isin(stock_list)].pivot(index="交易日期",columns="股票简称",values="收盘价").fillna(method='bfill').fillna(method='ffill')

st_echarts(line_muti_price(stock_list_price))

st.sidebar.markdown("### 安全性指标")
an_quan=["流动比率","速动比率","资产负债率"]
for i in an_quan:
    agree1 = st.sidebar.checkbox(i)
    if agree1:
        cw_muti_index(i)
st.sidebar.markdown("### 盈利能力指标")
an_quan=["营业利润/营业总收入","销售毛利率","销售净利率","净资产收益率(扣除非经常损益)","总资产报酬率"]
for i in an_quan:
    agree1 = st.sidebar.checkbox(i)
    if agree1:
        cw_muti_index(i)
st.sidebar.markdown("### 杜邦分析")
an_quan=["扣除非经常损益后的单季度净利润","总资产周转率","总资产净利率"]
for i in an_quan:
    agree1 = st.sidebar.checkbox(i)
    if agree1:
        cw_muti_index(i)
st.sidebar.markdown("### 成长性指标分析")
an_quan=["营业总收入同比增长率(%)(单季度)","净利润同比增长率(%)(单季度)","扣除非经常性损益后的净利润(扣非净利润)",'每股营业收入','研发费用']
for i in an_quan:
    agree1 = st.sidebar.checkbox(i)
    if agree1:
        cw_muti_index(i)
st.sidebar.markdown("### 管理水平指标")
an_quan=["应收账款周转率","存货周转率","固定资产周转率"]
for i in an_quan:
    agree1 = st.sidebar.checkbox(i)
    if agree1:
        cw_muti_index(i)