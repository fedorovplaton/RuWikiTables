"""
    Crawler model
"""
import os
import requests
from src.types.TitlesDictionary import TitlesDictionary
from threading import Thread

# Переменная для храанения общего количества страниц русской вики
# Она инициализируется с самого начала, чтобы показывать пользователям,
# сколько еще названий страниц нужно выкачать
from src.utils.io import dump, hook_up

total_titles = None


def get_link_by_ap_continue(ap_continue: str) -> str:
    """
    Генератор ссылка для получения 500 названий, начиная со слова ap_continue
    :param ap_continue:
    :return:
    """
    return 'https://ru.wikipedia.org/w/api.php?action=query&format=json&list=allpages&' + \
           f'apcontinue={ap_continue}&apnamespace=0&apfilterredir=all&aplimit=500&apdir=ascending'


class TitlesCrawler:
    """
    Класс для краулуера, который в отдельном потоке будет выкачивать названия страниц вики
    """
    titles: TitlesDictionary
    is_loading: bool = False
    download_thread: Thread

    def __init__(self):
        self.download_thread = Thread(target=self.__downloading)
        self.__load()

    def __downloading(self):
        """
        Самый первый знак(в топологической сортировки) с которого могут начинаться страницы - это "!".
        apcontinue = '!'
        Делаем запрос в алфавитный казатель https://ru.wikipedia.org/wiki/Википедия:Алфавитный_указатель
        И получаем назавания первых 500 страниц
        Также в ответе получаем следующий указатель, начиная с которого пойдут следующие 500 страниц
        и т.д
        Рааботает где-то 40 минут
        """
        while self.is_loading:
            # Делаем запрос
            ap_continue = self.titles.ap_continue
            response = requests.get(get_link_by_ap_continue(ap_continue))
            data = response.json()
            # Получаем следующий алфавитный указатель и сохраняем его
            self.titles.ap_continue = data["continue"]["apcontinue"]
            # Получем массив из 500 страниц
            all_pages = data["query"]["allpages"]

            # Сохранем названия страниц в словрь со знаечением False, ибо это про название,
            # саму страницу мы еще не выкачали
            titles = self.titles.titles

            for page in all_pages:
                titles[page["title"]] = False

            self.__save()
            print(len(titles))

    def __save(self, filename: str = 'titles'):
        dump(self.titles, filename)

    def __load(self, filename: str = 'titles'):
        if os.path.exists(filename):
            self.titles = hook_up(filename)
        else:
            self.titles = TitlesDictionary()

    def start_download(self):
        self.__load()
        self.is_loading = True
        self.download_thread.start()

    def stop_download(self):
        self.is_loading = False
        self.download_thread = Thread(target=self.__downloading)
        self.__save()

    def get_downloaded_titles__count(self):
        return len(self.titles.titles)

    def get_approximate_time(self):
        return "0 days 00:00:00"
