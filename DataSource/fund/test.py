import pandas as pd
from .core import Fund

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 100)


def get_one_fund_base_info():
    fund = Fund()
    s = fund.get_one_fund_base_info('003834')
    print(s)


def get_funds_base_info():
    fund = Fund()
    s = fund.get_funds_base_info(['003834', '005669', '001475'])
    print(s)


def get_all_fund_codes():
    fund = Fund()
    s = fund.get_all_fund_codes()
    print(s)


def get_all_gp_fund_codes():
    fund = Fund()
    s = fund.get_all_fund_codes('gp')
    print(s)


def get_fund_history():
    fund = Fund()
    s = fund.get_quote_history('003834')
    print(s)
