"""
    Titles crawler class
"""
import os
import time
from typing import List, Tuple

import requests

from my_types.Title import Title
from my_types.TitlesDictionary import TitlesDictionary
from threading import Thread

from scripts.get_ru_titles_total_count import get_ru_titles_total_count
from utils.io import dump, hook_up
from utils.links import get_link_by_ap_continue


class TitlesCrawler:
    """
        Class for crawling ru wiki page titles
    """
    titles: TitlesDictionary
    download_thread: Thread

    total_count: int = 0
    average_speed: float = 0.0
    downloaded_in_row: int = 0
    times_in_row: List[float] = []

    is_loading: bool = False
    is_finished: bool = False

    __AP_CONTINUE_FINISHED_MARKER__ = '__AP_CONTINUE_FINISHED_MARKER__'

    def __init__(self):
        self.download_thread = Thread(target=self.__downloading)
        self.total_count = get_ru_titles_total_count()
        self.__load()

        if self.titles.ap_continue == self.__AP_CONTINUE_FINISHED_MARKER__:
            self.is_finished = True

    def __downloading(self):
        iteration = 1

        while self.is_loading:
            print(len(self.titles.titles))
            t1 = time.time()
            ap_continue = self.titles.ap_continue
            link = get_link_by_ap_continue(ap_continue)
            response = requests.get(link)
            data = response.json()

            try:
                ap_continue = data["continue"]["apcontinue"]
            except Exception as error:
                self.titles.ap_continue = self.__AP_CONTINUE_FINISHED_MARKER__
                self.is_loading = False
                self.is_finished = True
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

    def __get_downloaded_titles__count(self) -> int:
        return len(self.titles.titles)

    def __get_approximate_time(self) -> float:
        if self.is_finished:
            return 0.0

        if len(self.times_in_row) == 0:
            return 9999999.999999

        t = sum(self.times_in_row)
        count = self.downloaded_in_row
        speed = t / count
        to_download = self.total_count - self.__get_downloaded_titles__count()

        return speed * to_download

    def start_download(self):
        if self.is_loading:
            return

        self.__load()

        if self.titles.ap_continue != self.__AP_CONTINUE_FINISHED_MARKER__:
            self.is_loading = True
            self.download_thread.start()
        else:
            self.is_finished = True

    def stop_download(self):
        if not self.is_loading:
            return

        self.is_loading = False
        self.download_thread = Thread(target=self.__downloading)
        self.times_in_row = []
        self.downloaded_in_row = 0

    def get_status(self) -> Tuple[bool, bool, int, int, float]:
        """
        :return: Tuple [
            bool,  is loading
            bool,  is process finished,
            int,   downloaded titles count,
            int,   total count for downloading,
            float, approximate time for downloading
        ]
        """

        return self.is_loading, \
               self.is_finished, \
               self.__get_downloaded_titles__count(), \
               self.total_count, \
               self.__get_approximate_time()
