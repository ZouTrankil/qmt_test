#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 27/02/2025.
@author: Air.Zou
"""
def code_symbol(code):
    # 上海证券交易所: sh, 深证证券交易所: sz, 北京证券交易所: bj;
    if code.startswith('00'):
        return code + '.SZ'
    elif code.startswith('30'):
        return code + '.SH'
    elif code.startswith('60'):
        return code + '.SH'
    elif code.startswith('90'):
        return code + '.SH'
    elif code.startswith('11'):
        return code + '.SH'
    return 0