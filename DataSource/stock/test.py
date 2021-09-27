from .infofetch import get_all_stock_base_info
from .infofetch import Stock


def get_stock_base_info():
    data = get_all_stock_base_info()
    print(data)


def get_all_stocks() -> None:
    s = Stock()
    stocks = s.get_all_stock_info()
    print(stocks)
