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
            print("netvalue = {0}, sharp1 = {1}, stddev = {2}, type(sharp1) = {3}".format(fund_info['LJJZ'],
                                                                                          fund_info['SHARP1'],
                                                                                          fund_info['STDDEV1'],
                                                                                          type(fund_info['SHARP1'])))
            list_of_codes.append((code, fund_info['LJJZ'], fund_info['SHARP1'], fund_info['STDDEV1']))
        print(list_of_codes)
        list_of_codes.sort(key=lambda x: x[2], reverse=True)
        print(list_of_codes)
        return list_of_codes[:top_num]

    @staticmethod
    def get_all_funds_basic_information() -> float:
        """
        获取市场上所有基金基本面信息
        :return:
        所有基金的基本面信息，pd.DataFrame
                  0%|          | 0/12884 [00:00<?, ?it/s]['000689' '886831' '005669' ... '015014' '013228' '013428']
        processing 0: 100%|██████████| 12884/12884 [06:40<00:00, 32.13it/s]
                 基金代码                   基金简称    FTYPE              FEATURE BFUNDTYPE  ...  HSGRT  \
        0         NaN                    NaN      NaN                  NaN       NaN  ...    NaN
        1      700003               平安策略先锋混合   混合型-灵活                  215       002  ...  0.15%
        2      005669             前海开源公用事业股票      股票型                  701       001  ...  0.15%
        3      001933               华商新兴活力混合   混合型-灵活                  215       002  ...  0.15%
        4      004391              平安转型创新混合C   混合型-灵活                  215       002  ...  0.00%
        ...       ...                    ...      ...                  ...       ...  ...    ...
        12879  013228       中邮鑫享30天滚动持有短债债券C  债券型-中短债              042,073       003  ...  0.00%
        12880  012387           国金ESG持续增长混合A   混合型-偏股              211,701       002  ...  0.15%
        12881  013280              泰达睿智稳健混合C   混合型-灵活                  215       002  ...  0.00%
        12882     NaN                    NaN      NaN                  NaN       NaN  ...    NaN
        12883  014090  中融添益进取3个月持有混合发起(FOF)A   混合型-偏股  030,073,080,211,701       002  ...  0.12%

                                                           BENCH FINSALES INVESTMENTIDEAR  \
        0                                                    NaN      NaN             NaN
        1                         沪深300指数收益率×60% + 中证全债指数收益率×40%        0              --
        2                    MSCI中国A股公用事业指数收益率×80%+中证全债指数收益率×20%        0              --
        3                           中证800指数收益率×65%+上证国债指数收益率×35%        0              --
        4                          沪深300指数收益率×50%+中证综合债指数收益率×50%        0              --
        ...                                                  ...      ...             ...
        12879            中债综合财富(1年以下)指数收益率*80%+一年期定期存款利率(税后)*20%        0              --
        12880  中证中财沪深100ESG领先指数收益率*60%+中证全债指数收益率*30%+中证港股通综合指...        0              --
        12881                     沪深300指数收益率*35%+中证综合债券指数收益率*65%        0              --
        12882                                                NaN      NaN             NaN
        12883                       中证800指数收益率*80%+中债综合指数收益率*20%        0              --

              INVESTMENTIDEARIMG
        0                    NaN
        1                     --
        2                     --
        3                     --
        4                     --
        ...                  ...
        12879                 --
        12880                 --
        12881                 --
        12882                NaN
        12883                 --

        [12884 rows x 118 columns]
        """
        fund = Fund()
        all_fund_codes = fund.get_all_fund_codes()['基金代码'].values
        all_funds_info = fund.get_funds_base_info(all_fund_codes)
        cwd = os.getcwd()
        all_fund_basic_information_path = cwd + '/fundsInfo/'
        os.mkdir(all_fund_basic_information_path, 0o755)
        funds_information = all_fund_basic_information_path + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '-funds_info.csv'
        print(all_funds_info)
        all_funds_info.to_csv(funds_information)
