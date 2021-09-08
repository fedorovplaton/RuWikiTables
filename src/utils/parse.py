from typing import List

import pandas as pd
from bs4 import BeautifulSoup

import chardet

from src.types.TableInfo import TableInfo

stop_tags = ["h2"]


def find_context_after(words_count: int, html_table):
    result = []
    after = html_table.find_next_sibling()
    while after and after.name not in stop_tags and len(result) < words_count:
        result.extend(after.text.split())
        after = after.find_next_sibling()

    return ' '.join(result[:words_count])


def find_context_previous(words_count: int, html_table):
    result = []
    previous = html_table.findPreviousSibling()
    while previous and previous.name not in stop_tags and len(result) < words_count:
        result = previous.text.split() + result
        previous = previous.findPreviousSibling()

    return ' '.join(result[:words_count])


def parse_wiki_page(html_text: str) -> List[TableInfo]:
    """
    :param html_text: html code of wiki page
    :return: list of TableInfo
    """

    tables = []
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        indiatable = soup.findAll('table', {'class': "wikitable"})
        for html_table in indiatable:
            table = pd.read_html(str(html_table))[0]
            previous_context = ""
            after_context = ""
            title = ""
            try:
                previous_context = find_context_previous(100, html_table)
                after_context = find_context_after(100, html_table)
                caption = html_table.find("caption")
                if not caption is None:
                    title = html_table.find("caption").text
                elif html_table.findPreviousSibling() and not html_table.findPreviousSibling().find('span', {
                    'class': "mw-headline"}) is None:
                    title = html_table.findPreviousSibling().find('span', {'class': "mw-headline"}).text
                elif html_table.findPrevious("h2") and not html_table.findPrevious("h2").find('span', {
                    'class': "mw-headline"}) is None:
                    title = html_table.findPrevious("h2").find('span', {'class': "mw-headline"}).text
                tables.append(TableInfo(previous_context, after_context, table, title))
            except Exception as error:
                continue
        return tables
    except Exception as error:
        return tables