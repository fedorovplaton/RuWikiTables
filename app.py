import os
from typing import List

from flask import Flask, jsonify
from flask_cors import CORS

from model.PagesCrawler import PagesCrawler
from model.TitlesCrawler import TitlesCrawler
from scripts.get_ru_titles_total_count import get_ru_titles_total_count

# app - simplest Flask server, app.run() to run server
from scripts.separate_titles import separate_titles
from my_types.Title import Title
from my_types.TitlesDictionary import TitlesDictionary
from utils.io import dump

app = Flask(__name__)
CORS(app)
titles_crawler = TitlesCrawler()
pages_crawler = PagesCrawler()


@app.route("/", methods=['GET'])
def base():
    """
    Base route
    :return: str
    """
    return "RuWikiTables"


@app.route("/titles/start", methods=['POST'])
def start():
    """
        Start downloading page titles
    """

    titles_crawler.start_download()
    is_loading, is_finished, downloaded_count, total_count, approximate_time = titles_crawler.get_status()

    return jsonify({
        "isLoading": is_loading,
        "isFinished": is_finished,
        "downloadedCount": downloaded_count,
        "totalCount": total_count,
        "approximateTime": approximate_time
    })


@app.route("/titles/stop", methods=['POST'])
def stop():
    """
        Stop downloading page titles
    """

    titles_crawler.stop_download()
    is_loading, is_finished, downloaded_count, total_count, approximate_time = titles_crawler.get_status()

    return jsonify({
        "isLoading": is_loading,
        "isFinished": is_finished,
        "downloadedCount": downloaded_count,
        "totalCount": total_count,
        "approximateTime": approximate_time
    })


@app.route("/titles/status", methods=['GET'])
def status():
    """
        Get status of page titles downloading
    """

    is_loading, is_finished, downloaded_count, total_count, approximate_time = titles_crawler.get_status()

    return jsonify({
        "isLoading": is_loading,
        "isFinished": is_finished,
        "downloadedCount": downloaded_count,
        "totalCount": total_count,
        "approximateTime": approximate_time
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
    sep: List[List[Title]] = list(separate_titles('titles', 8))

    for i in range(len(sep)):
        d = {}

        for title in sep[i]:
            d[str(title.page_id)] = title

        titles_dictionary = TitlesDictionary(titles=d, ap_continue=TitlesCrawler.__AP_CONTINUE_FINISHED_MARKER__)

        dump(titles_dictionary, f'titles_part_{i}')

    return 'ok'


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')

    app.run()
