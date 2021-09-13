"""
    Doc
"""
import pandas as pd

from my_types.ColumnInfo import ColumnInfo


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
                    int(table[column].isnull().sum()),
                    # ToDo: Error: Object of type bool_ is not JSON serializable while dump to json file
                    bool(pd.to_numeric(table[column], errors='coerce').notnull().all())
                ))
