"""
    Doc
"""
import os

from src.types.Title import Title
from src.types.TitlesDictionary import TitlesDictionary
from src.utils.io import hook_up


def get_pages_with_tables_count(path_to_data: str, path_to_titles: str, path_to_only_pages_parsed) -> None:
    """
        Doc
    """
    pages_with_tables_count = 0

    for path in os.listdir(path_to_data):
        full_path = os.path.join(path_to_data, path)
        if os.path.isdir(full_path):
            pages_with_tables_count += 1

    titles: TitlesDictionary = hook_up(path_to_titles)
    only_pages_parsed: dict[str, Title] = hook_up(path_to_only_pages_parsed)

    titles_total_count = len(titles.titles)
    titles_downloaded_count = len(only_pages_parsed)

    print(f'Total pages: {titles_total_count}, parsed pages: {titles_downloaded_count}, pages with tables: {pages_with_tables_count}')
