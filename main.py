# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import DataSource.test as dt
import DataSource.stock as ds
import DataSource.fund as df

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
    df.test.get_funds_base_info()
    # df.test.get_all_fund_codes()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
