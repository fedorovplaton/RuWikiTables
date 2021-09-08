import math
import sys

from bs4 import BeautifulSoup
import pandas as pd
import os
import threading
import time
from typing import Dict, List

from src.types.Title import Title
from src.types.TitlesDictionary import TitlesDictionary
from src.utils.io import hook_up, dump_parsed_page
from multiprocessing import Pool, Process
from queue import Queue
import requests

from src.types.TableInfo import TableInfo
from src.utils.links import get_ru_wiki_link
import asyncio

import aiohttp

from src.utils.parse import parse_wiki_page


class PagesCrawler:
    titles_dict: TitlesDictionary = {}
    q: Queue = Queue()  # Queue[Title]
    pages_parsed: Dict[str, bool] = {}

    def __init__(self):
        self.__load_titles_dict()
        pass

    def __load_titles_dict(self, filename: str = 'pages_parsed'):
        if os.path.exists(filename):
            self.titles_dict = hook_up(filename)
        elif os.path.exists('titles'):
            self.titles_dict = hook_up('titles')

    async def __worker(self, session, title: Title):
        url = get_ru_wiki_link(title.title)

        async with session.get(url) as resp:
            html_text = await resp.text()
            table_info_list = parse_wiki_page(html_text)
            dump_parsed_page(table_info_list, title)
            self.pages_parsed[title.page_id] = True

    async def __async_init(self, thread_id: int, max_tasks_per_thread: int):
        async with aiohttp.ClientSession() as session:
            tasks = []

            while not self.q.empty() and len(tasks) <= max_tasks_per_thread:
                title: Title = self.q.get()
                task = asyncio.create_task(self.__worker(session, title))
                tasks.append(task)

            print(f'{len(tasks)} tasks created for {thread_id} thread')

            await asyncio.gather(*tasks)

    def __thread_init(self, thread_id: int, max_tasks_per_thread: int):
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.run(self.__async_init(thread_id, max_tasks_per_thread))

    def parsing_threads(self, pages_count: int, threads_count: int = 4):
        i = 0

        for title in self.titles_dict.titles:
            if i > pages_count:
                break

            i += 1
            self.q.put(self.titles_dict.titles[title])

        tasks = []

        pages_at_thread = math.ceil(pages_count / threads_count)

        for j in range(threads_count):
            tasks.append(threading.Thread(target=self.__thread_init, args=(j, pages_at_thread)))

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()
