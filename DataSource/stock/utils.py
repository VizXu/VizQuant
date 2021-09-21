"""
utils for stock
"""
import pandas as pd
from .config import QUOTES_SAVE_PATH

def get_market_stock_type(stock_code:str, update = True) -> int:
    """
    根据股票代码，如600001，得到所属市场，0表示上证，1表示深证
    :param stock_code: stock code, 六位数股票代码
    :param update:
    :return:
        所属市场，0表示沪市，1表示深市
    :raises
        KeyError
        当获取失败时生成异常KeyError
    """
    return 0

def gen_security_id(stock_code : str):
    """
    生成股票代码
    :param stock_code: stock code
    :return: specific stock code for EastMoney format
    """
    _type = get_market_stock_type(stock_code, update = False)
    return f'{int(_type)}.{stock_code}'
