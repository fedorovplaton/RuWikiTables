"""
    Crawler model
"""
import os
import time
from typing import List

import requests

from src.types.TitlesCrawlerStatus import TitlesCrawlerStatus
from src.types.TitlesDictionary import TitlesDictionary
from threading import Thread

# Переменная для храанения общего количества страниц русской вики
# Она инициализируется с самого начала, чтобы показывать пользователям,
# сколько еще названий страниц нужно выкачать
from src.utils.io import dump, hook_up

total_titles = None


def get_link_by_ap_continue(ap_continue: str) -> str:
    """
    Генератор ссылка для получения 500 названий, начиная со слова ap_continue
    :param ap_continue:
    :return:
    """
    return 'https://ru.wikipedia.org/w/api.php?action=query&format=json&list=allpages&' + \
           f'apcontinue={ap_continue}&apnamespace=0&apfilterredir=all&aplimit=500&apdir=ascending'


class TitlesCrawler:
    """
    Класс для краулуера, который в отдельном потоке будет выкачивать названия страниц вики
    """
    titles: TitlesDictionary
    status: TitlesCrawlerStatus
    download_thread: Thread

    average_speed: float = 0.0  # speed for one title
    downloaded_in_row: int = 0
    times_in_row: List[float] = []

    __AP_CONTINUE_FINISHED_MARKER__ = '__AP_CONTINUE_FINISHED_MARKER__'

    def __init__(self):
        self.download_thread = Thread(target=self.__downloading)
        self.__load()
        is_finished = False
        is_loading = False

        if self.titles.ap_continue == self.__AP_CONTINUE_FINISHED_MARKER__:
            is_finished = True

        self.status = TitlesCrawlerStatus(is_loading, is_finished)

    def __downloading(self):
        iteration = 1

        while self.status.is_loading:
            t1 = time.time()
            ap_continue = self.titles.ap_continue
            response = requests.get(get_link_by_ap_continue(ap_continue))
            data = response.json()

            try:
                ap_continue = data["continue"]["apcontinue"]
            except Exception as error:
                self.titles.ap_continue = self.__AP_CONTINUE_FINISHED_MARKER__
                self.status.is_loading = False
                self.status.is_finished = True
                self.__save()
                break

            self.titles.ap_continue = ap_continue
            print(self.titles.ap_continue)

            try:
                all_pages = data["query"]["allpages"]
            except Exception as error:
                print('DFKLJFKDSFJDSKFJDSJFLDSJFDLSFJDSJK')
                raise error

            titles = self.titles.titles

            for page in all_pages:
                titles[page["title"]] = False

            iteration += 1

            if iteration % 20 == 0:
                self.__save()

            t2 = time.time()

            self.times_in_row.append(t2 - t1)
            self.downloaded_in_row += len(all_pages)

    def __save(self, filename: str = 'titles'):
        dump(self.titles, filename)

    def __load(self, filename: str = 'titles'):
        if os.path.exists(filename):
            self.titles = hook_up(filename)
        else:
            self.titles = TitlesDictionary()

    def start_download(self):
        self.__load()

        if self.status.is_loading:
            return

        if self.titles.ap_continue != self.__AP_CONTINUE_FINISHED_MARKER__:
            self.status.is_loading = True
            self.download_thread.start()
        else:
            self.status.is_finished = True

    def stop_download(self):
        if not self.status.is_loading:
            return

        self.status.is_loading = False
        self.download_thread = Thread(target=self.__downloading)
        self.times_in_row = []
        self.downloaded_in_row = 0

    def get_downloaded_titles__count(self) -> int:
        return len(self.titles.titles)

    def get_approximate_time(self, total_count: int) -> float:
        if self.status.is_finished:
            return 0.0

        if len(self.times_in_row) == 0:
            return 9999999.999999

        t = sum(self.times_in_row)
        count = self.downloaded_in_row
        speed = t / count
        to_download = total_count - self.get_downloaded_titles__count()

        return speed * to_download
