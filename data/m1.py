#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/2/23.
@author: Air.Zou
"""
import pandas as pd
import tushare as ts
from pymongo import MongoClient


pro = ts.pro_api('2876ea85cb005fb5fa17c809a98174f2d5aae8b1f830110a5ead6211')  # 替换为你的Tushare Token
df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

client = MongoClient(host='localhost',
                     port=27017)


# 存入数据
def insert_mongo(df):
    db = client['demos']
    collection = db['stock_basic']
    print(df)
    collection.insert_many(df.to_dict('records'))

insert_mongo(df)