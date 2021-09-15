"""
    Doc
"""
import os

from my_types.Title import Title
from my_types.TitlesDictionary import TitlesDictionary
from utils.io import hook_up


def get_pages_with_tables_count(path_to_data: str, path_to_titles: str, path_to_only_pages_parsed) -> None:
    """
        Doc
    """
    pages_with_tables_count = 0
    tables_count = 0

    for path in os.listdir(path_to_data):
        if path == '.DS_Store':
            continue

        full_path = os.path.join(path_to_data, path)
        if os.path.isdir(full_path):
            pages_with_tables_count += 1

        for path2 in os.listdir(full_path):
            full_path2 = os.path.join(full_path, path2)
            if os.path.isfile(full_path2):
                tables_count += 1

    titles: TitlesDictionary = hook_up(path_to_titles)
    only_pages_parsed: dict[str, Title] = hook_up(path_to_only_pages_parsed)

    titles_total_count = len(titles.titles)
    titles_downloaded_count = len(only_pages_parsed)

    print(f'Total pages: {titles_total_count},'
          f'\nparsed pages: {titles_downloaded_count},'
          f'\npages with tables: {pages_with_tables_count}'
          f'\nAvg number of tables per page: {(tables_count - pages_with_tables_count) / pages_with_tables_count / 2}')


if __name__ == '__main__':
    path_to_data = '../data'
    path_to_titles = '../titles'
    path_to_only_pages_parsed = '../only_pages_parsed'
    get_pages_with_tables_count(path_to_data, path_to_titles, path_to_only_pages_parsed)
