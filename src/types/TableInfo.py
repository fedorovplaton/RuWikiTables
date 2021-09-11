"""
    Doc
"""
import pandas as pd

from src.types.ColumnInfo import ColumnInfo


class TableInfo:
    """
        Doc
    """

    def __init__(self, previous_context: str = "",
                 after_context: str = "",
                 table: pd.DataFrame = pd.DataFrame(),
                 title: str = ""):
        self.previous_context: str = previous_context
        self.after_context: str = after_context
        self.table: pd.DataFrame = table
        self.title: str = title
        self.col_count: int = table.shape[1]
        self.row_count: int = table.shape[0]
        self.columns_info = []

        for column in table:
            self.columns_info.append(
                ColumnInfo(
                    column,
                    table[column].isnull().sum(),
                    pd.to_numeric(table[column], errors='coerce').notnull().all()
                ))
