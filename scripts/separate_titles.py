"""
    Doc
"""
from typing import List

from my_types.Title import Title
from my_types.TitlesDictionary import TitlesDictionary
from utils.io import hook_up


def separate_titles(path_to_titles: str, n_parts: int):
    """
        Doc
    """
    titles: TitlesDictionary = hook_up(path_to_titles)
    n = len(titles.titles)
    titles_in_part = n // n_parts + 1
    titles_list: List[Title] = []

    for (key, value) in titles.titles.items():
        titles_list.append(value)

    for i in range(0, len(titles_list), titles_in_part):
        yield titles_list[i:i + titles_in_part]
