import os

from utils.io import hook_up


def __load_only_pages_parsed(self):
    print('loading only_pages_parsed')

    if os.path.exists('only_pages_parsed'):
        self.pages_parsed = hook_up('only_pages_parsed')
    else:
        self.pages_parsed = {}


if __name__ == '__main__':
    __load_only_pages_parsed()