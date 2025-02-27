#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25/02/2025.
@author: Air.Zou
"""

import tushare as ts
import pandas as pd

import backtrader as bt
# 设置 tushare token
ts.set_token('2876ea85cb005fb5fa17c809a98174f2d5aae8b1f830110a5ead6211')
import time

try:
    while True:
        print(f"当前时间：{time.ctime()}")

        # sina数据
        df = ts.realtime_tick(ts_code='300059.SZ')
        # 输出
        print(df)

        # 东财数据
        df = ts.realtime_tick(ts_code='300059.SZ', src='dc')
        print(df)

        # 暂停 5 秒
        time.sleep(5)
except KeyboardInterrupt:
    print("程序被手动停止")

