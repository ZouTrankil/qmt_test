#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27/02/2025.
@author: Air.Zou
"""
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

from data.资金.code_symbol import code_symbol

# 设置时间范围（例如最近 30 天，可根据需求调整）
end_date = datetime.now().strftime('%Y%m%d')  # 当前日期
start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')  # 30 天前

# 获取中证 A500 成分股列表
a500_constituents = ak.index_stock_cons_csindex(symbol="000510")
print(a500_constituents)
a500_constituents.to_csv('a500_constituents.csv', index=False, encoding='utf-8-sig')

# 初始化结果 DataFrame
# result = pd.DataFrame()

# 遍历每只成分股，获取资金流向和涨幅数据
# for stock_code in a500_constituents['成分券代码']:
#     try:
#         # 获取资金流向数据（单位：万元）
#         mark = code_symbol(stock_code)
#         money_flow = ak.stock_individual_fund_flow(stock=stock_code, market=mark)
#         money_flow_filtered = money_flow[
#             (money_flow['date'] >= start_date) & (money_flow['date'] <= end_date)
#             ]
#
#         # 计算净流入（主力净流入 + 超大单净流入）
#         net_inflow = (money_flow_filtered['main_net_inflow'].sum() +
#                       money_flow_filtered['super_net_inflow'].sum())
#
#         # 获取股票行情数据（收盘价用于计算涨幅）
#         stock_data = ak.stock_zh_a_hist(symbol=stock_code,
#                                         start_date=start_date,
#                                         end_date=end_date,
#                                         adjust="qfq")
#
#         if not stock_data.empty:
#             # 计算涨幅（首日收盘价到末日收盘价的百分比变化）
#             start_price = stock_data['收盘'].iloc[0]
#             end_price = stock_data['收盘'].iloc[-1]
#             price_change = ((end_price - start_price) / start_price) * 100
#         else:
#             price_change = None
#
#         # 将结果添加到 DataFrame
#         result = pd.concat([result, pd.DataFrame({
#             'stock_code': [stock_code],
#             'name': [a500_constituents[a500_constituents['symbol'] == stock_code]['name'].iloc[0]],
#             'net_inflow': [net_inflow],  # 单位：万元
#             'price_change': [price_change]  # 单位：%
#         })])
#
#     except Exception as e:
#         print(f"获取 {stock_code} 数据时出错: {e}")
#         continue

# 按净流入从大到小排序
# result = result.sort_values(by='net_inflow', ascending=False).reset_index(drop=True)

# 输出结果
# print(f"中证 A500 成分股 {start_date} 至 {end_date} 的资金流入及涨幅统计：")
# print(result[['stock_code', 'name', 'net_inflow', 'price_change']])

# 可选：保存到 CSV 文件
# result.to_csv('a500_fund_flow_and_return.csv', index=False, encoding='utf-8-sig')