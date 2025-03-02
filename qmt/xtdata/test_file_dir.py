#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/1.
@author: Air.Zou
"""
import os
from xtquant import xtdata

# 设置自定义路径
def setup_xtdata_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    xtdata.data_dir = path
    xtdata.default_data_dir = path
    print(f"数据目录已设置为: {xtdata.get_data_dir()}")

# 使用示例
if __name__ == "__main__":
    custom_dir = "G:\qmt_mini_data"  # 修改为你的路径
    setup_xtdata_dir(custom_dir)

    # 下载数据测试
    component_stocks = xtdata.data_dir
    print("中证500成分股:", component_stocks)