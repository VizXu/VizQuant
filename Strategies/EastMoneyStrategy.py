import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset
import alphalens
from alphalens.utils import print_table
import json
from tqdm import *
from jqdata import *
import tushare as ts
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn')
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']


## 数据获取
# 获取基金基础信息

def GetFundInfo(start_date: str, end_date: str) -> pd.DataFrame:
    # 按年度获取
    start_period = pd.date_range(start_date, end_date, freq='YS')
    end_period = pd.date_range(start_date, end_date, freq='Y')
    df_list = []
    for start, end in zip(start_period, end_period):
        df_list.append(Query_Fund_Info(start, end))
    return pd.concat(df_list)


# jq数据基金分类之区分股票和混合 没有更细的分类
def Query_Fund_Info(start_date: str, end_date: str) -> pd.DataFrame:
    '''获取某时间段中开放式基金中的股票型、混合型基金数据'''
    q = query(finance.FUND_MAIN_INFO).filter(finance.FUND_MAIN_INFO.operate_mode == '开放式基金',
                                             finance.FUND_MAIN_INFO.underlying_asset_type.in_(
                                                 ['股票型', '混合型']),
                                             finance.FUND_MAIN_INFO.start_date >= start_date,
                                             finance.FUND_MAIN_INFO.start_date <= end_date)
    return finance.run_query(q)


# 获取基金规模数据
def GetFundTotalAsset(ts_code: list, start_date: str, end_date: str) -> pd.DataFrame:
    limit_codes = 3000  # 不能大于3000行
    if len(ts_code) <= limit_codes:
        df = Query_fund_total_asset(ts_code, start_date, end_date)
    else:
        code_list = [ts_code[i:i + limit_codes]
                     for i in range(0, len(ts_code), limit_codes)]
        df_temp = []
        for code in tqdm(code_list, desc='查询基金规模'):
            df_temp.append(Query_fund_total_asset(code, start_date, end_date))
        df = pd.concat(df_temp)
    return df


def Query_fund_total_asset(codes: list, start_date: str, end_date: str) -> pd.DataFrame:
    # 按季度获取
    periods = pd.date_range(start_date, end_date, freq='Q')
    df_list = []
    for rptdate in periods:
        q = query(finance.FUND_PORTFOLIO.code,
                  finance.FUND_PORTFOLIO.period_end,
                  finance.FUND_PORTFOLIO.pub_date,
                  finance.FUND_PORTFOLIO.report_type,
                  finance.FUND_PORTFOLIO.total_asset).filter(
            finance.FUND_PORTFOLIO.code.in_(codes),
            finance.FUND_PORTFOLIO.period_end == rptdate)
        df_list.append(finance.run_query(q))
    df = pd.concat(df_list).reset_index(drop=True)
    return df


# 批量查询
def GetFundsNav(main_code_list: str, start_date: str, end_date: str):
    # 按季度将所有数据拼接在一起
    # 每季度的交易日按60日算 限制为3000行 那么main_code需要分为每组50个
    # 才能保证最获取到所有数据
    temp_list = []
    N = 50
    codes = [main_code[i:i + N] for i in range(0, len(main_code), N)]
    for code in tqdm(codes, desc='查询基金净值'):
        temp_list.append(Query_Fund_Nav(code, start_date, end_date))
    fund_df = pd.concat(temp_list, ignore_index=True)
    return fund_df


# 查询基金累计复权净值
def Query_Fund_Nav(main_code: list, start_date: str, end_date: str) -> pd.DataFrame:
    start_period = pd.date_range(start_date, end_date, freq='QS')
    end_period = pd.date_range(start_date, end_date, freq='Q')

    df_list = []
    for start, end in zip(start_period, end_period):
        q = query(finance.FUND_NET_VALUE.code, finance.FUND_NET_VALUE.day,
                  finance.FUND_NET_VALUE.refactor_net_value).filter(
            finance.FUND_NET_VALUE.code.in_(main_code), finance.FUND_NET_VALUE.day >= start,
                                                        finance.FUND_NET_VALUE.day <= end)
        df_list.append(finance.run_query(q))

    return pd.concat(df_list, ignore_index=True)


# 设置时间范围
start_date, end_date = '2007-01-01', '2021-12-1'
# 获取基金基础数据
fund_info = GetFundInfo(start_date, end_date)
main_code = fund_info['main_code'].unique().tolist()
print('共计%s支基金' % len(main_code))

# 获取基金规模数据(季度)
fund_share = GetFundTotalAsset(main_code, start_date, end_date)
fund_share.to_csv('./fund_share.csv')
