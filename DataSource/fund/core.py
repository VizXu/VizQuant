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
        self.all_funds_params = [('op', 'ph'), ('dt', 'kf'), ('rs', ''), ('gs', '0'),
                                 ('sc', '6yzf'), ('st', 'desc'), ('qdii', ''), ('tabSubtype', ',,,,,'),
                                 ('pi', '1'), ('pn', '50000'), ('dx', '1'), ('v', '0.09350685300919159'),
                                 ]
        self.all_funds_url = "http://fund.eastmoney.com/data/rankhandler.aspx"
        self.all_funds_headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
            'Accept': '*/*',
            'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        self.history_data = {
            'FCODE': f'{fund_code}',
            'IsShareNet': 'true',
            'MobileKey': '1',
            'appType': 'ttjj',
            'appVersion': '6.2.8',
            'cToken': '1',
            'deviceid': '1',
            'pageIndex': '1',
            'pageSize': f'{pz}',
            'plat': 'Iphone',
            'product': 'EFund',
            'serverVersion': '6.2.8',
            'uToken': '1',
            'userId': '1',
            'version': '6.2.8'
        }
        self.history_url = 'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNHisNetList'

    def get_all_fund_codes(self, ft: str = None) -> pd.DataFrame:
        """
        获取所以公募基金代码及名称
        :param:
            ft: str类型，可选
            基金类型：
                ’zq‘: 债券类型基金
                ’gp‘: 股本类型基金
                None: 默认全部
        :return:
            DataFrame
                包含所有基金组成的DataFrame
                 基金代码                   基金简称
            0      000689             前海开源新经济混合A
            1      017623                  1.50%
            2      005669             前海开源公用事业股票
            3      001933               华商新兴活力混合
            4      001245               工银生态环境股票
            ...       ...                    ...
            12849  014090  中融添益进取3个月持有混合发起(FOF)A
            12850  014109              融通内需驱动混合C
            12851  303832
            12852  013228       中邮鑫享30天滚动持有短债债券C
            12853  013428       东兴鑫享6个月滚动持有债券发起A

            [12854 rows x 2 columns]
        """
        if ft is not None and ft in ['gp', 'zq']:
            self.all_funds_params.append(('ft', ft))
        response = requests.get(self.all_funds_url, headers=self.all_funds_headers, params=self.all_funds_params)
        # results = re.findall('(\d{6}),(.*?),', response.text)
        columns = ['基金代码', '基金简称']
        results = re.findall('(\d{6}),(.*?),', response.text)
        df = pd.DataFrame(results, columns=columns)
        return df

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
                             基金代码        基金简称   FTYPE FEATURE BFUNDTYPE  ...  HSGRT                                 BENCH  \
            0  003834   华夏能源革新股票A     股票型      --       001  ...  0.15%        中证内地新能源指数收益率*90%+上证国债指数收益率*10%
            1  001475   易方达国防军工混合  混合型-偏股     211       002  ...  0.15%  申万国防军工指数收益率×70%+一年期人民币定期存款利率(税后)×30%
            2  005669  前海开源公用事业股票     股票型     701       001  ...  0.15%   MSCI中国A股公用事业指数收益率×80%+中证全债指数收益率×20%

              FINSALES INVESTMENTIDEAR INVESTMENTIDEARIMG
            0        0              --                 --
            1        0              --                 --
            2        0              --                 --
        Raises:
            TypeError: 当fund_codes 类型不符合时抛出异常
        """
        if isinstance(fund_codes, str):
            return self.get_one_fund_base_info(fund_codes)
        elif hasattr(fund_codes, '__iter__'):
            # print("fund_codes = {0}, len(fund_codes) is {1}".format(fund_codes, len(fund_codes)))
            return self.get_multi_funds_base_info(fund_codes)
        raise TypeError(f'参数有误，不符合要求，请输入6位数的基金代码或者由6位数基金代码组成的列表')

    def get_quote_history(self, fund_code: str, pz: int = 40000) -> pd.DataFrame:
        """
        获取基金代码净值信息数据
        :param fund_code:
                6位基金代码
        :param pz:
                可选参数，默40000页历史数据
        :return:
            pd.DataFrame，包含历史净值等数据
        """
        json_response = requests.get(self.history_url, headers=EastmoneyFundHeaders, data=self.history_data).json()
        rows = []
        columns = ['日期', '单位净值', '累计净值', '涨跌幅']
        if json_response is None:
            return pd.DataFrame(row, columns=columns)
        datas = json_response['Datas']
        if len(datas) == 0:
            return pd.DataFrame(row, columns=columns)
        for fund in datas:
            date = fund['FSRQ']
            rows.append({
                '日期': date,
                '单位净值': fund['DWJZ'],
                '累计净值': fund['LJJZ'],
                '涨跌幅': fund['JZZZL']
            })
        df = pd.DataFrame(rows)
        return df