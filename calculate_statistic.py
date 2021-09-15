import collections
import re

import pandas as pd
import glob
import matplotlib.pyplot as plt
from progress.bar import IncrementalBar


def calculate_statistic():
    path = 'data'
    all_files = glob.glob(path + "/*/*.csv")
    max_row_len = 0
    max_row_len_filename = ""
    max_col_len = 0
    max_col_len_filename = ""
    max_cells = 0
    max_cells_filename = ""

    max_characters_in_cell = 0
    max_characters_in_cell_filename = ""

    characters_total = 0
    rus_characters_total = 0
    en_characters_total = 0

    only_russian_col_count = 0
    only_english_col_count = 0
    only_numeric_col_count = 0

    rows_total = 0
    cols_total = 0
    cells_total = 0

    rus_reg = re.compile('[а-яА-Я]')
    en_reg = re.compile('[a-zA-Z]')

    non_string_count = 0

    null_rows_count = 0
    null_cols_count = 0

    table_sizes = dict()
    headers = dict()
    most_table_rich_page = dict()
    n_row_tables_count = dict()
    n_col_tables_count = dict()

    bar = IncrementalBar('Countdown', max=len(all_files))

    for filename in all_files:
        page_id = filename.split('/')[1]

        if page_id:
            most_table_rich_page[page_id] = most_table_rich_page.get(page_id, 0) + 1

        df = pd.read_csv(filename, sep='|')
        bar.next()

        cells = df.shape[0] * df.shape[1]
        if max_col_len < df.shape[1]:
            max_col_len = df.shape[1]
            max_col_len_filename = filename
        if max_row_len < df.shape[0]:
            max_row_len = df.shape[0]
            max_row_len_filename = filename
        if max_cells < cells:
            max_cells = cells
            max_cells_filename = filename

        tmp_key = str(df.shape[1]) + "x" + str(df.shape[0])
        table_sizes[tmp_key] = table_sizes.get(tmp_key, 0) + 1

        n_row_tables_count[df.shape[0]] += 1
        n_col_tables_count[df.shape[1]] += 1

        cols_total += df.shape[1]
        rows_total += df.shape[0]
        cells_total += cells
        tmp_length = 0
        for i in range(df.shape[0]):  # iterate over rows
            if df.loc[i, :].isna().sum() > 0.7 * df.shape[1]:
                null_rows_count += 1
            for j in range(df.shape[1]):  # iterate over columns
                string_value = str(df.iat[i, j])
                chars_in_cell = len(string_value)
                tmp_length += chars_in_cell
                characters_total += chars_in_cell
                rus_characters_total += len(rus_reg.findall(string_value))
                en_characters_total += len(en_reg.findall(string_value))
                if not string_value.isalpha():
                    non_string_count += 1

        if max_characters_in_cell < tmp_length:
            max_characters_in_cell = tmp_length
            max_characters_in_cell_filename = filename

        for i in range(df.shape[1]):  # iterate over rows
            if df.iloc[:, [i]].isna().sum()[0] > 0.7 * df.shape[0]:
                null_cols_count += 1

            tmp_is_only_russian = True
            tmp_is_only_english = True
            tmp_is_only_numeric = True
            for j in range(df.shape[0]):  # iterate over columns
                string_value = str(df.iat[j, i])
                if len(rus_reg.findall(string_value)) > 0 or not string_value.isalpha():
                    tmp_is_only_english = False
                if len(en_reg.findall(string_value)) > 0 or not string_value.isalpha():
                    tmp_is_only_russian = False
                if not string_value.isdigit():
                    tmp_is_only_numeric = False
                if not tmp_is_only_russian and not tmp_is_only_english and not tmp_is_only_numeric:
                    break

            if tmp_is_only_russian:
                only_russian_col_count += 1
            if tmp_is_only_english:
                only_english_col_count += 1
            if tmp_is_only_numeric:
                only_numeric_col_count += 1

        for header in df.columns:
            headers[str(header)] = headers.get(header, 0) + 1

    sorted_table_sizes = sorted(table_sizes.items(), key=lambda item: item[1])
    sorted_header_tuples = sorted(headers.items(), key=lambda item: item[1])
    sorted_most_table_rich_page_tuples = sorted(most_table_rich_page.items(), key=lambda item: item[1])
    sorted_n_row_tables_count = sorted(n_row_tables_count.items(), key=lambda item: item[1])
    sorted_n_col_tables_count = sorted(n_col_tables_count.items(), key=lambda item: item[1])

    # Table 1
    tables_count = len(all_files)
    print("Total number of tables: ", tables_count)
    print("Total number of rows: ", rows_total)
    print("Total number of columns: ", cols_total)
    print("Total number of cells: ", cells_total)
    print("Avg cells per table: ", cells_total / tables_count)
    print("Avg numbers of tables per page: ", tables_count / 3960680)
    print("Avg numbers of cells per row: ", cells_total / rows_total)
    print("Avg numbers of cells per column: ", cells_total / cols_total)
    print("Avg numbers of characters per cell: ", characters_total / cells_total)
    print("Avg numbers of Russian characters per cell: ", rus_characters_total / cells_total)
    print("Avg numbers of Latin characters per cell: ", en_characters_total / cells_total)
    print("Percentage of cells with non-string data: ", non_string_count / cells_total)
    print("Percentage of columns that are mostly NULL: ", null_cols_count / cols_total)
    print("Percentage of rows that are mostly NULL: ", null_rows_count / rows_total)
    print("Percentage of columns that contains only Russian characters: ", only_russian_col_count / cols_total)
    print("Percentage of columns that contains only Latin characters: ", only_english_col_count / cols_total)
    print("Percentage of columns that contains only numeric data: ", only_numeric_col_count / cols_total)
    print("Most common table sizes in INVERSED ORDER:", sorted_table_sizes[-10:])
    print("Ten most common headers in INVERSED ORDER:", sorted_header_tuples[-10:])
    print("Most big table (x cells): ", max_cells, max_cells_filename)
    print("Most wide table (x cells): ", max_col_len, max_col_len_filename)
    print("Most long table (x cells): ", max_row_len, max_row_len_filename)
    print("Most populated table: ", max_characters_in_cell, " ", max_characters_in_cell_filename)
    print("Most table-rich page (x tables) in INVERSED ORDER: ", sorted_most_table_rich_page_tuples[-10:])

    print("Dict with rows count: ", sorted_n_row_tables_count)
    print("Dict with cols count: ", sorted_n_col_tables_count)


if __name__ == '__main__':
    calculate_statistic()
