# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:04:41 2023

@author: wp
"""
import pandas as pd
import numpy as np
import sqlite3
import talib
from datetime import datetime
import streamlit as st

st.set_page_config(page_title='股票财务分析系统',layout="wide")
st.markdown("# 股票财务分析系统")
st.sidebar.markdown("# 主页")
data = r"G:\fund\dbdata\stock_2018_daily\stock_2018.db"
conn=sqlite3.connect(data)

@st.cache_data
def read_cw():
    cwzbsj=pd.read_sql("select * from cwzbsj",con=conn)
    cwzbsj["报告期"]=cwzbsj["报告期"].astype("str").astype("datetime64[ns]")
    cwzbsj.set_index("报告期",inplace=True,drop=False)
    return cwzbsj

@st.cache_data
def read_price():
    stock_daily=pd.read_sql("select * from stock_daily where 股票代码<'003000.SZ'",con=conn)
    stock_daily["交易日期"]=stock_daily["交易日期"].astype("str").astype("datetime64[ns]")
    stock_daily.set_index("交易日期",inplace=True,drop=False)
    return stock_daily

@st.cache_data
def read_xx():
    stock_hy=pd.read_csv(r'G:\fund\qmt_test\B站学习背包\财务指标\tushare_bak_basic_20250216155614.csv')
    stock_hy = stock_hy.rename(columns={'ts_code': '股票代码', 'industry': '二级行业', 'name': '股票简称'})
    stock_hy = stock_hy.sort_values(by='股票代码')
    return stock_hy[stock_hy["股票代码"]<'003000.SZ'][["股票简称","股票代码","二级行业"]]


if 'cwzbsj' not in st.session_state:
    st.session_state.cwzbsj = read_cw()
    
if 'stock_daily' not in st.session_state:
    st.session_state.stock_daily = read_price()

if 'stock_xx' not in st.session_state:
    st.session_state.stock_xx = read_xx()

if 'name_id' not in st.session_state:
    st.session_state.name_id = {}
    for i in st.session_state.stock_xx.values:
        st.session_state.name_id.update({i[0]:i[1]})

st.write(st.session_state.name_id)

for i in st.session_state.stock_xx["二级行业"].unique():
    st.write(i)
    hy_stock=st.session_state.stock_xx[st.session_state.stock_xx["二级行业"]==i][["股票简称","股票代码"]]
    hy_stock.set_index("股票简称",inplace=True)
    st.table(hy_stock.T)