import os
import threading
from typing import Dict, Tuple, List

from my_types.Title import Title
from my_types.TitlesDictionary import TitlesDictionary
from utils.io import hook_up, dump_parsed_page, dump

from utils.links import get_ru_wiki_link_by_id
import asyncio

import aiohttp

from utils.parse import parse_wiki_page


class PagesCrawler:
    """
        PageCrawler
    """
    titles_dict: TitlesDictionary = {}
    titles_parsed: Dict[str, bool] = {}
    MAX_TASKS: int = 500
    thread: threading.Thread

    average_speed: float = 0.0
    downloaded_in_row: int = 0
    times_in_row: List[float] = []

    is_loading: bool = False
    is_finished: bool = False
    is_stopping_tasks: bool = False

    filename: str = None

    def __init__(self):
        self.thread = threading.Thread(target=self.__run_async_client)
        pass

    async def __worker(self, session, title: Title):
        url = get_ru_wiki_link_by_id(str(title.page_id))

        try:
            async with session.get(url) as resp:
                if resp.status == 429:
                    raise Exception(f'{resp.status} Too many requests')
                if resp.status != 200 and resp.status != 304:
                    print(f'{resp.status} Unknown case {str(title.page_id)} : {title.title}')
                    return
                if resp.status == 200:
                    if not self.is_loading:
                        raise Exception('Stop loading...')

                    html_text = await resp.text()
                    try:
                        table_info_list = parse_wiki_page(html_text)

                        if len(table_info_list) > 0:
                            dump_parsed_page(table_info_list, title)

                        self.titles_parsed[str(str(title.page_id))] = True
                    except Exception as error:
                        print('Parsing error: ', error)  # ToDo log parsing errors
                        self.titles_parsed[str(title.page_id)] = False
        except Exception as error:
            print('Network error:', str(error))
            raise error

    async def __async_client(self) -> int:
        async with aiohttp.ClientSession() as session:
            tasks = []

            for (page_id, title) in self.titles_dict.titles.items():
                if str(page_id) not in self.titles_parsed:
                    if len(tasks) >= self.MAX_TASKS:
                        break

                    task = asyncio.create_task(self.__worker(session, title))
                    tasks.append(task)

            try:
                print(f'start {len(tasks)} tasks...')
                await asyncio.gather(*tasks)

                return len(tasks)
            except Exception as error:
                print('Error in tasks: ', error, '\n --- Stopping tasks...')

                for task in tasks:
                    task.cancel()

                self.is_stopping_tasks = False

                return -1

    def __run_async_client(self):
        asyncio.set_event_loop(asyncio.new_event_loop())

        while self.is_loading:
            tasks_count = asyncio.run(self.__async_client())

            if tasks_count == 0:
                self.is_finished = True
                self.is_loading = False

            self.__save()

    def __load_titles_parsed(self, filename: str):
        if os.path.exists(f'titles_parsed/{filename}_parsed'):
            self.titles_parsed = hook_up(f'titles_parsed/{filename}_parsed')
        else:
            self.titles_parsed = {}

    def __load_titles(self, filename):
        if os.path.exists(f'titles/{filename}'):
            self.titles_dict = hook_up(f'titles/{filename}')
        else:
            self.titles_dict = TitlesDictionary({})

    def __load(self, filename):
        if len(self.titles_parsed) == 0:
            self.__load_titles_parsed(filename)

        if filename != self.filename:
            self.__load_titles(filename)
        else:
            try:
                if self.titles_dict.ap_continue is None:
                    self.__load_titles(filename)
            except Exception as error:
                print('ap_continue error', error)
                self.__load_titles(filename)

    def __save(self):
        dump(self.titles_parsed, f'titles_parsed/{self.filename}_parsed')

    def start(self, filename='titles'):
        if filename == self.filename:
            if self.is_loading or self.is_finished or self.is_stopping_tasks:
                return
        else:
            self.titles_parsed = {}

        self.__load(filename)
        self.is_loading = True
        self.filename = filename
        self.thread.start()

    def stop(self):
        if not self.is_loading or self.is_stopping_tasks:
            return

        self.is_stopping_tasks = True
        self.is_loading = False
        self.thread = threading.Thread(target=self.__run_async_client)

    def get_status(self) -> Tuple[bool, bool, int, int]:
        """
        :return: Tuple [
            bool,  is loading
            bool,  is process finished,
            int,   downloaded titles count,
            int,   total count for downloading
        ]
        """
        try:
            total_count = len(self.titles_dict.titles)
        except Exception:
            total_count = 0

        return self.is_loading, \
               self.is_finished, \
               len(self.titles_parsed), \
               total_count
