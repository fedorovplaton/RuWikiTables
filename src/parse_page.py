# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Todo:
    * Сделать парсер страницы с википедии для получения всего, что нам нужно

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

from src.model import PagesCrawler
from src.types import TableInfo


def parse(html_text: str) -> any:
    """
    :param html_text: html code of wiki page
    :return: ?
    """
    print(html_text)


if __name__ == '__main__':
    # response = requests.get('https://en.wikipedia.org/wiki/Wikipedia:Wikidata')
    response = requests.get('https://en.wikipedia.org/wiki/Help:Table')
    #parse(response.text)
    crawler_parse = PagesCrawler.parse(response.text)
