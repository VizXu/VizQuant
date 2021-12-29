import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def view(stock: pd.DataFrame) -> None:
    pass


def view_test() -> None:
    y = np.random.standard_normal((3, 100))
    x = [i for i in range(len(y[0]))]
    print(x)
    print(y)
    print(len(y))
    plt.plot(x, y[0])
    plt.show()
