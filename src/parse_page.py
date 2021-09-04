# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Todo:
    * Сделать парсер страницы с википедии для получения всего, что нам нужно

"""

import requests


def parse(html_text: str) -> any:
    """
    :param html_text: html code of wiki page
    :return: ?
    """

    print(html_text)

    return True


if __name__ == '__main__':
    response = requests.get('https://ru.wikipedia.org/wiki/Премия_«Оскар»_за_лучший_фильм')
    parse(response.text)
