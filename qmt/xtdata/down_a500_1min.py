#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/1.
@author: Air.Zou
"""
from qmt.xtdata.test_file_dir import setup_xtdata_dir
from qmt.xtdata.testdown500 import get_code_list

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025/3/1.
@author: Air.Zou
"""

# 从本地python导入xtquant库，如果出现报错则说明安装失败
from xtquant import xtdata

setup_xtdata_dir("G:\qmt_mini_data")
import time

# 设定一个标的列表
getcode_list = get_code_list()

# 设定获取数据的周期
period = "1m"
start_time = '20130701'
count = -1

# 下载标的行情数据
if 1:
    for i in getcode_list:
        code = i[0]
        name = i[1]
        print("code: %s, name: %s" % (code, name))
        try:
            print(f"开始下载数据{code}")
            xtdata.download_history_data(code, start_time=start_time, period=period,
                                         incrementally=True)  # 增量下载行情数据（开高低收,等等）到本地

            print(f"下载数据{name}完成")
            print(f'测试数据是否OK')
            last_history_data = xtdata.get_market_data([], [code], start_time=start_time, period=period, count=1)
            print(last_history_data)
            print("=" * 20)
            time.sleep(1)

            # print(f'下载财务数据{code}-{name}')
            # # xtdata.download_financial_data([code], incrementally=True)
            # print(f'下载财务数据{code}-{name}完成')
            # print("=" * 20)
            # time.sleep(3)
        except Exception as e:
            print(f"下载数据{code}-{name}失败")
            print(e)
            continue
    #   # 下载财务数据到本地
    # xtdata.download_sector_data()  # 下载板块数据到本地
    # 更多数据的下载方式可以通过数据字典查询

# 读取本地历史行情数据


# 使用回调时，必须要同时使用xtdata.run()来阻塞程序，否则程序运行到最后一行就直接结束退出了。
xtdata.run()



