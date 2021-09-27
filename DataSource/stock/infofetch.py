import requests
import pandas as pd
from .config import EastMoneyHeaders
from .config import EastMoneyQuotes
from .config import EastMoneyStockBaseInfo
from .utils import Utils

fields = ",".join(EastMoneyQuotes.keys())
columns = list(EastMoneyQuotes.values())
params = (
    ('pn', '1'),
    ('pz', '1000000'),
    ('po', '1'),
    ('np', '1'),
    ('fltt', '2'),
    ('invt', '2'),
    ('fid', 'f3'),
    ('fs', 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23'),
    ('fields', fields),
)


def get_all_stock_base_info():
    json_response = requests.get('http://76.push2.eastmoney.com/api/qt/clist/get',
                                 headers=EastMoneyHeaders, params=params).json()
    return pd.DataFrame(json_response['data']['diff']).rename(columns=EastMoneyQuotes)[columns]


class Stock(object):
    def __init__(self):
        self.all_stock_info_fields = ",".join(EastMoneyQuotes.keys())
        self.all_stock_info_columns = list(EastMoneyQuotes.values())
        self.base_info_fields = ",".join(EastMoneyStockBaseInfo.keys())
        self.all_stock_info_url = 'http://76.push2.eastmoney.com/api/qt/clist/get'
        self.base_info_url = 'http://push2.eastmoney.com/api/qt/stock/get'

    def get_all_stock_info(self) -> pd.DataFrame:
        stock_info_params = (
            ('pn', '1'),
            ('pz', '1000000'),
            ('po', '1'),
            ('np', '1'),
            ('fltt', '2'),
            ('invt', '2'),
            ('fid', 'f3'),
            ('fs', 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23'),
            ('fields', self.all_stock_info_fields),
        )
        json_response = requests.get(self.all_stock_info_url,
                                     headers=EastMoneyHeaders, params=stock_info_params).json()
        return pd.DataFrame(json_response['data']['diff']).rename(columns=EastMoneyQuotes)[columns]
