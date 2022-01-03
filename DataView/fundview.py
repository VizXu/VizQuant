import pandas as pd
import numpy as np
import DataSource.fund as dfund
import matplotlib.pyplot as plt


def view_fund_net_value(code: str) -> None:
    df = dfund.get_fund_history(code)
    print(df)
    dr = df['日期']
    net_value = df['单位净值']
    plt.plot(dr, net_value)
    plt.show()
    pass
