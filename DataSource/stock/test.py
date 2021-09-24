from .infofetch import get_all_stock_base_info


def get_stock_base_info():
    print("this name is {0}".format(__name__))
    data = get_all_stock_base_info()
    print(data)
