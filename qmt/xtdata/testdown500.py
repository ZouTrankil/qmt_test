#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/1.
@author: Air.Zou
"""


# 从本地python导入xtquant库，如果出现报错则说明安装失败
import time

from data.资金.code_symbol import code_symbol

# 设定一个标的列表
code_list = []

# 读取 G:\fund\qmt_test\data\资金\a500_constituents.csv 数据
import pandas as pd

def get_code_list():
    a500_constituents = pd.read_csv('a500_constituents.csv')
    code_list = a500_constituents[['成分券代码', '成分券名称']].values.tolist()
    new_code_list = [[code_symbol(str(item[0]).zfill(6)), item[1]] for item in code_list]
    return new_code_list


if __name__ == '__main__':
    code_list = get_code_list()
    print(code_list)
