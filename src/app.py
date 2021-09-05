from flask import Flask
from flask_cors import CORS

from src.model.TitlesCrawler import TitlesCrawler
from src.scripts.get_ru_titles_total_count import get_ru_titles_total_count

# app - simplest Flask server, app.run() to run server
app = Flask(__name__)
CORS(app)
titles_crawler = TitlesCrawler()
ru_titles_total_count = get_ru_titles_total_count()


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
    return str(titles_crawler.get_downloaded_titles__count())


@app.route("/total_titles_count")
def total_titles_count():
    """
    Сколько всего страниц в вики
    :return:
    """
    return str(ru_titles_total_count)


@app.route("/start")
def start():
    """
    Начать скачивать имена страниц
    :return:
    """
    titles_crawler.start_download()

    return 'ok'


@app.route("/stop")
def stop():
    """
    Прекратить скачивать имена страниц
    :return:
    """
    titles_crawler.stop_download()

    return 'ok'


@app.route("/approximate_time")
def approximate_time():
    """
    Примерное время ожидания
    :return:
    """

    return str(titles_crawler.get_approximate_time())


if __name__ == '__main__':
    app.run()
