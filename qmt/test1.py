#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 19/02/2025.
@author: Air.Zou
"""
# ... existing code ...
import tushare as ts
import pandas as pd
# 设置 tushare token
ts.set_token('2876ea85cb005fb5fa17c809a98174f2d5aae8b1f830110a5ead6211')
pro = ts.pro_api()

df = pro.fund_daily(ts_code='510310.SH', start_date='20241010', end_date='20250217')
print(df.head())
