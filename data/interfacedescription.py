# 接口描述字典
interface_descriptions = {
    "stock_basic": {
        "name": "stock_basic",
        "description": "获取基础信息数据，包括股票代码、名称、上市日期、退市日期等",
        "permissions": "2000积分起，建议调取一次后保存到本地存储使用",
        "input_parameters": {
            "ts_code": {"type": "str", "required": "N", "description": "TS股票代码"},
            "name": {"type": "str", "required": "N", "description": "名称"},
            "market": {"type": "str", "required": "N", "description": "市场类别（主板/创业板/科创板/CDR/北交所）"},
            "list_status": {"type": "str", "required": "N", "description": "上市状态 L上市 D退市 P暂停上市，默认是L"},
            "exchange": {"type": "str", "required": "N", "description": "交易所 SSE上交所 SZSE深交所 BSE北交所"},
            "is_hs": {"type": "str", "required": "N", "description": "是否沪深港通标的，N否 H沪股通 S深股通"}
        },
        "output_parameters": {
            "ts_code": {"type": "str", "default_display": "Y", "description": "TS代码"},
            "symbol": {"type": "str", "default_display": "Y", "description": "股票代码"},
            "name": {"type": "str", "default_display": "Y", "description": "股票名称"},
            "area": {"type": "str", "default_display": "Y", "description": "地域"},
            "industry": {"type": "str", "default_display": "Y", "description": "所属行业"},
            "fullname": {"type": "str", "default_display": "N", "description": "股票全称"},
            "enname": {"type": "str", "default_display": "N", "description": "英文全称"},
            "cnspell": {"type": "str", "default_display": "Y", "description": "拼音缩写"},
            "market": {"type": "str", "default_display": "Y", "description": "市场类型（主板/创业板/科创板/CDR）"},
            "exchange": {"type": "str", "default_display": "N", "description": "交易所代码"},
            "curr_type": {"type": "str", "default_display": "N", "description": "交易货币"},
            "list_status": {"type": "str", "default_display": "N", "description": "上市状态 L上市 D退市 P暂停上市"},
            "list_date": {"type": "str", "default_display": "Y", "description": "上市日期"},
            "delist_date": {"type": "str", "default_display": "N", "description": "退市日期"},
            "is_hs": {"type": "str", "default_display": "N", "description": "是否沪深港通标的，N否 H沪股通 S深股通"},
            "act_name": {"type": "str", "default_display": "Y", "description": "实控人名称"},
            "act_ent_type": {"type": "str", "default_display": "Y", "description": "实控人企业性质"}
        }
    },
    "trade_cal": {
        "name": "trade_cal",
        "description": "获取各大交易所交易日历数据，默认提取的是上交所",
        "permissions": "需2000积分",
        "input_parameters": {
            "exchange": {"type": "str", "required": "N", "description": "交易所 SSE上交所,SZSE深交所,CFFEX中金所,SHFE上期所,CZCE郑商所,DCE大商所,INE上能源"},
            "start_date": {"type": "str", "required": "N", "description": "开始日期（YYYYMMDD）"},
            "end_date": {"type": "str", "required": "N", "description": "结束日期（YYYYMMDD）"},
            "is_open": {"type": "str", "required": "N", "description": "是否交易 '0'休市 '1'交易"}
        },
        "output_parameters": {
            "exchange": {"type": "str", "default_display": "Y", "description": "交易所 SSE上交所 SZSE深交所"},
            "cal_date": {"type": "str", "default_display": "Y", "description": "日历日期"},
            "is_open": {"type": "str", "default_display": "Y", "description": "是否交易 0休市 1交易"},
            "pretrade_date": {"type": "str", "default_display": "Y", "description": "上一个交易日"}
        }
    },
    "namechange": {
        "name": "namechange",
        "description": "历史名称变更记录",
        "permissions": "无特殊积分要求",
        "input_parameters": {
            "ts_code": {"type": "str", "required": "N", "description": "TS代码"},
            "start_date": {"type": "str", "required": "N", "description": "公告开始日期"},
            "end_date": {"type": "str", "required": "N", "description": "公告结束日期"}
        },
        "output_parameters": {
            "ts_code": {"type": "str", "default_display": "Y", "description": "TS代码"},
            "name": {"type": "str", "default_display": "Y", "description": "证券名称"},
            "start_date": {"type": "str", "default_display": "Y", "description": "开始日期"},
            "end_date": {"type": "str", "default_display": "Y", "description": "结束日期"},
            "ann_date": {"type": "str", "default_display": "Y", "description": "公告日期"},
            "change_reason": {"type": "str", "default_display": "Y", "description": "变更原因"}
        }
    },
    "new_share": {
        "name": "new_share",
        "description": "获取新股上市列表数据",
        "permissions": "用户需要至少120积分，单次最大2000条，总量不限制",
        "input_parameters": {
            "start_date": {"type": "str", "required": "N", "description": "上网发行开始日期"},
            "end_date": {"type": "str", "required": "N", "description": "上网发行结束日期"}
        },
        "output_parameters": {
            "ts_code": {"type": "str", "default_display": "Y", "description": "TS股票代码"},
            "sub_code": {"type": "str", "default_display": "Y", "description": "申购代码"},
            "name": {"type": "str", "default_display": "Y", "description": "名称"},
            "ipo_date": {"type": "str", "default_display": "Y", "description": "上网发行日期"},
            "issue_date": {"type": "str", "default_display": "Y", "description": "上市日期"},
            "amount": {"type": "float", "default_display": "Y", "description": "发行总量（万股）"},
            "market_amount": {"type": "float", "default_display": "Y", "description": "上网发行总量（万股）"},
            "price": {"type": "float", "default_display": "Y", "description": "发行价格"},
            "pe": {"type": "float", "default_display": "Y", "description": "市盈率"},
            "limit_amount": {"type": "float", "default_display": "Y", "description": "个人申购上限（万股）"},
            "funds": {"type": "float", "default_display": "Y", "description": "募集资金（亿元）"},
            "ballot": {"type": "float", "default_display": "Y", "description": "中签率"}
        }
    },
    "stk_rewards": {
        "name": "stk_rewards",
        "description": "获取上市公司管理层薪酬和持股",
        "permissions": "用户需要2000积分，5000积分以上频次相对较高",
        "input_parameters": {
            "ts_code": {"type": "str", "required": "Y", "description": "TS股票代码，支持单个或多个代码输入"},
            "end_date": {"type": "str", "required": "N", "description": "报告期"}
        },
        "output_parameters": {
            "ts_code": {"type": "str", "default_display": "Y", "description": "TS股票代码"},
            "ann_date": {"type": "str", "default_display": "Y", "description": "公告日期"},
            "end_date": {"type": "str", "default_display": "Y", "description": "截止日期"},
            "name": {"type": "str", "default_display": "Y", "description": "姓名"},
            "title": {"type": "str", "default_display": "Y", "description": "职务"},
            "reward": {"type": "float", "default_display": "Y", "description": "报酬"},
            "hold_vol": {"type": "float", "default_display": "Y", "description": "持股数"}
        }
    },
    "stock_company": {
        "name": "stock_company",
        "description": "获取上市公司基础信息，单次提取4500条，可以根据交易所分批提取",
        "permissions": "用户需要至少120积分",
        "input_parameters": {
            "ts_code": {"type": "str", "required": "N", "description": "股票代码"},
            "exchange": {"type": "str", "required": "N", "description": "交易所代码，SSE上交所 SZSE深交所 BSE北交所"}
        },
        "output_parameters": {}  # 未提供具体输出参数，可根据实际需求补充
    },
    "hs_const": {
        "name": "hs_const",
        "description": "获取沪股通、深股通成分数据",
        "permissions": "无特殊积分要求",
        "input_parameters": {
            "hs_type": {"type": "str", "required": "Y", "description": "类型SH沪股通SZ深股通"},
            "is_new": {"type": "str", "required": "N", "description": "是否最新 1是 0否（默认1）"}
        },
        "output_parameters": {
            "ts_code": {"type": "str", "default_display": "Y", "description": "TS代码"},
            "hs_type": {"type": "str", "default_display": "Y", "description": "沪深港通类型SH沪SZ深"},
            "in_date": {"type": "str", "default_display": "Y", "description": "纳入日期"},
            "out_date": {"type": "str", "default_display": "Y", "description": "剔除日期"},
            "is_new": {"type": "str", "default_display": "Y", "description": "是否最新 1是 0否"}
        }
    }
}