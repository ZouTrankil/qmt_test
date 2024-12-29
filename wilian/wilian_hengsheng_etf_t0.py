# encoding:gbk

'''
@Date : 2024��12��29��14:04:22
@Author: ��ǿ
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

# ����ETF
ETFs = {
    "159318": "�����۹�ͨETF",
    "159506": "����ҽ��ETF",
    "159545": "���������Ͳ�ETF",
    "159557": "����ҽ��ָ��ETF",
    "159615": "��������Ƽ�ETF",
    "159688": "����������ETF",
    "159699": "��������ETF",
    "159726": "��������ETF",
    "159740": "�����Ƽ�ETF",
    "159742": "�����Ƽ�ָ��ETF",
    "159850": "��������ETF",
    "159892": "����ҽҩETF",
    "159920": "����ETF",
    "159960": "�����й���ҵETF",
    "513010": "�����Ƽ�30ETF",
    "513060": "����ҽ��ETF",
    "513130": "�����Ƽ�ETF",
    "513180": "�����Ƽ�ָ��ETF",
    "513210": "����ETF�׷���",
    "513280": "��������Ƽ�ETF",
    "513330": "����������ETF",
    "513320": "�����¾���ETF",
    "513600": "����ָ��ETF",
    "513660": "����ETF",
    "513690": "�����߹�ϢETF",
    "513890": "�����Ƽ�HKEtf",
    "513950": "��������ETF",
    "513970": "��������ETF"
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
    # �Ƿ�ز⿪��
    C.do_back_test=True
    # ��������
    C.spare_list = C.get_stock_list_in_sector('���ĺ���ETF')
    for s in C.spare_list:
        print(s)
        # ����λ
        A.max_etf_pos[s] = 200000
        A.final_dict[s] = 200000
    # �趨��Ʊ��
    C.set_universe(C.spare_list)
    print(f'ContextInfo.capital{C.capital}')
    print(f'ContextInfo.period{C.period}')
    #print(f'ContextInfo.get_commission{ContextInfo.get_commission()}')

def update_time(ContextInfo):
    index = ContextInfo.barpos
    realtimetag = ContextInfo.get_bar_timetag(index)
    print(f"<----------------->Tick K ��ʱ�� ��{timetag_to_datetime(realtimetag, '%Y/%m/%d %H:%M:%S')}")
    return timetag_to_datetime(realtimetag, '%H:%M:%S')


def handlebar(C):
    # skip history k
    # ����Ҫע�⣬ʵ�̵�ʱ�򣬺ͻز��ʱ�� ��һ��
    # �ز��ʱ�� ����C �����ǹ�ȥ�����ݣ� �µ�������Ҫע��
    # ʵ�̵�ʱ�� ����C ��ʵʱ����Ҫ���˵���ȥ�����ݣ� �����ظ��µ���������������������
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
        print(A.acct, '�˺�δ��¼��ֹͣ����')
        return

    print('�ܵ���ʼ������')
    acct = acct[0]
    # �����ʽ�
    available_cash = acct.m_dAvailable
    print(f'�����ʽ�{available_cash}')

    # ��ȡ�ֲ���Ϣ
    final_dict = A.final_dict
    position_list = get_trade_detail_data(A.acct, A.acct_type, 'position')
    for obj in position_list:
        print(f'obj.m_strInstrumentID{obj.m_strInstrumentID}')
        print(f'obj.m_strExchangeID{obj.m_strExchangeID}')
        print(f'obj.m_canUseVolumn{obj.m_nCanUseVolume}')
        print(f'obj.m_nVolume{obj.m_nVolume}')
        print(obj.__doc__)#�鿴����Щ�����ֶ�
    #
    # # �ֲ����� ����ֵ�
    # # #��Ƶ����Ҫ��ʱ��⣬���ܵ�K�� HHHHHHHHHHHHHH
    position_dict = {i.m_strInstrumentID + '.' + i.m_strExchangeID : int(i.m_nVolume) for i in position_list}
    position_dict_available = {i.m_strInstrumentID + '.' + i.m_strExchangeID : int(i.m_nCanUseVolume) for i in position_list}
    position_dict_open_price = {i.m_strInstrumentID + '.' + i.m_strExchangeID : round(i.m_dOpenPrice) for i in position_list}

    # û�г��е�Ʒ�����ֹ��� 0
    not_in_position_stock_dict = {i : 0 for i in final_dict if i not in position_dict}
    position_dict.update(not_in_position_stock_dict)

    if C.spare_list:
        for stock in C.spare_list:
            ## VBA��������(�Ա�Pythonʵ��)
            lw1 = call_vba('LW_R.LWR1', stock, '15m', C)
            lw1 = round(lw1, 3)
            lw2 = call_vba('LW_R.LWR2', stock, '15m', C)
            lw2 = round(lw2, 3)
            lw_up_15 = call_vba('LW_R.lwr1_up_lwr2', stock, '15m', C)
            lw_down_15 = call_vba('LW_R.lwr1_down_lwr2', stock, '15m', C)

            if lw_down_15 == 1 and lw1 < 80 and lw2 > 50:
                print(f'15���� {stock} ���ֶ�ͷ����')
                if position_dict[stock] < A.final_dict[stock]:
                    msg = f"{now.strftime('%Y-%m-%d %H:%M:%S')} ��ͷ���� {stock} �µ�"
                    print(msg)
                    #  ��2����������������ζ����µ�
                    passorder(23, 1101, A.accID, stock, 14, -1, A.max_etf_pos[stock], "˳���볡", 2, msg, C)
                else:
                    print(f'{stock} �Ѿ��в�λ��')
                    pass
            if lw_up_15 == 1 and stock in position_dict_open_price:
                cost = position_dict_open_price[stock]
                if position_dict[stock] > 0:
                    msg = f"{now.strftime('%Y-%m-%d %H:%M:%S')} {stock} ����_{A.max_etf_pos[stock]}"
                    print(msg)
                    passorder(23, 1101, A.accID, stock, 14, 1, A.max_etf_pos[stock], "���Ƴ���", 2, msg, C)
                else:
                    print(f'{stock} û�в�λ��')
                    pass

    #
