"""
    Doc
"""


def get_ru_wiki_link(title: str):
    """
        Doc
    :param title: str, Название страницы
    :return: str, Ссылка на страницувикипедии с соотвествующим названием
    """
    return f'https://ru.wikipedia.org/wiki/{title}'


def get_ru_wkik_link_by_id(page_id: str):
    """
        Doc
    :param page_id:
    :return:
    """
    return f''


def get_link_by_ap_continue(ap_continue: str) -> str:
    """
    Генератор ссылка для получения 500 названий, начиная со слова ap_continue
    :param ap_continue:
    :return:
    """
    return 'https://ru.wikipedia.org/w/api.php?action=query&format=json&list=allpages&' + \
           f'apcontinue={ap_continue}&apnamespace=0&apfilterredir=all&aplimit=500&apdir=ascending'
