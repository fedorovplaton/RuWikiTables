"""
    Crawler model
"""
import os
import time
from typing import List

import requests

from my_types.Title import Title
from my_types.TitlesCrawlerStatus import TitlesCrawlerStatus
from my_types.TitlesDictionary import TitlesDictionary
from threading import Thread

# Переменная для храанения общего количества страниц русской вики
# Она инициализируется с самого начала, чтобы показывать пользователям,
# сколько еще названий страниц нужно выкачать
from utils.io import dump, hook_up
from utils.links import get_link_by_ap_continue


class TitlesCrawler:
    titles: TitlesDictionary
    status: TitlesCrawlerStatus = TitlesCrawlerStatus()
    download_thread: Thread

    average_speed: float = 0.0
    downloaded_in_row: int = 0
    times_in_row: List[float] = []

    __AP_CONTINUE_FINISHED_MARKER__ = '__AP_CONTINUE_FINISHED_MARKER__'

    def __init__(self):
        self.download_thread = Thread(target=self.__downloading)
        self.__load()

        if self.titles.ap_continue == self.__AP_CONTINUE_FINISHED_MARKER__:
            self.status.is_finished = True

    def __downloading(self):
        iteration = 1

        while self.status.is_loading:
            print(len(self.titles.titles))
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
                print(error)
                break

            self.titles.ap_continue = ap_continue

            try:
                all_pages = data["query"]["allpages"]
            except Exception as error:
                print(error)
                break

            for page in all_pages:
                title = page["title"]
                page_id = page["pageid"]
                self.titles.titles[page_id] = Title(title, str(page_id))

            iteration += 1

            if iteration % 50 == 0:
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
        if self.status.is_loading:
            return

        self.__load()

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
