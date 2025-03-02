#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/1.
@author: Air.Zou
"""
code = '000001.SZ'
start_time = '20250217'
period = '1d'
count = -1
from xtquant import xtdata

#取全推数据
full_tick = xtdata.get_full_tick([code])
print('全推数据 日线最新值', full_tick)

#下载历史数据 下载接口本身不返回数据
xtdata.download_history_data(code, period='1m', start_time=start_time)

#订阅最新行情
c = 0
def callback_func(data):
    global c
    c += 1
    print(f'c:{c} 回调触发{data}')

xtdata.subscribe_quote(code, period='1m', count=-1, callback= callback_func)
data = xtdata.get_market_data([], [code], period='1m', start_time=start_time)
print('一次性取数据', data)

#死循环 阻塞主线程退出
xtdata.run()
