import os
import pickle
from typing import Any, List
import json

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
