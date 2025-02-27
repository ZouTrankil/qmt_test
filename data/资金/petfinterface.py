#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27/02/2025.
@author: Air.Zou
"""
import tushare as ts
import pandas as pd

from data.tokendesc import token

# 设置 Tushare token（请替换为你的实际 token）
ts.set_token(token)

# 初始化 pro 接口
pro = ts.pro_api()
hs300 = pro.index_weight(index_code='000300.SH')
print(hs300[hs300['trade_date'] == '20250205'])

zz500 = pro.index_weight(index_code='000905.SH')

# 打印最新交易日的中证500成分股
latest_date = zz500['trade_date'].max()
print(f"中证500最新交易日（{latest_date}）的成分股：")
print(zz500[zz500['trade_date'] == latest_date])
# 添加股票名称（可选）
# stock_basic = pro.stock_basic(fields='ts_code,name')
# a500_constituents = a500_constituents.merge(stock_basic, on='ts_code', how='left')

# 输出结果
# print("中证 A500 成分股列表：")
# print(a500_constituents[['ts_code', 'name', 'in_date', 'out_date']])

# 可选：保存到 CSV 文件
# a500_constituents.to_csv('a500_constituents.csv', index=False, encoding='utf-8-sig')
