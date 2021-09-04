from flask import Flask
import threading
import requests
import pandas as pd
from bs4 import BeautifulSoup

# app - simplest Flask server, app.run() to run server
app = Flask(__name__)
# titles - Словарь со всемм названиями страницы русской википедии
# titles['titleA'] = False, Если мы еще не выкачали страницы или не обработали её
# titles['titleB'] = True, Если мы полностью обработали страницу и сохранили результат
titles = {}
# Переменная для храанения общего количества страниц русской вики
# Она инициализируется с самого начала, чтобы показывать пользователям,
# сколько еще названий страниц нужно выкачать
total_titles = None


# Базовый класс для объектов, которые будут работать в отдельном поток
class MyThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name

    def run(self):
        print('You should implement "run" method in child')


# Класс сервера, который будет работать в отдельном потоке,
# Это просто сервер для REST запросов
class RestServer(MyThread):
    def run(self):
        app.run()


# Класс для краулуера, который в отдельном потоке будет выкачивать названия страниц вики
class TitlesCrawler(MyThread):

    # Генератор ссылка для получения 500 названий, начиная со слова apcontinue
    def get_link_by_apcontinue(self, apcontinue):
        return 'https://ru.wikipedia.org/w/api.php?action=query&format=json&list=allpages&' + \
               f'apcontinue={apcontinue}&apnamespace=0&apfilterredir=all&aplimit=500&apdir=ascending'

    def run(self):
        apcontinue = '!'

        '''
        Самый первый знак(в топологической сортировки) с которого могут начинаться страницы - это "!". 
        apcontinue = '!'
        Делаем запрос в алфавитный казатель https://ru.wikipedia.org/wiki/Википедия:Алфавитный_указатель
        И получаем назавания первых 500 страниц
        Также в ответе получаем следующий указатель, начиная с которого пойдут следующие 500 страниц
        и т.д
        Рааботает где-то 40 минут
        '''

        while True:
            # Делаем запрос
            response = requests.get(self.get_link_by_apcontinue(apcontinue))
            data = response.json()
            # Получаем следующий алфавитный указатель и сохраняем его
            apcontinue = data["continue"]["apcontinue"]
            # Получем массив из 500 страниц
            allpages = data["query"]["allpages"]

            # Сохранем названия страниц в словрь со знаечением False, ибо это про название,
            # саму страницу мы еще не выкачали
            for page in allpages:
                titles[page["title"]] = False


# Прописываем пути в аннотации и пишем код
@app.route("/")
def base():
    """
    Base route
    :return:
    """
    return "Hello, World!"


@app.route("/titles_count")
def titles_count():
    """
    Выводит сколько уже названий страниц скачали
    :return:
    """
    return str(len(titles))


@app.route("/total_titles_count")
def total_titles_count():
    """
    Сколько всего страниц в вики
    :return:
    """
    return str(total_titles)


# Скрипт для получения того, сколько всего страниц в русской вики
# Заходит на сайт со статистикой, наход таблицу со статистикой (Она первая)
# Находим там строку про русскую вики
# И берет оттуда просто число
def get_ru_titles_count():
    response = requests.get("https://ru.wikipedia.org/wiki/Википедия:Список_Википедий")
    table_class = "wikitable"
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find('table',{'class':"wikitable"})
    df = pd.read_html(str(indiatable))
    df = pd.DataFrame(df[0])

    return df.loc[df['Код'] == 'ru']['Статей'].values[0]


if __name__ == '__main__':
    # Получем сколько всего страниц в русской викик, чтобы уметь писать "Скачано 400/170000" страниц
    total_titles = get_ru_titles_count()
    # Создаем 1 поток для сервера
    thread1 = RestServer(1, "RestServer")
    # Создаем 1 поток для краулера
    thread2 = TitlesCrawler(2, "TitleCrawler")

    # Start new Threads
    thread1.start()
    thread2.start()
