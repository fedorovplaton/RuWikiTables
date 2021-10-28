import re


class Filter:
    """
        Filter
    """

    def __init__(self,
                 min_cols: int = 0, max_cols: int = 9999999,
                 min_rows: int = 0, max_rows: int = 9999999,
                 min_empty: int = 0, max_empty: int = 999999999999,
                 min_rus_ratio: int = 0, max_rus_ratio: int = 1,
                 max_empty_ratio_table: int = 1,
                 max_empty_ratio_column: int = 1,
                 min_rus_cel_in_table_ratio: int = 0,
                 min_rus_cel_ratio: int = 0,
                 min_rus_cel_in_col_ratio: int = 0,
                 not_rus_symbols_pattern: str = "^([А-Яа-яЁё]+|\d+)",
                 keep_only_pattern: str = "[А-Яа-яЁё]+|\d+",
                 is_keep_only: bool = False,
                 use_white_list_table: bool = False,
                 use_black_list_table: bool = False,
                 use_black_list_column: bool = False,
                 use_white_list_column: bool = False,
                 white_list_table=None,
                 black_list_table=None,
                 black_list_column=None,
                 white_list_column=None,
                 min_rus_col_ratio: int = 0,
                 skip_only_numbers: bool = False):
        """
        :param skip_only_numbers: if true, then will skip columns which contains only numbers
        :param min_rus_ratio: min russian characters and digits ratio in table to whole length
        :param max_rus_ratio: max russian characters and digits ratio in table to whole length
        :param max_empty: max empty count in column to accept column
        :param min_empty: min empty count in column to accept column
        :param min_cols: min columns in table to accept
        :param max_cols: max columns rows in table to accept
        :param min_rows:  min rows in table to accept
        :param max_rows: max rows in table to accept
        :param max_empty_ratio_column: skip column with empty cells ratio more than expected
        :param max_empty_ratio_table: skip table with empty cells ratio more than expected
        :param min_rus_cel_in_table_ratio: skip table with russian cells ratio less than expected
        :param min_rus_cel_ratio: min russian cell ratio to say that cell is russian
        :param min_rus_cel_in_col_ratio: skip column with russian cells ratio in column less than expected
        :param not_rus_symbols_pattern: pattern of russian symbols
        :param keep_only_pattern: pattern of symbols which need to be persisted
        :param is_keep_only: need to filter chars in table
        :param white_list_table: white list of table headers
        :param black_list_table: black list of table headers
        :param black_list_column: black list of column headers
        :param white_list_column: white list of column headers
        :param min_rus_col_ratio: skip column with russian ratio less than expected
        :param use_white_list_table: need to filter white_list_table
        :param use_black_list_table: need to filter use_black_list_table
        :param use_black_list_column: need to filter use_black_list_column
        :param use_white_list_column: need to filter use_white_list_column
        """

        self.use_white_list_column = use_white_list_column
        self.use_black_list_column = use_black_list_column
        self.use_black_list_table = use_black_list_table
        self.use_white_list_table = use_white_list_table
        self.is_keep_only = is_keep_only
        self.keep_only_pattern = re.compile(keep_only_pattern)
        self.not_rus_symbols = re.compile(not_rus_symbols_pattern)
        if black_list_table is None:
            black_list_table = []
        if black_list_column is None:
            black_list_column = []
        if white_list_column is None:
            white_list_column = []
        if white_list_table is None:
            white_list_table = []
        self.black_list_table = black_list_table
        self.white_list_table = white_list_table
        self.white_list_column = white_list_column
        self.black_list_column = black_list_column
        self.min_rus_col_ratio = min_rus_col_ratio
        self.min_rus_cel_in_col_ratio = min_rus_cel_in_col_ratio
        self.min_rus_cel_in_table_ratio = min_rus_cel_in_table_ratio
        self.min_rus_cel_ratio = min_rus_cel_ratio
        self.max_empty_ratio_table = max_empty_ratio_table
        self.max_empty_ratio_column = max_empty_ratio_column
        self.skip_only_numbers = skip_only_numbers
        self.min_rus_ratio = min_rus_ratio
        self.max_rus_ratio = max_rus_ratio
        self.min_empty = min_empty
        self.max_empty = max_empty
        self.min_rows = min_rows
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.min_cols = min_cols
        self.russian_digit = re.compile("[А-Яа-яЁё]+|\d+")
