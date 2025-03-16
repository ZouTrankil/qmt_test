#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/1.
@author: Air.Zou
"""

# 很慢 卡主了一样

from xtquant import xtdata
# 设定一个标的列表
code_list = ["000001.SZ"]

# 下载标的行情数据
if 1:
    xtdata.download_financial_data(code_list, table_list=['Balance'], start_time='20240101', incrementally=True)  # 下载财务数据到本地
    df = xtdata.get_financial_data(code_list, table_list=['Balance'], start_time='20240101', end_time='', report_type='report_time')
    print(df)




