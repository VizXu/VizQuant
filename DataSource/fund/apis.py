import pandas as pd
import numpy as np
from typing import List, Union
from .core import Fund


def get_all_fund_codes(ft: str = 'gp') -> pd.DataFrame:
    fund = Fund()
    return fund.get_all_fund_codes(ft)


def get_fund_base_info(code: str) -> pd.DataFrame:
    fund = Fund()
    return fund.get_one_fund_base_info(code)


def get_funds_base_info(codes: Union[str, List[str]]) -> Union[pd.Series, pd.DataFrame]:
    fund = Fund()
    return fund.get_funds_base_info(codes)


def get_fund_history(code: str) -> pd.DataFrame:
    fund = Fund()
    return fund.get_quote_history(code, 40000)
