"""
    Doc
"""
from typing import Dict


class TitlesDictionary:
    """
        Doc
    """

    # titles - Словарь со всемм названиями страницы русской википедии
    # titles['titleA'] = False, Если мы еще не выкачали страницы или не обработали её
    # titles['titleB'] = True, Если мы полностью обработали страницу и сохранили результат
    def __init__(self, titles: Dict[str, bool] = None, ap_continue: str = '!'):
        if titles is None:
            titles = {}

        self.titles = titles
        self.ap_continue = ap_continue

    def __str__(self):
        return f'titles: Dict[{len(self.titles)}], apcontinue: {self.ap_continue}'
