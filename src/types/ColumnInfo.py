"""
    Doc
"""


class ColumnInfo:
    """
        Doc
    """

    def __init__(self, name: str,
                 empty_count: int,
                 only_numbers: bool):
        self.name: str = name
        self.empty_count: int = empty_count
        self.only_numbers: bool = only_numbers
        '''Todo en/ru Какие символы используются в таблице? + время последней версии и номер версии'''
