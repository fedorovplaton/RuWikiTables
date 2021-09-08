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

    tables_directory = f'{page_directory.title()}/tables'

    if not os.path.exists(tables_directory):
        os.mkdir(tables_directory)

    for index in range(len(table_info_list)):
        table_info = table_info_list[index]
        path = f'{tables_directory}/tables_{index}'

        if not os.path.exists(path):
            os.mkdir(path)

        table_info.table.to_json(f'{path}/table.json', indent=4)

        with open(f'{path}/meta.json', 'w+', encoding='utf-8') as f:
            json.dump({
                "title": table_info.title,
                "after_context": table_info.after_context,
                "previous_context": table_info.previous_context
            }, f, indent=4)

    pass
