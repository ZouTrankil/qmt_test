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


def line_hq_cw(index_id):
    
    data_cw1=cw_price[index_id[0]]
    data_cw2=cw_price[index_id[1]]

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data_cw1.index.tolist()]
      },
      "yAxis": [{
        "type": 'value'
      },{
        "type": 'value'
      },],
      "tooltip": {},
      "series": [
        {
          "data": data_cw1.tolist(),
          "type": 'line',
          "showBackground": True,
          "backgroundStyle": {
            "color": 'rgba(180, 180, 180, 0.2)'
          }
        },
        {
          "data": data_cw2.tolist(),
          "type": 'line',
          "yAxisIndex":1
        }
      ]
    };
    
    return option

def line_hq(index_id):
    
    data_cw=stock_price_gl[index_id]

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data_cw.index.tolist()]
      },
      "yAxis": {
        "type": 'value'
      },
      "tooltip": {},
      "series": [
        {
          "data": data_cw.tolist(),
          "type": 'line',
          "showBackground": True,
          "backgroundStyle": {
            "color": 'rgba(180, 180, 180, 0.2)'
          }
        }
      ]
    };
    
    return option

def bar_cw(index_id):
    
    data_cw=stock_cw[index_id]

    option = {
      "xAxis": {
        "type": 'category',
        "data": [d.strftime("%Y-%m-%d")for d in data_cw.index.tolist()]
      },
      "yAxis": {
        "type": 'value'
      },
      "tooltip": {},
      "series": [
        {
          "data": data_cw.tolist(),
          "type": 'bar',
          "showBackground": True,
          "backgroundStyle": {
            "color": 'rgba(180, 180, 180, 0.2)'
          }
        }
      ]
    };
    
    return option


stock_name = st.sidebar.text_input('输入股票简称', '格力电器')
choice2=st.session_state.name_id[stock_name]
st.title(stock_name)

stock_cw=st.session_state.cwzbsj[st.session_state.cwzbsj["股票代码"]==choice2][['扣除非经常性损益后的净利润(扣非净利润)','净资产收益率(扣除非经常损益)','销售毛利率','销售净利率', '企业自由现金流量', '非经常性损益','净债务','每股净资产','每股营业总收入']]
stock_price_gl=st.session_state.stock_daily[st.session_state.stock_daily["股票代码"]==choice2][['收盘价', '成交量(手)','量比', '市盈率(静态)', '市盈率(TTM)', '市盈率(动态)', '市净率','市销率', '市销率(TTM)', '股息率(%)', '股息率(TTM)(%)','总市值(万元)', '流通市值(万元)']]
stock_cw1=stock_cw.resample("d").bfill()
cw_price=pd.concat([stock_price_gl,stock_cw1],axis=1).dropna()


choice4 = st.sidebar.multiselect(
    '选择两个指标',
    cw_price.columns,
    ['收盘价','销售毛利率'], max_selections=2)

if len(choice4)==2:
    st_echarts(line_hq_cw(choice4))


st.sidebar.markdown("### 行情指标")
for i in stock_price_gl.columns:
    agree1 = st.sidebar.checkbox(i)
    if agree1:
        st.write(i)
        st_echarts(line_hq(i))
        
st.sidebar.markdown("### 财务指标")
for i in stock_cw.columns:
    agree1 = st.sidebar.checkbox(i)
    if agree1:
        st.write(i)
        st_echarts(bar_cw(i))