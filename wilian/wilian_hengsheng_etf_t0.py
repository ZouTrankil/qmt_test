# encoding:gbk

'''
@Date : 2024年12月29日14:04:22
@Author: 邹强
'''

import numpy as np
import pandas as pd
import talib
import pickle
from collections import deque, namedtuple
from enum import Enum, unique

import threading
import time
from datetime import timedelta, datetime

# 定义ETF
ETFs = {
    "159318": "恒生港股通ETF",
    "159506": "恒生医疗ETF",
    "159545": "恒生红利低波ETF",
    "159557": "恒生医疗指数ETF",
    "159615": "恒生生物科技ETF",
    "159688": "恒生互联网ETF",
    "159699": "恒生消费ETF",
    "159726": "恒生红利ETF",
    "159740": "恒生科技ETF",
    "159742": "恒生科技指数ETF",
    "159850": "恒生国企ETF",
    "159892": "恒生医药ETF",
    "159920": "恒生ETF",
    "159960": "恒生中国企业ETF",
    "513010": "恒生科技30ETF",
    "513060": "恒生医疗ETF",
    "513130": "恒生科技ETF",
    "513180": "恒生科技指数ETF",
    "513210": "恒生ETF易方达",
    "513280": "恒生生物科技ETF",
    "513330": "恒生互联网ETF",
    "513320": "恒生新经济ETF",
    "513600": "恒生指数ETF",
    "513660": "恒生ETF",
    "513690": "恒生高股息ETF",
    "513890": "恒生科技HKEtf",
    "513950": "恒生红利ETF",
    "513970": "恒生消费ETF"
}


class a(): pass


A = a()
A.acct = '40158111'
A.acct_type = 'STOCK'
A.final_dict = {}
A.max_etf_pos = {}
A.waiting_dict = {}
A.order_time_dict = {}
A.all_order_ref_dict = {}
A.withdraw_secs = 200
A.start_time = '093000'
A.end_time = '145500'
A.end_flag = 0
A.D_NUM = 1
A.K_NUM = 1


def init(C):
    C.ratio = 1
    C.sell_code = 24
    A.accID = '40158111'
    A.accountType = 'STOCK'
    C.set_account(A.accID)
    # 是否回测开关
    C.do_back_test=True
    # 多层板块过滤
    C.spare_list = C.get_stock_list_in_sector('核心恒生ETF')
    for s in C.spare_list:
        print(s)
        # 最大仓位
        A.max_etf_pos[s] = 200000
        A.final_dict[s] = 200000
    # 设定股票池
    C.set_universe(C.spare_list)
    print(f'ContextInfo.capital{C.capital}')
    print(f'ContextInfo.period{C.period}')
    #print(f'ContextInfo.get_commission{ContextInfo.get_commission()}')

def update_time(ContextInfo):
    index = ContextInfo.barpos
    realtimetag = ContextInfo.get_bar_timetag(index)
    print(f"<----------------->Tick K 线时间 ：{timetag_to_datetime(realtimetag, '%Y/%m/%d %H:%M:%S')}")
    return timetag_to_datetime(realtimetag, '%H:%M:%S')


def handlebar(C):
    # skip history k
    # 这里要注意，实盘的时候，和回测的时候 不一样
    # 回测的时候， 这里C 可能是过去的数据， 下单参数需要注意
    # 实盘的时候 这里C 是实时数据要过滤掉过去的数据， 避免重复下单！！！！！！！！！！
    # if not C.is_last_bar():
    #     return
    t0 = time.time()
    now = datetime.now()
    now_timestr = now.strftime('%H:%M:%S')

    current_sys_time = update_time(C)
    print(current_sys_time)

    if current_sys_time < '093000' or current_sys_time > '145500':
        return

    acct = get_trade_detail_data(A.acct, A.acct_type, 'account')
    if len(acct) == 0:
        print(A.acct, '账号未登录，停止交易')
        return

    print('跑到开始交易了')
    acct = acct[0]
    # 可用资金
    available_cash = acct.m_dAvailable
    print(f'可用资金{available_cash}')

    # 获取持仓信息
    final_dict = A.final_dict
    position_list = get_trade_detail_data(A.acct, A.acct_type, 'position')
    for obj in position_list:
        print(f'obj.m_strInstrumentID{obj.m_strInstrumentID}')
        print(f'obj.m_strExchangeID{obj.m_strExchangeID}')
        print(f'obj.m_canUseVolumn{obj.m_nCanUseVolume}')
        print(f'obj.m_nVolume{obj.m_nVolume}')
        print(obj.__doc__)#查看有哪些属性字段
    #
    # # 持仓数据 组合字典
    # # #高频的需要定时检测，不能等K线 HHHHHHHHHHHHHH
    position_dict = {i.m_strInstrumentID + '.' + i.m_strExchangeID : int(i.m_nVolume) for i in position_list}
    position_dict_available = {i.m_strInstrumentID + '.' + i.m_strExchangeID : int(i.m_nCanUseVolume) for i in position_list}
    position_dict_open_price = {i.m_strInstrumentID + '.' + i.m_strExchangeID : round(i.m_dOpenPrice) for i in position_list}

    # 没有持有的品种填充持股数 0
    not_in_position_stock_dict = {i : 0 for i in final_dict if i not in position_dict}
    position_dict.update(not_in_position_stock_dict)

    if C.spare_list:
        for stock in C.spare_list:
            ## VBA函数更快(对比Python实现)
            lw1 = call_vba('LW_R.LWR1', stock, '15m', C)
            lw1 = round(lw1, 3)
            lw2 = call_vba('LW_R.LWR2', stock, '15m', C)
            lw2 = round(lw2, 3)
            lw_up_15 = call_vba('LW_R.lwr1_up_lwr2', stock, '15m', C)
            lw_down_15 = call_vba('LW_R.lwr1_down_lwr2', stock, '15m', C)

            if lw_down_15 == 1 and lw1 < 80 and lw2 > 50:
                print(f'15分钟 {stock} 出现多头排列')
                if position_dict[stock] < A.final_dict[stock]:
                    msg = f"{now.strftime('%Y-%m-%d %H:%M:%S')} 多头排列 {stock} 下单"
                    print(msg)
                    #  ‘2’参数代表无论如何都会下单
                    passorder(23, 1101, A.accID, stock, 14, -1, A.max_etf_pos[stock], "顺势入场", 2, msg, C)
                else:
                    print(f'{stock} 已经有仓位了')
                    pass
            if lw_up_15 == 1 and stock in position_dict_open_price:
                cost = position_dict_open_price[stock]
                if position_dict[stock] > 0:
                    msg = f"{now.strftime('%Y-%m-%d %H:%M:%S')} {stock} 卖出_{A.max_etf_pos[stock]}"
                    print(msg)
                    passorder(23, 1101, A.accID, stock, 14, 1, A.max_etf_pos[stock], "破势出场", 2, msg, C)
                else:
                    print(f'{stock} 没有仓位了')
                    pass

    #
