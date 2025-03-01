#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27/02/2025.
@author: Air.Zou
"""
import akshare as ak
import pandas as pd

A500 = '000510' # 中证500指数代码
ETF300 = '000300' # 沪深300指数代码
A50 = '930050' # 沪深300指数代码

# 获取中证 A500 成分股列表
# 指数代码：930050.CSI
a500_constituents = ak.index_stock_cons_csindex(symbol="000510")

# 输出结果
print("中证 A500 成分股列表：")
print(a500_constituents)
a500_constituents.to_csv('a500_constituents.csv', index=False, encoding='utf-8-sig')