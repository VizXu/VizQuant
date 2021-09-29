from .config import EastMoneyHeaders
from .config import EastMoneyQuotes
from .config import EastMoneyStockBaseInfo
from .config import EastMoneyBills
from .config import EastMoneyKLines
from .utils import gen_security_id
import requests
import pandas as pd
from typing import List, Dict, Union

# fields = ",".join(EastMoneyQuotes.keys())
# columns = list(EastMoneyQuotes.values())
# params = (
#     ('pn', '1'),
#     ('pz', '1000000'),
#     ('po', '1'),
#     ('np', '1'),
#     ('fltt', '2'),
#     ('invt', '2'),
#     ('fid', 'f3'),
#     ('fs', 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23'),
#     ('fields', fields),
# )
#
#
# def get_all_stock_base_info():
#     json_response = requests.get('http://76.push2.eastmoney.com/api/qt/clist/get',
#                                  headers=EastMoneyHeaders, params=params).json()
#     return pd.DataFrame(json_response['data']['diff']).rename(columns=EastMoneyQuotes)[columns]


class Stock(object):
    def __init__(self):
        self.all_stock_quote_url = 'http://76.push2.eastmoney.com/api/qt/clist/get'
        self.all_stock_quote_fields = ",".join(EastMoneyQuotes.keys())
        self.all_stock_quote_columns = list(EastMoneyQuotes.values())
        self.stock_quote_history_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
        self.stock_quote_history_fields = ",".join(EastMoneyKLines.keys())
        self.stock_quote_history_columns = list(EastMoneyKLines.values())
        self.base_info_fields = ",".join(EastMoneyStockBaseInfo.keys())
        self.base_info_url = 'http://push2.eastmoney.com/api/qt/stock/get'

    def get_all_stock_realtime_quote(self) -> pd.DataFrame:
        """
        获取沪深市场所有证券及最新报价、涨跌幅等信息
        :return:
        返回pandas.DataFrame,包含沪深市场所有证券最新报价、涨跌幅等信息，如下
              股票名称    股票代码    最新价   昨日收盘  ...   动态市盈率 沪/深           总市值         流通市值
        0      N大地  301068  43.98  13.98  ...   51.19   0    3034920000    647438978
        1     中国能建  601868   2.75   1.96  ...   24.36   1  114650699999  32094609998
        2     恒锋工具  300488  40.13  33.44  ...   52.61   0    6648709547   5485635481
        3     聚石化学  688669  44.27  36.89  ...   38.34   1    4131866696    881353545
        4     晓程科技  300139  10.74   8.95  ...  216.76   0    2942760000   2497984649
        ...    ...     ...    ...    ...  ...     ...  ..           ...          ...
        4659  迎驾贡酒  603198  51.67  54.87  ...   33.39   1   39504000000  39504000000
        4660  鹏欣资源  600490   6.02   6.69  ...  108.31   1   13321580216  11995580744
        4661  天沃科技  002564   5.38   5.98  ...  167.87   0    4677239017   4672407358
        4662  创意信息  300366   14.2  14.62  ...   83.92   0    6895559088   5282016749
        4663  谱尼测试  300887   66.0  66.88  ...  155.68   0    8208902349   2047753755
        """
        all_stock_quote_params = (
            ('pn', '1'),
            ('pz', '1000000'),
            ('po', '1'),
            ('np', '1'),
            ('fltt', '2'),
            ('invt', '2'),
            ('fid', 'f3'),
            ('fs', 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23'),
            ('fields', self.all_stock_quote_fields),
        )
        json_response = requests.get(self.all_stock_quote_url,
                                     headers=EastMoneyHeaders, params=all_stock_quote_params).json()
        return pd.DataFrame(json_response['data']['diff']).rename(columns=EastMoneyQuotes)[self.all_stock_quote_columns]

    def get_one_stock_quote_history(self, stock_code: str, beg: str='20210101', end: str='20210630', klt: int = 101, fqt: int=1) -> pd.DataFrame:
        """
        获取单只股票历史k线数据，默认起始时间为2021年1月1日，结束时间为2021年6月30日
        返回k线数据组成的pd.DataFrame
        :param stock_code: 股票代码，str类型，如000001
        :param beg: 起始时间
        :param end: 结束时间
        :param klt: k线间距，默认日k线
                101 -> 日k线
                102 -> 周k线
                1   -> 1分钱k线
                5   -> 5分钟k线
        :param fqt: 复权方式，默认前复权
                0 -> 不复权
                1 -> 前复权
                2 -> 后复权
        :return:
                包含历史k线的股票数据，pd.DataFrame
        """
        security_id = gen_security_id(stock_code)
        one_stock_quote_history_params = (
            ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
            ('fields2', self.stock_quote_history_fields),
            ('beg', beg),
            ('end', end),
            ('rtntype', '6'),
            ('secid', security_id),
            ('klt', f'{klt}'),
            ('fqt', f'{fqt}'),
        )
        json_response = requests.get(self.stock_quote_history_url, headers=EastMoneyHeaders,
                                     params=one_stock_quote_history_params).json()
        data = json_response.get('data')
        assert isinstance(data, object)
        return data
