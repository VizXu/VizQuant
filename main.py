# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd

import DataSource.test as dt
import DataSource.stock as ds
import DataSource.fund as df
import DataAnalysisAPIs.fundamentals as da

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dt.say_hello()
    # ds.test.get_all_stocks_realtime_quote()
    # ds.test.get_stock_quote_history_single()
    # ds.test.get_stock_quote_history_multi()
    # ds.test.get_stock_quote_history()
    # ds.test.plot_stock_quote_tendency_diagram()
    # data = ds.test.get_stock_base_info()
    # ds.test.test_requests()
    # ds.test.get_quote_base_info_single()
    # ds.test.get_quote_base_info_multi()
    # ds.test.get_quote_base_info()
    # df.test.get_one_fund_base_info()
    # df.test.get_funds_base_info()
    # df.test.get_all_fund_codes()
    # da.Fundamentals.get_fund_sharp_ratio(pd.Series(['003834', '005669', '001475']))
    # da.Fundamentals.get_top_sharp_ratio(10)
    # da.Fundamentals.get_all_funds_basic_information()
    # da.Fundamentals.get_top_n_sharp_value_in_all_funds(20)
    # df.test.get_all_gp_fund_codes()
    df.test.get_fund_history()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
