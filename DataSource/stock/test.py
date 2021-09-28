from .core import Stock


def get_all_stocks_realtime_quote() -> None:
    s = Stock()
    stocks = s.get_all_stock_realtime_quote()
    print(stocks)

