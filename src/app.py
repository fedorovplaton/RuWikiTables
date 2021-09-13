import os
from typing import List

from flask import Flask, jsonify
from flask_cors import CORS

from src.model.PagesCrawler import PagesCrawler
from src.model.TitlesCrawler import TitlesCrawler
from src.scripts.get_ru_titles_total_count import get_ru_titles_total_count

# app - simplest Flask server, app.run() to run server
from src.scripts.separate_titles import separate_titles
from src.types.Title import Title
from src.types.TitlesDictionary import TitlesDictionary
from src.utils.io import dump

app = Flask(__name__)
CORS(app)
titles_crawler = TitlesCrawler()
pages_crawler = PagesCrawler()
ru_titles_total_count: int = get_ru_titles_total_count()


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

    _status = titles_crawler.status

    return jsonify({
        "value": titles_crawler.get_downloaded_titles__count(),
        "status": {
            "isLoading": _status.is_loading,
            "isFinished": _status.is_finished
        }
    })


@app.route("/total_titles_count")
def total_titles_count():
    """
    Сколько всего страниц в вики
    :return:
    """

    _status = titles_crawler.status

    return jsonify({
        "value": ru_titles_total_count,
        "status": {
            "isLoading": _status.is_loading,
            "isFinished": _status.is_finished
        }
    })


@app.route("/start")
def start():
    """
    Начать скачивать имена страниц
    :return:
    """
    titles_crawler.start_download()

    _status = titles_crawler.status

    return jsonify({
        "isLoading": _status.is_loading,
        "isFinished": _status.is_finished
    })


@app.route("/stop")
def stop():
    """
    Прекратить скачивать имена страниц
    :return:
    """
    titles_crawler.stop_download()
    _status = titles_crawler.status

    return jsonify({
        "isLoading": _status.is_loading,
        "isFinished": _status.is_finished
    })


@app.route("/approximate_time")
def approximate_time():
    """
    Примерное время ожидания
    :return:
    """

    _status = titles_crawler.status

    return jsonify({
        "value": titles_crawler.get_approximate_time(ru_titles_total_count),
        "status": {
            "isLoading": _status.is_loading,
            "isFinished": _status.is_finished
        }
    })


@app.route("/status", methods=['GET'])
def status():
    """
    Возвращает статус, идет ли сейчас загрузка и т.д, инициализация состояния на фронте при обновлении
    :return:
    """
    _status = titles_crawler.status

    return jsonify({
        "isLoading": _status.is_loading,
        "isFinished": _status.is_finished
    })


@app.route("/pages/start")
def pages_start():
    """
        Doc
    """
    pages_crawler.start()

    return 'start parsing...'


@app.route("/pages/stop")
def pages_stop():
    """
        Doc
    """
    pages_crawler.stop()

    return 'start stopping...'


@app.route("/pages/status")
def pages_status():
    """
        Doc
    """

    return jsonify({
        "isLoading": pages_crawler.is_loading,
        "isFinished": pages_crawler.is_finished,
        "isStoppingTasks": pages_crawler.is_stopping_tasks
    })


@app.route("/split")
def split():
    """
        Doc
    """
    sep: List[List[Title]] = list(separate_titles('titles', 6))

    for i in range(len(sep)):
        d = {}

        for title in sep[i]:
            d[title.page_id] = title

        titles_dictionary = TitlesDictionary(titles=d, ap_continue=TitlesCrawler.__AP_CONTINUE_FINISHED_MARKER__)

        dump(titles_dictionary, f'titles_part_{i}')

    return 'ok'


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')

    app.run()
