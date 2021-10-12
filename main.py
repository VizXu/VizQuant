# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import DataSource.test as dt
import DataSource.stock as ds

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dt.say_hello()
    # ds.test.get_all_stocks_realtime_quote()
    ds.test.get_stock_quote_history_single()
    # data = ds.test.get_stock_base_info()
    # ds.test.test_requests()
    # ds.test.get_quote_base_info_single()
    # ds.test.get_quote_base_info_multi()
    # ds.test.get_quote_base_info()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
