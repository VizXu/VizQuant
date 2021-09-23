import requests
import pandas as pd
from .config import EastMoneyHeaders
from .config import EastMoneyQuotes

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


def get_json_response_data():
    json_response = requests.get('http://76.push2.eastmoney.com/api/qt/clist/get',
                                 headers=EastMoneyHeaders, params=params).json()
    return pd.DataFrame(json_response['data']['diff']).rename(columns=EastMoneyQuotes)[columns]
