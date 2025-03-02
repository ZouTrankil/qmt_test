#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载 A500 从20240101 到20250301 的数据
Created on 2025/3/1.
@author: Air.Zou
"""
code = '000001.SZ'
start_time = '20250217'
period = '1d'
count = -1
from xtquant import xtdata


df = xtdata.get_sector_list()
print(df)

for i in df.index:
    print(df.loc[i])
    p = df.loc[i]
    codeList = xtdata.get_stock_list_in_sector(p['name'])
    print(f'板块:{p["name"]} 股票数量:{len(codeList)}')
    print(codeList)
