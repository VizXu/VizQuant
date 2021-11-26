import os
import sys
import pandas as pd
from typing import List, Union
import numpy as np
import seaborn as sns
from scipy.stats import kstest
from scipy import stats
from datetime import datetime


class Fundamentals(object):
    def __init__(self):
        pass

    def get_fund_sharp_ratio(self, fund_codes: Union[pd.Series, pd.DataFrame]) -> float:
        pass