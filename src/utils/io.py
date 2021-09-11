import os
import pickle
from typing import Any, List
import json

from src.types.TableInfo import TableInfo
from src.types.Title import Title


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


def dump_parsed_page(table_info_list: List[TableInfo], title: Title) -> None:
    """
        Doc
    """
    page_directory = os.path.join('data', title.page_id)

    if not os.path.exists(page_directory):
        os.mkdir(page_directory)

    with open(f'{page_directory.title()}/page_meta.json', 'w+', encoding='utf-8') as f:
        json.dump({
            "title": title.title,
            "page_id": title.page_id
        }, f, indent=4)

    if len(table_info_list) == 0:
        return

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
                    "page_id": title.page_id
                },
                "title": table_info.title,
                "after_context": table_info.after_context,
                "previous_context": table_info.previous_context,
                "col_count": table_info.col_count,
                "row_count": table_info.row_count,
                "columns": columns
            }, f, indent=4)
