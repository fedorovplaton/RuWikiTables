import json
import os
import re
from functools import reduce

import pandas as pd
from pandas import DataFrame

import utils.io
from my_types.Filter import Filter
from my_types.TableInfo import TableInfo
from my_types.Title import Title


class DataSetGenerator:
    """
        DataSetGenerator
    """

    def __init__(self, ffilter: Filter):
        self.ffilter = ffilter

    def __calculate_russian_ratio_in_column(self, column: pd.Series):
        df_str = column.to_string(na_rep="").replace(" ", "").replace("\n", "").replace(",", "")
        ru_list = re.findall(self.ffilter.russian_digit, df_str)
        return reduce(lambda count, l: count + len(l), ru_list, 0) / len(df_str)

    def __calculate_russian_ratio_in_table(self, df: DataFrame):
        df_str = df.to_string(index=False, na_rep="").replace(" ", "").replace("\n", "").replace(",", "")
        ru_list = re.findall(self.ffilter.russian_digit, df_str)
        return reduce(lambda count, l: count + len(l), ru_list, 0) / len(df_str)

    def __is_rus_cell(self, cell_value) -> bool:
        if not cell_value:
            return 0 < self.ffilter.min_rus_cel_ratio
        ru_list = re.findall(self.ffilter.russian_digit, cell_value)
        return reduce(lambda count, l: count + len(l), ru_list, 0) / len(cell_value) < self.ffilter.min_rus_cel_ratio

    def __filter_cell_data(self, cell_value) -> str:
        return self.ffilter.keep_only_pattern.sub('', str(cell_value))

    def __filter_column(self, column_name: str, column: pd.Series):
        empty_count = int(column.isnull().sum())
        if self.ffilter.min_empty > empty_count or empty_count > self.ffilter.max_empty:
            return None
        only_numbers = bool(pd.to_numeric(column, errors='coerce').notnull().all())
        if self.ffilter.skip_only_numbers and only_numbers:
            return None
        empty_ratio = column.isnull().sum() / len(column)
        if self.ffilter.max_empty_ratio_column < empty_ratio:
            return None
        cells_rus_vector = [self.__is_rus_cell(x) for x in column]
        rus_cel_in_col_ratio = sum(cells_rus_vector) / len(cells_rus_vector)
        if self.ffilter.min_rus_cel_in_col_ratio < rus_cel_in_col_ratio:
            return None
        rus_col_ratio = self.__calculate_russian_ratio_in_column(column)
        if self.ffilter.min_rus_col_ratio < rus_col_ratio:
            return None
        if self.ffilter.use_black_list_column and column_name in self.ffilter.black_list_column:
            return None
        if self.ffilter.use_white_list_column and column_name not in self.ffilter.white_list_column:
            return None
        if self.ffilter.is_keep_only:
            result = pd.Series([self.__filter_cell_data(x) for x in column])
            return result
        return column

    def __filter_table(self, table_info: TableInfo) -> TableInfo:
        try:
            result = DataFrame()
            table = table_info.table
            for column in table:
                filtered_column = self.__filter_column(column, table[column])
                if filtered_column:
                    result[column] = filtered_column
            if self.ffilter.min_cols > result.shape[1] or result.shape[1] > self.ffilter.max_cols:
                return None
            if self.ffilter.min_rows > result.shape[0] or result.shape[0] > self.ffilter.max_rows:
                return None
            ru_ratio = self.__calculate_russian_ratio_in_table(result)
            if self.ffilter.min_rus_ratio > ru_ratio or ru_ratio > self.ffilter.max_rus_ratio:
                return None
            empty_ratio = table.isnull().sum().sum() / result.shape[1] * result.shape[0]
            if self.ffilter.max_empty_ratio_table < empty_ratio:
                return None
            if self.ffilter.use_black_list_table and table_info.title in self.ffilter.black_list_table:
                return None
            if self.ffilter.use_white_list_table and table_info.title not in self.ffilter.white_list_table:
                return None
            cells_rus_vector = [self.__is_rus_cell(item) for sublist in table for item in sublist]
            if self.ffilter.min_rus_cel_in_table_ratio > sum(cells_rus_vector) / len(cells_rus_vector):
                return None
            return TableInfo(table_info.previous_context, table_info.after_context, result)
        except Exception:
            return None

    def __load_table_info(self, table_path: str, table_meta_path: str):
        table = pd.read_csv(table_path, sep='|')
        table_info = TableInfo(table=table)
        with open(table_meta_path, 'r') as file:
            table_meta_json = json.load(file)
            table_info.title = table_meta_json["title"]
            table_info.after_context = table_meta_json["after_context"]
            table_info.previous_context = table_meta_json["previous_context"]
            table_info.col_count = table_meta_json["col_count"]
            table_info.row_count = table_meta_json["row_count"]
        return table_info

    def generate(self, dataset_name):
        rootdir = 'data'
        if os.path.exists(dataset_name):
            return
        os.makedirs(dataset_name)
        for subdir, dirs, files in os.walk(rootdir):
            r_table_meta = re.compile("table_\d+_meta.json")
            r_table = re.compile("table_\d+.csv")
            table_meta_list = list(filter(r_table_meta.match, files))
            if len(table_meta_list) < 1:
                continue
            table_meta_path = os.path.join(subdir, table_meta_list[0])
            if len(table_meta_list) < 1:
                continue
            table_list = list(filter(r_table.match, files))
            if len(table_list) < 1:
                continue
            table_path = os.path.join(subdir, table_list[0])
            page_list = list(filter(lambda x: x == "page_meta.json", files))
            if len(page_list) < 1:
                continue
            page_path = os.path.join(subdir, page_list[0])

            table_info_list = []
            filtered_table_info = self.__filter_table(table_meta)
            if filtered_table_info:
                table_info_list.append(filtered_table_info)
            if len(table_info_list) > 0:
                utils.io.dump_parsed_page(table_info_list, title, dataset_name)
