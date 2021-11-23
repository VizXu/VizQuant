import signal
import multitasking
import pandas as pd
import numpy as np
from tqdm import tqdm
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

    def get_multi_funds_base_info(self, fund_codes: List[str]) -> pd.Series:
        """
        获取多只基金的基本面信息
        :param fund_codes:
            6位基金代码组成的List
        :return:
        pd.Series
            包含多只基金的基本信息，以pd.Series返回
        """
        ss = []

        @multitasking.task
        @retry(tries=3, delay=1)
        def start(fund_code: str) -> None:
            s = self.get_one_fund_base_info(fund_code)
            ss.append(s)
            bar.update()
            bar.set_description(f'processing {0}'.format(fund_code))

        bar = tqdm(total=len(fund_codes))
        for fund_code in fund_codes:
            start(fund_code)
        multitasking.wait_for_tasks()
        df = pd.DataFrame(ss)
        return df

    def get_funds_base_info(self, fund_codes: Union[str, List[str]]) -> Union[pd.Series, pd.DataFrame]:
        """
        获取某只或多只基金基本面信息
        :param fund_codes:
            6位数的基金代码或者6位数基金代码组成的列表
        :return:
            Union[pd.Series, pd.DataFrame]
            pd.Series: 包含单只基金基本面信息
            pd.DataFrame: 包含多只基金基本面信息
        Raises:
            TypeError: 当fund_codes 类型不符合时抛出异常
        """
        if isinstance(fund_codes, str):
            return self.get_one_fund_base_info(fund_codes)
        elif hasattr(fund_codes, '__iter__'):
            # print("fund_codes = {0}, len(fund_codes) is {1}".format(fund_codes, len(fund_codes)))
            return self.get_multi_funds_base_info(fund_codes)
        raise TypeError(f'参数有误，不符合要求，请输入6位数的基金代码或者由6位数基金代码组成的列表')
