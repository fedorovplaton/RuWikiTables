"""
    Doc
"""
from typing import Dict

from my_types.Title import Title


class TitlesDictionary:
    """
        Doc
    """
    def __init__(self, titles: Dict[str, Title] = None, ap_continue: str = '!'):
        if titles is None:
            titles = {}

        self.titles = titles
        self.ap_continue = ap_continue
