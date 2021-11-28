import os
import sys
import pandas as pd
from typing import List, Union
import numpy as np
import seaborn as sns
from scipy.stats import kstest
from scipy import stats
from datetime import datetime
from DataSource.fund.core import Fund


class Fundamentals(object):
    def __init__(self):
        pass

    @staticmethod
    def get_test_fund():
        print("get_test_fund static function!")

    @staticmethod
    def get_top_sharp_ratio(top_num: int = 10) -> pd.Series:
        fund = Fund()
        all_fund_codes = fund.get_all_fund_codes()
        num = 0
        list_of_codes = []
        for code in all_fund_codes['基金代码']:
            fund_info = fund.get_funds_base_info(code)
            if len(fund_info) == 0:
                continue
            # print("netvalue = {0}, sharp1 = {1}, stddev = {2}, type(sharp1) = {3}".format(fund_info['LJJZ'],
            # fund_info['SHARP1'], fund_info['STDDEV1'], type(fund_info['SHARP1'])))
            list_of_codes.append((code, fund_info['LJJZ'], fund_info['SHARP1'], fund_info['STDDEV1']))
        print(list_of_codes)
        list_of_codes.sort(key=lambda x: x[2], reverse=True)
        print(list_of_codes)
        return list_of_codes[:top_num]

    @staticmethod
    def get_fund_sharp_ratio(fund_codes: Union[pd.Series, pd.DataFrame]) -> float:
        fund = Fund()
        all_fund_codes = fund.get_all_fund_codes()
        print(all_fund_codes)
