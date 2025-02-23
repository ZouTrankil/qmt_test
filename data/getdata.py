#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/2/23.
@author: Air.Zou
"""
from data.interfacedescription import interface_descriptions

import tushare as ts
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import time
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tushare_data.log'),  # 日志记录到文件
        logging.StreamHandler()  # 同时输出到控制台
    ]
)
logger = logging.getLogger(__name__)

# 设置 Tushare Token
TOKEN = '2876ea85cb005fb5fa17c809a98174f2d5aae8b1f830110a5ead6211'  # 替换为你的 Token
pro = ts.pro_api(TOKEN)

# 连接到 MongoDB
client = MongoClient(host='localhost', port=27017)
db = client['tushare_data']


# 通用的数据获取和增量存储函数
def fetch_and_store_data(interface_name, params=None):
    try:
        logger.info(f"开始处理接口: {interface_name}")

        # 调用 Tushare 接口
        if params:
            df = getattr(pro, interface_name)(**params)
        else:
            df = getattr(pro, interface_name)()

        # 如果数据为空，跳过存储
        if df.empty:
            logger.warning(f"{interface_name} 返回空数据，跳过存储")
            return

        # 将 DataFrame 转换为字典列表
        data = df.to_dict('records')

        # 添加字段描述
        field_descriptions = interface_descriptions[interface_name]['output_parameters']
        for record in data:
            record['field_descriptions'] = field_descriptions

        # 使用接口名作为集合名
        collection = db[interface_name]

        # 获取唯一的标识字段（根据接口特性选择）
        unique_key = 'ts_code' if 'ts_code' in df.columns else 'cal_date' if 'cal_date' in df.columns else None

        # 获取已有数据的唯一标识集合
        existing_keys = set()
        if unique_key:
            existing_docs = collection.find({}, {unique_key: 1})
            existing_keys = {doc[unique_key] for doc in existing_docs if unique_key in doc}
            logger.info(f"{interface_name} 已有记录数: {len(existing_keys)}")

        # 筛选新记录
        new_records = []
        for record in data:
            if unique_key and unique_key in record:
                if record[unique_key] not in existing_keys:
                    new_records.append(record)
            else:
                # 如果没有唯一标识，按记录全字段判断（效率较低）
                if not collection.find_one(record):
                    new_records.append(record)

        # 插入新记录
        if new_records:
            collection.insert_many(new_records)
            logger.info(f"增量存储 {interface_name} 新数据到 MongoDB，记录数: {len(new_records)}")
        else:
            logger.info(f"{interface_name} 无新数据需要存储")

    except Exception as e:
        logger.error(f"处理 {interface_name} 时出错: {str(e)}")

    # 避免触发频率限制
    time.sleep(1)


# 主执行逻辑
def main():
    # 为每个接口设置默认参数
    interface_params = {
        'stock_basic': {'exchange': '', 'list_status': 'L'},
        'trade_cal': {'exchange': '', 'start_date': '20100901', 'end_date': '20250223'},
        'namechange': {'ts_code': '600848.SH', 'fields': 'ts_code,name,start_date,end_date,change_reason'},
        'new_share': {'start_date': '20100901', 'end_date': '20250223'},
        'stk_rewards': {'ts_code': '000001.SZ'},
        'stock_company': {'exchange': 'SSE'},
        'hs_const': {'hs_type': 'SH'}
    }

    # 遍历所有接口并获取数据
    for interface in interface_descriptions.keys():
        params = interface_params.get(interface, None)
        fetch_and_store_data(interface, params)


if __name__ == "__main__":
    main()

    # 关闭 MongoDB 连接
    client.close()
    logger.info("程序执行完成，关闭 MongoDB 连接")