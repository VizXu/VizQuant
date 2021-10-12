from .core import Stock


def get_all_stocks_realtime_quote() -> None:
    s = Stock()
    stocks = s.get_all_stock_realtime_quote()
    print(stocks)


def get_stock_quote_history_single() -> None:
    s = Stock()
    history = s.get_stock_quote_history_single('000001')
    print(history)


def get_quote_base_info_single() -> None:
    s = Stock()
    base_info = s.get_quote_base_info_single('600021')
    print(base_info)


def get_quote_base_info_multi() -> None:
    s = Stock()
    base_info = s.get_quote_base_info_multi(['000001', '000002'])
    print(base_info)


def get_quote_base_info() -> None:
    s = Stock()
    base_info = s.get_quote_base_info(['600519', '300750'])
    print(base_info)
