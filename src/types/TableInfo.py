"""
    Doc
"""
from pandas import DataFrame


class TableInfo:
    """
        Doc
    """

    def __init__(self, previous_context: str = "",
                 after_context: str = "",
                 table: DataFrame = DataFrame(),
                 title: str = ""):
        self.previous_context: str = previous_context
        self.after_context: str = after_context
        self.table: DataFrame = table
        self.title: str = title
