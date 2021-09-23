from .infofetch import get_json_response_data


def show_stock_info():
    print("this name is {0}".format(__name__))
    data = get_json_response_data()
    print(data)
