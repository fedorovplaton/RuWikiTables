"""
    Doc
"""


class TitlesCrawlerStatus:
    """
        Doc
    """

    def __init__(self, is_loading: bool = False, is_finished: bool = False):
        self.is_loading: bool = is_loading
        self.is_finished: bool = is_finished

    def __str__(self):
        return f'is_loading: {self.is_loading}], is_finished: {self.is_finished}'
