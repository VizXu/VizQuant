import pandas as pd
from .core import Fund

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)


def get_one_fund_base_info():
    fund = Fund()
    s = fund.get_one_fund_base_info('003834')
    print(s)
