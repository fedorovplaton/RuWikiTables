from bs4 import BeautifulSoup
import pandas as pd

from src.types.TableInfo import TableInfo


def parse(html_text: str) -> any:
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
                caption = html_table.find("caption")
                if not caption is None:
                    title = html_table.find("caption").text
                elif html_table.findPreviousSibling() and not html_table.findPreviousSibling().find('span', {'class': "mw-headline"}) is None:
                    title = html_table.findPreviousSibling().find('span', {'class': "mw-headline"}).text
                elif html_table.findPrevious("h2") and not html_table.findPrevious("h2").find('span', {'class': "mw-headline"}) is None:
                    title = html_table.findPrevious("h2").find('span', {'class': "mw-headline"}).text
                tables.append(TableInfo(previous_context, after_context, table, title))
            except Exception as error:
                continue
        return tables
    except Exception as error:
        return tables


class PagesCrawler:
    def __init__(self):
        pass
