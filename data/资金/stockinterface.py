#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27/02/2025.
@author: Air.Zou
"""
import tushare as ts
import pandas as pd
from datetime import datetime, timedelta

from data.tokendesc import token

# 设置 Tushare token（请替换为你的实际 token）
ts.set_token(token)

# 初始化 pro 接口
pro = ts.pro_api()

ETF300 = '000300.SH' # 沪深300指数代码
ZZ500 = '000905.SH' # 中证500指数代码

# 获取指数成分股列表，最近5个交易日的资金净流入
def get_index_constituents_and_moneyflow(index_code, days=5):
    """
    获取指定指数的成分股列表，并计算成分股在指定时间段内的资金净流入。

    :param index_code: 指数代码，例如 '000300.SH'
    :param days: 时间范围，默认 5 天
    :return: 包含成分股代码、名称和资金净流入的 DataFrame
    """
    # 获取当前日期和指定天数前的日期
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')

    # 获取指数成分股列表
    index_constituents = pro.index_weight(index_code=index_code)
    latest_date = index_constituents['trade_date'].max()
    index_constituents = index_constituents[index_constituents['trade_date'] == latest_date]
    index_constituents['ts_code'] = index_constituents['con_code']
    index_constituents = index_constituents[['ts_code', 'con_code']]

    # 添加股票名称
    stock_basic = pro.stock_basic(fields='ts_code,name')
    index_constituents = index_constituents.merge(stock_basic, on='ts_code', how='left')

    # 获取个股资金流向数据
    moneyflow_data = pd.DataFrame()
    for stock_code in index_constituents['ts_code']:
        try:
            # 获取单只股票在指定时间段的资金流向数据
            df = pro.moneyflow(ts_code=stock_code,
                               start_date=start_date,
                               end_date=end_date)
            if not df.empty:
                # 计算该股票总净流入（buy - sell）
                stock_net_flow = (df['buy_sm_amount'].sum() + df['buy_md_amount'].sum() +
                                  df['buy_lg_amount'].sum() + df['buy_elg_amount'].sum() -
                                  df['sell_sm_amount'].sum() - df['sell_md_amount'].sum() -
                                  df['sell_lg_amount'].sum() - df['sell_elg_amount'].sum())

                # 添加到结果 DataFrame
                moneyflow_data = pd.concat([moneyflow_data,
                                            pd.DataFrame({'ts_code': [stock_code],
                                                          'net_flow': [stock_net_flow]})])
        except Exception as e:
            print(f"获取 {stock_code} 数据时出错: {e}")
            continue

    # 添加股票名称
    moneyflow_data = moneyflow_data.merge(stock_basic, on='ts_code', how='left')

    # 按净流入从大到小排序
    moneyflow_data = moneyflow_data.sort_values(by='net_flow', ascending=False)

    # 重置索引
    moneyflow_data = moneyflow_data.reset_index(drop=True)

    return moneyflow_data


if __name__ == "__main__":
    # 示例：获取沪深 300 指数成分股的资金流向
    index_code = '000300.SH'
    days = 5
    result = get_index_constituents_and_moneyflow(index_code, days)

    # 输出结果
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    end_date = datetime.now().strftime('%Y%m%d')
    print(f"{index_code} 成分股 {start_date} 至 {end_date} 的资金净流入排名（单位：万元）：")
    print(result[['ts_code', 'name', 'net_flow']])

    # 可选：保存到 CSV 文件
    result.to_csv(index_code +'_moneyflow.csv', index=False, encoding='utf-8-sig')
