import glob

import matplotlib.pyplot as plt
import pandas as pd
from progress.bar import IncrementalBar


def calculate_statistic():
    path = 'data'
    all_files = glob.glob(path + "/*/*.csv")

    cols_count = dict()
    rows_count = dict()

    bar = IncrementalBar('Countdown', max=len(all_files))

    for filename in all_files:
        df = pd.read_csv(filename, sep='|')
        bar.next()

        if df.shape[1] <= 100:
            cols_count[df.shape[1]] = cols_count.get(df.shape[1], 0) + 1
        if df.shape[0]:
            rows_count[df.shape[0]] = rows_count.get(df.shape[0], 0) + 1

    x = []
    y = []
    max_key = max(rows_count.keys())
    for i in range(1, max_key + 1):
        k = 0
        x.append(i)
        for key1, value1 in rows_count.items():
            if key1 >= i:
                k += value1
        y.append(k)
    y = [e / len(all_files) for e in y]

    x1 = []
    y1 = []
    max_key = max(cols_count.keys())
    for i in range(1, max_key + 1):
        k = 0
        x1.append(i)
        for key1, value1 in cols_count.items():
            if key1 >= i:
                k += value1
        y1.append(k)
    y1 = [e / len(all_files) for e in y1]

    plt.style.use('seaborn-whitegrid')
    # x = rows_count.keys()
    # y = rows_count.values()
    plt.plot(x, y, 'x', label='at least x rows')
    plt.plot(x1, y1, 'o', label='at least x columns')
    plt.xlabel('Distribution of rows and columns')
    plt.ylabel('Fraction of Web Tables')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    calculate_statistic()
