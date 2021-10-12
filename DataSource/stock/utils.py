"""
utils for stock
"""
import os
import time
import pandas as pd
from .config import QUOTES_SAVE_PATH


def get_market_stock_type(stock_code: str, update=True) -> int:
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
    if not os.path.exists(QUOTES_SAVE_PATH):
        from .core import Stock
        s = Stock()
        df = s.get_all_stock_realtime_quote()
        df.to_csv(QUOTES_SAVE_PATH, encoding='utf-8-sig', index=False)
    elif update is False:
        if time.time() - os.path.getmtime(QUOTES_SAVE_PATH) >= 24 * 3600:
            from .core import Stock
            s = Stock()
            df = s.get_all_stock_realtime_quote()
            df.to_csv(QUOTES_SAVE_PATH, encoding='utf-8-sig', index=False)
    else:
        update_local_market_stock_quotes_cache_file(QUOTES_SAVE_PATH)
    df = pd.read_csv(QUOTES_SAVE_PATH, dtype={'股票代码': str})
    df.index = df['股票代码']
    if stock_code in df.index:
        return df.loc[stock_code, '沪/深']
    update_local_market_stock_quotes_cache_file(QUOTES_SAVE_PATH)
    raise KeyError(f'股票代码{0}可能有误，请重新输入'.format(stock_code))


def update_local_market_stock_quotes_cache_file(path: str = None) -> pd.DataFrame:
    """
    更新本地沪深市场基本信息缓存文件
    :param path:
    缓存文件路径
    :return:
    pd.DataFrame
    """
    if path is None:
        path = QUOTES_SAVE_PATH
    from .core import Stock
    s = Stock()
    df = s.get_all_stock_realtime_quote()
    df.to_csv(path, encoding='utf-8-sig', index=False)
    return df


def gen_security_id(stock_code: str):
    """
    生成股票代码
    :param stock_code: stock code
    :return: specific stock code for EastMoney format
    """
    _type = get_market_stock_type(stock_code, update=False)
    # print('security_id is {}'.format(f'{int(_type)}.{stock_code}'))
    return f'{int(_type)}.{stock_code}'
