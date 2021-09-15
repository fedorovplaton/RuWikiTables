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
    max_rows_cell_count = 0

    max_cols = 0
    max_cols_cell_count = 0

    cols_count = dict()
    rows_count = dict()
    length_dict = dict()
    length_russian_dict = dict()
    length_english_dict = dict()

    max_length = 0
    max_length_cell_count = 0

    cell_count = 0
    non_string_count = 0

    null_rows_count = 0
    bar = IncrementalBar('Countdown', max=len(all_files))

    for filename in all_files:
        df = pd.read_csv(filename, sep='|')
        cells = df.shape[0] * df.shape[1]
        bar.next()
        if df.shape[1] > max_cols:
            max_cols = df.shape[1]
            max_cols_cell_count = cells

        if df.shape[0] > max_rows:
            max_rows = df.shape[0]
            max_rows_cell_count = cells

        cols_count[df.shape[1]] = cols_count.get(df.shape[1], 0) + 1
        rows_count[df.shape[0]] = rows_count.get(df.shape[0], 0) + 1
        length = 0
        cell_count += cells
        for i in range(df.shape[0]):  # iterate over rows
            null_rows_count += df.loc[i, :].isna().sum()
            for j in range(df.shape[1]):  # iterate over columns
                string_value = str(df.iat[i, j])
                len1 = len(string_value)
                length += len1  # get cell value
                length_dict[len1] = length_dict.get(len1, 0) + 1
                rus_len = len(re.findall('[а-яА-Я]', string_value))
                en_len = len(re.findall('[a-zA-Z]', string_value))
                length_russian_dict[rus_len] = length_russian_dict.get(rus_len, 0) + 1
                length_english_dict[en_len] = length_russian_dict.get(en_len, 0) + 1
                if not string_value.isalpha():
                    non_string_count += 1

        if length > max_length:
            max_length = length
            max_length_cell_count = cells

    # Table 1
    print("Most length table (x cells): ", max_rows_cell_count)
    print("Most wide table (x cells): ", max_cols_cell_count)
    print("Most popular table (x characters): ", max_length)
    print("Most popular table (x cells): ", max_length_cell_count)

    print(' ')

    cols = 0
    c_c = 0

    for key, value in cols_count.items():
        cols += value
        c_c += key * value

    rows = 0
    r_c = 0
    for key, value in rows_count.items():
        rows += value
        r_c += key * value

    rus = 0
    ruc_c = 0
    for key, value in length_russian_dict.items():
        rus += value
        ruc_c += key * value

    en = 0
    en_c = 0
    for key, value in length_english_dict.items():
        en += value
        en_c += key * value

    l = 0
    l_c = 0
    for key, value in length_dict.items():
        l += value
        l_c += key * value

    # Table 2
    print("Tables count: ", len(all_files))
    print("Avg number of cells per row: ", c_c / cols)
    print("Avg number of cells per column: ", r_c / rows)
    print("Avg number of characters per cell: ", l_c / l)
    print("Avg number of Russian characters per cell: ", ruc_c / rus)
    print("Avg number of Latin characters per cell: ", en_c / en)
    print("Percentage of cells with non-string data: ", non_string_count / cell_count)
    print("Percentage of rows thar are mostly NULL: ", null_rows_count / rows)

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
