from .config import EastMoneyHeaders
from .config import EastMoneyQuotes
from .config import EastMoneyStockBaseInfo
from .config import EastMoneyBills
from .config import EastMoneyKLines
from .utils import gen_security_id
from .utils import update_local_market_stock_quotes_cache_file
import requests
import pandas as pd
from typing import List, Dict, Union
import multitasking
from retry import retry
from tqdm import tqdm
import datetime


# fields = ",".join(EastMoneyQuotes.keys())
# columns = list(EastMoneyQuotes.values())
# params = (
#     ('pn', '1'),
#     ('pz', '1000000'),
#     ('po', '1'),
#     ('np', '1'),
#     ('fltt', '2'),
#     ('invt', '2'),
#     ('fid', 'f3'),
#     ('fs', 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23'),
#     ('fields', fields),
# )
#
#
# def get_all_stock_base_info():
#     json_response = requests.get('http://76.push2.eastmoney.com/api/qt/clist/get',
#                                  headers=EastMoneyHeaders, params=params).json()
#     return pd.DataFrame(json_response['data']['diff']).rename(columns=EastMoneyQuotes)[columns]


class Stock(object):
    def __init__(self):
        self.all_stock_quote_url = 'http://76.push2.eastmoney.com/api/qt/clist/get'
        self.all_stock_quote_fields = ",".join(EastMoneyQuotes.keys())
        self.all_stock_quote_columns = list(EastMoneyQuotes.values())
        self.stock_quote_history_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
        self.stock_quote_history_fields = list(EastMoneyKLines.keys())
        self.stock_quote_history_columns = list(EastMoneyKLines.values())
        self.base_info_fields = ",".join(EastMoneyStockBaseInfo.keys())
        self.base_info_url = 'http://push2.eastmoney.com/api/qt/stock/get'

    def get_quote_base_info_single(self, stock_code: str) -> pd.Series:
        """
        获取某只股票基本信息
        :parameter
            stock_code : 股票代码
        :return:
            pd.Series : 包含某只股票的基本信息
        """
        quote_base_info_params = (
            ('ut', 'fa5fd1943c7b386f172d6893dbfba10b'),
            ('invt', '2'),
            ('fltt', '2'),
            ('fields', self.base_info_fields),
            ('secid', gen_security_id(stock_code)),
        )
        json_response = requests.get(self.base_info_url, headers=EastMoneyHeaders, params=quote_base_info_params).json()
        s = pd.Series(json_response['data']).rename(index=EastMoneyStockBaseInfo)
        return s[EastMoneyStockBaseInfo.values()]

    def get_quote_base_info_multi(self, stock_codes: List[str]) -> pd.DataFrame:
        """
        获取多只股票基本信息
        :param stock_codes:
            股票代码，List，可传入多只股票代码
        :return:
            pd.DataFrame 包含多只股票基本信息
        """
        ss = []

        @multitasking.task
        @retry(tries=3, delay=1)
        def start(stock_code: str):
            s = self.get_quote_base_info_single(stock_code)
            ss.append(s)
            bar.update()
            bar.set_description(f'processing {stock_code}')

        bar = tqdm(total=len(stock_codes))
        for stock_code in stock_codes:
            start(stock_code)
        multitasking.wait_for_tasks()
        df = pd.DataFrame(ss)
        return df

    def get_quote_base_info(self, stock_code: Union[str, List[str]]) -> Union[pd.Series, pd.DataFrame]:
        """
        获取股票基本信息
        :param stock_code:
        股票代码或者股票代码组成的链表
        :return:
        如果输入的是单只股票，则返回pd.Series
        如果输入多只股票组成的链表，则返回pd.DataFrame
        效果如下：
             股票代码  股票名称  市盈率(动)    市净率  ...    ROE        净利率           净利润        毛利润
        0  300750  宁德时代  131.16  17.11  ...   6.74  12.082045  4.483788e+09  27.255689
        1  600519  贵州茅台   47.67  14.53  ...  14.20  53.387935  2.465399e+10  91.378421

        [2 rows x 12 columns]
        processing 600519: 100%|██████████| 2/2 [00:00<00:00,  9.28it/s
        """
        if isinstance(stock_code, str):
            return self.get_quote_base_info_single(stock_code)
        elif hasattr(stock_code, '__iter__'):
            return self.get_quote_base_info_multi(stock_code)
        else:
            raise TypeError(f'给定stock_code:{0}错误'.format(stock_code))

    def get_all_stock_realtime_quote(self) -> pd.DataFrame:
        """
        获取沪深市场所有证券及最新报价、涨跌幅等信息
        :return:
        返回pandas.DataFrame,包含沪深市场所有证券最新报价、涨跌幅等信息，如下
              股票名称    股票代码    最新价   昨日收盘  ...   动态市盈率 沪/深           总市值         流通市值
        0      N大地  301068  43.98  13.98  ...   51.19   0    3034920000    647438978
        1     中国能建  601868   2.75   1.96  ...   24.36   1  114650699999  32094609998
        2     恒锋工具  300488  40.13  33.44  ...   52.61   0    6648709547   5485635481
        3     聚石化学  688669  44.27  36.89  ...   38.34   1    4131866696    881353545
        4     晓程科技  300139  10.74   8.95  ...  216.76   0    2942760000   2497984649
        ...    ...     ...    ...    ...  ...     ...  ..           ...          ...
        4659  迎驾贡酒  603198  51.67  54.87  ...   33.39   1   39504000000  39504000000
        4660  鹏欣资源  600490   6.02   6.69  ...  108.31   1   13321580216  11995580744
        4661  天沃科技  002564   5.38   5.98  ...  167.87   0    4677239017   4672407358
        4662  创意信息  300366   14.2  14.62  ...   83.92   0    6895559088   5282016749
        4663  谱尼测试  300887   66.0  66.88  ...  155.68   0    8208902349   2047753755
        """
        all_stock_quote_params = (
            ('pn', '1'),
            ('pz', '1000000'),
            ('po', '1'),
            ('np', '1'),
            ('fltt', '2'),
            ('invt', '2'),
            ('fid', 'f3'),
            ('fs', 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23'),
            ('fields', self.all_stock_quote_fields),
        )
        json_response = requests.get(self.all_stock_quote_url,
                                     headers=EastMoneyHeaders, params=all_stock_quote_params).json()
        return pd.DataFrame(json_response['data']['diff']).rename(columns=EastMoneyQuotes)[self.all_stock_quote_columns]

    def get_stock_quote_history_single(self, stock_code: str,
                                       beg: str = None,
                                       end: str = None,
                                       klt: int = 101,
                                       fqt: int = 1) -> pd.DataFrame:
        """
        获取单只股票历史k线数据，默认起始时间为2021年1月1日，结束时间为2021年6月30日
        返回k线数据组成的pd.DataFrame
        :param stock_code: 股票代码，str类型，如000001
        :param beg: 起始时间
        :param end: 结束时间
        :param klt: k线间距，默认日k线
                101 -> 日k线
                102 -> 周k线
                1   -> 1分钱k线
                5   -> 5分钟k线
        :param fqt: 复权方式，默认前复权
                0 -> 不复权
                1 -> 前复权
                2 -> 后复权
        :return:
                包含历史k线的股票数据，pd.DataFrame
        """
        if end is None:
            end = datetime.datetime.now().strftime("%Y%m%d"),
        if beg is None:
            beg = (datetime.datetime.now() - datetime.timedelta(days=180)).strftime("%Y%m%d"),
        security_id = gen_security_id(stock_code)
        fields = ",".join(self.stock_quote_history_fields)
        one_stock_quote_history_params = (
            ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
            ('fields2', fields),
            ('beg', beg),
            ('end', end),
            ('rtntype', '6'),
            ('secid', security_id),
            ('klt', f'{klt}'),
            ('fqt', f'{fqt}'),
        )
        json_response = requests.get(self.stock_quote_history_url, headers=EastMoneyHeaders,
                                     params=one_stock_quote_history_params).json()
        data = json_response.get('data')
        if data is None:
            return pd.DataFrame(columns=self.stock_quote_history_columns)
        stock_name = data['name']
        klines: List[str] = data['klines']
        rows = [kline.split(',') for kline in klines]
        df = pd.DataFrame(rows, columns=self.stock_quote_history_columns)
        df.insert(0, '股票代码', [stock_code] * len(df))
        df.insert(0, '股票名称', [stock_name] * len(df))
        return df

    def get_stock_quote_history_multi(self, stock_codes: List[str],
                                      beg: str = None,
                                      end: str = None,
                                      klt: int = 101,
                                      fqt: int = 1,
                                      tries: int = 3) -> Dict[str, pd.DataFrame]:
        if beg is None:
            print("beg is {}".format(beg))
            beg: str = datetime.datetime.now().strftime("%Y%m%d")
        if end is None:
            print("end is {}".format(end))
            end: str = (datetime.datetime.now() - datetime.timedelta(days=180)).strftime("%Y%m%d")
        print("beg = {0}, end = {1}".format(beg, end))
        dfs: Dict[str, pd.DataFrame] = {}
        total = len(stock_codes)
        if total != 0:
            update_local_market_stock_quotes_cache_file()

        @multitasking.task
        @retry(tries=3, delay=1)
        def start(stock_code: str):
            _df = self.get_stock_quote_history_single(stock_code, beg=beg, end=end, klt=klt, fqt=fqt)
            dfs[stock_code] = _df
            pbar.update(1)
            pbar.set_description_str(f'Processing: {0}'.format(stock_code))

        pbar = tqdm(total=total)
        for stock_code in stock_codes:
            start(stock_code)
        multitasking.wait_for_tasks()
        pbar.close()
        return dfs

    def get_stock_quote_history(self, stock_codes: Union[str, List[str]],
                                beg: str = None,
                                end: str = None,
                                klt: int = 101,
                                fqt: int = 1,
                                tries: int = 3) -> pd.DataFrame:
        """
        获取某只或某几只股票在时间[beg, end]区间内的k线数据
        :param stock_codes:
                股票代码，List类型，可以是一只或者多只
        :param beg:
                起始时间，默认执行当日之前半年
        :param end:
                结束时间，默认执行当日
        :param klt: k线间距，默认日k线
                101 -> 日k线
                102 -> 周k线
                1   -> 1分钱k线
                5   -> 5分钟k线
        :param fqt: 复权方式，默认前复权
                0 -> 不复权
                1 -> 前复权
                2 -> 后复权
        :param tries:
                当网络不稳定时尝试3次获取
        :return:
        示例如下：
        Processing: 0: 100%|██████████| 2/2 [00:00<00:00,  3.69it/s]
        {'000001':      股票名称    股票代码          日期     开盘  ...    振幅    涨跌幅    涨跌额   换手率
        0    平安银行  000001  2021-04-19  19.85  ...  6.62   4.43   0.89  0.57
        1    平安银行  000001  2021-04-20  20.90  ...  4.91   2.58   0.54  0.43
        2    平安银行  000001  2021-04-21  22.12  ...  4.18   6.14   1.32  0.82
        3    平安银行  000001  2021-04-22  23.01  ...  1.97  -0.13  -0.03  0.43
        4    平安银行  000001  2021-04-23  23.14  ...  2.54   1.36   0.31  0.42
        ..    ...     ...         ...    ...  ...   ...    ...    ...   ...
        112  平安银行  000001  2021-09-30  18.09  ...  2.70  -1.21  -0.22  0.41
        113  平安银行  000001  2021-10-08  18.17  ...  4.85   3.96   0.71  0.60
        114  平安银行  000001  2021-10-11  19.00  ...  3.97   4.08   0.76  0.75
        115  平安银行  000001  2021-10-12  19.30  ...  2.63  -0.26  -0.05  0.53
        116  平安银行  000001  2021-10-13  19.30  ...  3.82   1.19   0.23  0.42

        [117 rows x 13 columns], '600519':      股票名称    股票代码          日期       开盘  ...    振幅    涨跌幅     涨跌额   换手率
        0    贵州茅台  600519  2021-04-19  2035.71  ...  3.21   1.62   33.02  0.25
        1    贵州茅台  600519  2021-04-20  2051.81  ...  2.85   0.33    6.80  0.23
        2    贵州茅台  600519  2021-04-21  2056.71  ...  1.58  -0.71  -14.80  0.21
        3    贵州茅台  600519  2021-04-22  2070.61  ...  2.31  -1.19  -24.50  0.21
        4    贵州茅台  600519  2021-04-23  2036.68  ...  3.31   2.62   53.44  0.27
        ..    ...     ...         ...      ...  ...   ...    ...     ...   ...
        112  贵州茅台  600519  2021-09-30  1818.18  ...  2.57   0.55   10.00  0.32
        113  贵州茅台  600519  2021-10-08  1822.42  ...  3.87   0.52    9.60  0.38
        114  贵州茅台  600519  2021-10-11  1839.51  ...  3.20   1.50   27.52  0.30
        115  贵州茅台  600519  2021-10-12  1866.00  ...  1.85   0.21    3.87  0.24
        116  贵州茅台  600519  2021-10-13  1870.00  ...  4.70   3.15   58.91  0.40

        [117 rows x 13 columns]}
        """
        if end is None:
            end: str = datetime.datetime.now().strftime("%Y%m%d")
        if beg is None:
            beg: str = (datetime.datetime.now() - datetime.timedelta(days=180))
        if isinstance(stock_codes, str):
            return self.get_stock_quote_history_single(stock_codes, beg, end, klt, fqt, tries)
        elif hasattr(stock_codes, '__iter__'):
            return self.get_stock_quote_history_multi(stock_codes, beg, end, klt, fqt, tries)
        else:
            raise TypeError(f'给定stock_codes:{0}错误'.format(stock_codes))
