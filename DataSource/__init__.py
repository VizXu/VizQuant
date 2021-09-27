import pandas as pd
import re
from typing import Union, Callable
from functools import wraps
from .test import say_hello


def convert_to_numbers(func: Callable):
    """
    convert DataFrame data to numbers
    :param func:
    function
    :return:
    DataFrame or Series
    """
    ignore = ['股票代码', '基金代码', '代码', '沪/深']

    @wraps(func)
    def run(*args, **kwargs):
        values = func(args, kwargs)
        if isinstance(values, pd.DataFrame):
            for column in values.columns:
                if column not in ignore:
                    values[column] = values[column].apply(convert)
        elif isinstance(values, pd.Series):
            for index in values.index:
                if index not in ignore:
                    values[index] = convert(values[index])
        return values

    def convert(o: Union[str, int, float]) -> Union[str, float, int]:
        if not re.findall('\d', str(o)):
            return o
        try:
            o = float(o)
        except Exception as e:
            print(e)
            pass
        return o
    return run
