import signal
import multitasking
import pandas as pd
import numpy as np
import tqdm
import os
import re
from retry import retry
from typing import List, Union
from datetime import datetime
import requests
from .config import EastmoneyFundHeaders

signal.signal(signal.SIGINT, multitasking.killall)


# def get_fund_net_value_history(fund_code : str, pz: int = 4000) -> pd.DataFrame:

class Fund(object):
    def __init__(self):
        self.base_url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNNBasicInformation'
        self.base_columns = {
            'FCODE': '基金代码',
            'SHORTNAME': '基金简称',
            'ESTABDATE': '成立日期',
            'RZDF': '涨跌幅',
            'DWJZ': '最新净值',
            'JJGS': '基金公司',
            'FSRQ': '净值更新日期',
            'COMMENTS': '简介',
        }

    def get_one_fund_base_info(self, fund_code: str) -> pd.Series:
        """
        获取某只基金的基本面信息
        :param fund_code:
            6位基金代码
        :return:
        pd.Series
            包含该只基金的基本信息，以pd.Series返回
        """
        params = (
            ('FCODE', fund_code),
            ('deviceid', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
            ('plat', 'Iphone'),
            ('product', 'EFund'),
            ('version', '6.3.8'),
        )
        json_response = requests.get(self.base_url, headers=EastmoneyFundHeaders, params=params).json()
        s = pd.Series(json_response['Datas']).rename(index=self.base_columns)
        s = s.apply(lambda x: x.replace('\n', ' ').strip() if isinstance(x, str) else x)
        return s
