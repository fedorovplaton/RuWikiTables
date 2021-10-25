import collections
import re

import pandas as pd
import glob
import matplotlib.pyplot as plt
from progress.bar import IncrementalBar


def calculate_statistic():
    path = 'data'
    all_files = glob.glob(path + "/*/*.csv")
    max_rows = 0
    max_cols = 0
    cells_count = 0

    cols_count = 0
    rows_count = 0

    bar = IncrementalBar('Countdown', max=len(all_files))

    for filename in all_files:
        df = pd.read_csv(filename, sep='|')
        bar.next()
        cells_count += df.shape[0] * df.shape[1]

        max_cols = max(max_cols, df.shape[1])
        max_rows = max(max_rows, df.shape[0])

        cols_count += df.shape[1]
        rows_count += df.shape[0]

    print("Rows: ", rows_count)
    print("Cols: ", cols_count)
    print("Cells: ", cells_count)


if __name__ == '__main__':
    calculate_statistic()
