import os
import pickle
from typing import Any, List
import json

from my_types import Filter
from my_types.TableInfo import TableInfo
from my_types.Title import Title
from os import listdir
from os.path import isfile, join


def dump(obj: Any, filename: str) -> None:
    """
        Dump object to file
        :param obj: Any
        :param filename: str
    """

    file = open(filename, "wb")
    pickle.dump(obj, file)


def hook_up(filename: str) -> Any:
    """
        Hook up object from file
        :param filename: str
        :return: object as Any
    """

    file = open(filename, "rb")

    return pickle.load(file)


def save_filter(ffilter: Filter):
    with open('filter.json', 'w+', encoding='utf-8') as f:
        json.dump({"min_cols": ffilter.min_cols,
                   "max_cols": ffilter.max_cols,
                   "min_rows": ffilter.min_rows,
                   "max_rows": ffilter.max_rows,
                   "min_empty": ffilter.min_empty,
                   "max_empty": ffilter.max_empty,
                   "min_rus_ratio": ffilter.min_rus_ratio,
                   "max_rus_ratio": ffilter.max_rus_ratio,
                   "max_empty_ratio_table": ffilter.max_empty_ratio_table,
                   "max_empty_ratio_column": ffilter.max_empty_ratio_column,
                   "min_rus_cel_in_table_ratio": ffilter.min_rus_cel_in_table_ratio,
                   "min_rus_cel_ratio": ffilter.min_rus_cel_ratio,
                   "min_rus_cel_in_col_ratio": ffilter.min_rus_cel_in_col_ratio,
                   "not_rus_symbols_pattern": ffilter.not_rus_symbols_pattern,
                   "keep_only_pattern": ffilter.keep_only_pattern,
                   "is_keep_only": ffilter.is_keep_only,
                   "use_white_list_table": ffilter.use_white_list_table,
                   "use_black_list_table": ffilter.use_black_list_table,
                   "use_black_list_column": ffilter.use_black_list_column,
                   "use_white_list_column": ffilter.use_white_list_column,
                   "white_list_table": ffilter.white_list_table,
                   "black_list_table": ffilter.black_list_table,
                   "black_list_column": ffilter.black_list_column,
                   "white_list_column": ffilter.white_list_column,
                   "min_rus_col_ratio": ffilter.min_rus_col_ratio,
                   "skip_only_numbers": ffilter.skip_only_numbers
                   }, f, indent=4)


def load_filter() -> Filter:
    with open(f'filter.json', 'r', encoding='utf-8') as f:
        filter_json = json.load(f)
        return Filter(
            min_cols=filter_json['min_cols'],
            max_cols=filter_json['max_cols'],
            min_rows=filter_json['min_rows'],
            max_rows=filter_json['max_rows'],
            min_empty=filter_json['min_empty'],
            max_empty=filter_json['max_empty'],
            min_rus_ratio=filter_json['min_rus_ratio'],
            max_rus_ratio=filter_json['max_rus_ratio'],
            max_empty_ratio_table=filter_json['max_empty_ratio_table'],
            max_empty_ratio_column=filter_json['max_empty_ratio_column'],
            min_rus_cel_in_table_ratio=filter_json['min_rus_cel_in_table_ratio'],
            min_rus_cel_ratio=filter_json['min_rus_cel_ratio'],
            min_rus_cel_in_col_ratio=filter_json['min_rus_cel_in_col_ratio'],
            not_rus_symbols_pattern=filter_json['not_rus_symbols_pattern'],
            keep_only_pattern=filter_json['keep_only_pattern'],
            is_keep_only=filter_json['is_keep_only'],
            use_white_list_table=filter_json['use_white_list_table'],
            use_black_list_table=filter_json['use_black_list_table'],
            use_black_list_column=filter_json['use_black_list_column'],
            use_white_list_column=filter_json['use_white_list_column'],
            white_list_table=filter_json['white_list_table'],
            black_list_table=filter_json['black_list_table'],
            black_list_column=filter_json['black_list_column'],
            white_list_column=filter_json['white_list_column'],
            min_rus_col_ratio=filter_json['min_rus_col_ratio'],
            skip_only_numbers=filter_json['skip_only_numbers'],
        )


def dump_parsed_page(table_info_list: List[TableInfo], title: Title, dir_name='data') -> None:
    """
        Doc
    """
    page_directory = os.path.join(dir_name, str(title.page_id))

    if not os.path.exists(page_directory):
        os.mkdir(page_directory)

    with open(f'{page_directory.title().lower()}/page_meta.json', 'w+', encoding='utf-8') as f:
        json.dump({
            "title": title.title,
            "page_id": str(title.page_id)
        }, f, indent=4)

    for index in range(len(table_info_list)):
        table_info = table_info_list[index]

        table_info.table.to_csv(f'{page_directory}/table_{index}.csv', sep='|', index=False, encoding='utf-8')

        columns = {}
        for column_index in range(len(table_info.columns_info)):
            column_info = table_info.columns_info[column_index]
            columns[column_index] = {
                "name": column_info.name,
                "empty_count": column_info.empty_count,
                "is_only_numbers": column_info.only_numbers
            }

        with open(f'{page_directory}/table_{index}_meta.json', 'w+', encoding='utf-8') as f:
            json.dump({
                "page": {
                    "title": title.title,
                    "page_id": str(title.page_id)
                },
                "title": table_info.title,
                "after_context": table_info.after_context,
                "previous_context": table_info.previous_context,
                "col_count": table_info.col_count,
                "row_count": table_info.row_count,
                "columns": columns
            }, f, indent=4)


def get_exist_title_filenamse() -> List[str]:
    path = 'titles'

    return [f for f in listdir(path) if isfile(join(path, f))]


def delete_title_filenamse(filenames: List[str]):
    for filename in filenames:
        os.remove(f"titles/{filename}")
        os.remove(f"titles_parsed/{filename}_parsed")
