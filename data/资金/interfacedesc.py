import tushare as ts
import pandas as pd

from data.tokendesc import token

# 设置 Tushare API 的 Token
ts.set_token(token)  # 替换为你的 Tushare API Token
pro = ts.pro_api()

def get_industry_moneyflow(start_date, end_date):
    """
    获取指定日期范围内的板块资金流向数据
    参数:
        start_date (str): 开始日期（格式为 YYYYMMDD）
        end_date (str): 结束日期（格式为 YYYYMMDD）
    返回:
        DataFrame: 包含板块资金流向的数据
    """
    try:
        # 调用 moneyflow_ind_ths 接口获取数据
        data = pro.moneyflow_ind_ths(start_date=start_date, end_date=end_date)
        return data
    except Exception as e:
        print(f"获取数据失败：{e}")
        return None

def analyze_and_sum_net_inflow(data):
    """
    根据板块代码（ts_code）对净流入值（net_amount）进行合并求和，并筛选出净流入总和为正数的板块
    参数:
        data (DataFrame): 从 get_industry_moneyflow 获取的数据
    返回:
        DataFrame: 筛选出的净流入总和为正数的板块
    """
    if data is None or data.empty:
        print("没有数据可供分析！")
        return None

    # 按板块代码分组，计算每个板块的净流入总和
    grouped_data = data.groupby('ts_code').agg({
        'net_amount': 'sum', # 合并求和
                      'industry': 'first',  # 保留板块名称
    'lead_stock': 'first',  # 保留领涨股票名称
    'company_num': 'first',  # 保留公司数量
    }).reset_index()

    # 筛选出净流入总和为正数的板块
    positive_inflow = grouped_data[grouped_data['net_amount'] > 0].copy()
    positive_inflow['net_amount'] = positive_inflow['net_amount']# 转换为亿元单位
    positive_inflow = positive_inflow.sort_values(by='net_amount', ascending=False)

    print("净流入总和为正数的板块：")
    print(positive_inflow)

    return positive_inflow

# 主程序
if __name__ == "__main__":
    start_date = '20250201'
    end_date = '20250223'

    # 获取板块资金流向数据
    data = get_industry_moneyflow(start_date, end_date)

    # 分析并筛选净流入总和为正数的板块
    positive_inflow_data = analyze_and_sum_net_inflow(data)