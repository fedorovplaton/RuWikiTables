from functools import reduce

from pandas import DataFrame
import pandas as pd
import re

russian_digit = re.compile("[А-Яа-яЁё]+|\d+")


def calculate_russian_ratio(df: DataFrame):
    df_str = df.to_string(index=False, na_rep="").replace(" ", "").replace("\n", "").replace(",", "")
    ru_list = re.findall(russian_digit, df_str)
    return reduce(lambda count, l: count + len(l), ru_list, 0) / len(df_str)


def filter_table(table: DataFrame,
                 min_cols=0, max_cols=9999999,
                 min_rows=0, max_rows=9999999,
                 min_empty=0, max_empty=999999999999,
                 min_rus_ratio=0, max_rus_ratio=1,
                 skip_only_numbers=False) -> DataFrame:
    """
    :param skip_only_numbers: if true, then will skip columns which contains only numbers
    :param min_rus_ratio: min russian characters and digits count in table to whole length
    :param max_rus_ratio: max russian characters and digits count in table to whole length
    :param max_empty: max empty count in column to accept column
    :param min_empty: min empty count in column to accept column
    :param min_cols: min columns in table to accept
    :param max_cols: max columns rows in table to accept
    :param min_rows:  min rows in table to accept
    :param max_rows: max rows in table to accept
    :param table: DataFrame table
    :return:  filtered DataFrame
    """

    try:
        result = DataFrame()
        for column in table:
            empty_count = int(table[column].isnull().sum())
            if min_empty > empty_count or empty_count > max_empty:
                continue
            only_numbers = bool(pd.to_numeric(table[column], errors='coerce').notnull().all())
            if skip_only_numbers and only_numbers:
                continue
            result[column] = table[column]
        if min_cols > result.shape[1] or result.shape[1] > max_cols:
            return None
        if min_rows > result.shape[0] or result.shape[0] > max_rows:
            return None
        ru_ratio = calculate_russian_ratio(result)
        if min_rus_ratio > ru_ratio or ru_ratio > max_rus_ratio:
            return None
        return result
    except Exception:
        return None
