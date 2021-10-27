"""
    Doc
"""
from random import shuffle
from typing import List

from model.TitlesCrawler import TitlesCrawler
from my_types.Title import Title
from my_types.TitlesDictionary import TitlesDictionary
from utils.io import hook_up, dump


def get_list_of_title_list(filename: str, machine_count: int):
    titles: TitlesDictionary = hook_up(f'titles/{filename}')
    n = len(titles.titles)
    titles_in_part = n // machine_count + 1
    titles_list: List[Title] = []

    for (key, value) in titles.titles.items():
        titles_list.append(value)

    shuffle(titles_list)

    for i in range(0, len(titles_list), titles_in_part):
        yield titles_list[i:i + titles_in_part]


def split_titles(filename: str, machine_count: int, split_names: List[str]):
    """
        Doc
    """
    index = 0

    for title_list in get_list_of_title_list(filename, machine_count):
        d = {}

        for title in title_list:
            d[str(title.page_id)] = title

        titles_dictionary = TitlesDictionary(titles=d, ap_continue=TitlesCrawler.__AP_CONTINUE_FINISHED_MARKER__)

        dump(titles_dictionary, f'titles/{split_names[index]}')
        index += 1

