import json
import os
from typing import List

import chardet
from flask import Flask, jsonify, request
from flask_cors import CORS

from model.PagesCrawler import PagesCrawler
from model.TitlesCrawler import TitlesCrawler

# app - simplest Flask server, app.run() to run server
from scripts.separate_titles import split_titles
from utils.io import get_exist_title_filenamse, delete_title_filenamse

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
        "totalCount": total_count
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
        "totalCount": total_count
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
        "totalCount": total_count
    })


@app.route("/pages/start", methods=['POST'])
def pages_start():
    """
        Doc
    """
    try:
        charset = chardet.detect(request.data)['encoding']
        data = json.loads(request.data.decode(charset))
        filename = data['filename']
        pages_crawler.start(filename)
        is_loading, is_finished, downloaded_count, total_count = pages_crawler.get_status()

        return jsonify({
            "isLoading": is_loading,
            "isFinished": is_finished,
            "downloadedCount": downloaded_count,
            "totalCount": total_count
        })
    except Exception as err:
        print('pages/split', err)

        return ({
            "isLoading": False,
            "isFinished": False,
            "downloadedCount": 0,
            "totalCount": 0
        })


@app.route("/pages/stop", methods=['POST'])
def pages_stop():
    """
        Doc
    """
    pages_crawler.stop()
    is_loading, is_finished, downloaded_count, total_count = pages_crawler.get_status()

    return jsonify({
        "isLoading": is_loading,
        "isFinished": is_finished,
        "downloadedCount": downloaded_count,
        "totalCount": total_count
    })


@app.route("/pages/status", methods=['GET'])
def pages_status():
    """
        Doc
    """

    is_loading, is_finished, downloaded_count, total_count = pages_crawler.get_status()

    return jsonify({
        "isLoading": is_loading,
        "isFinished": is_finished,
        "downloadedCount": downloaded_count,
        "totalCount": total_count
    })


@app.route("/pages/filenames", methods=['GET'])
def get_filenames():
    """
        Get filenames with titles
    """
    filenames = get_exist_title_filenamse()

    return jsonify({
        "filenames": filenames
    })


@app.route("/pages/split", methods=['POST'])
def split():
    """
        Doc
    """
    try:
        charset = chardet.detect(request.data)['encoding']
        data = json.loads(request.data.decode(charset))
        filename = data['filename']
        machineCount: int = data['machineCount']
        splitNames: List[str] = data['splitNames']
        split_titles(filename, machineCount, splitNames)
    except Exception as err:
        print('pages/split', err)

    filenames = get_exist_title_filenamse()

    return jsonify({
        "filenames": filenames
    })

@app.route("/pages/delete/filenames", methods=['POST'])
def delete_filenames():
    try:
        charset = chardet.detect(request.data)['encoding']
        data = json.loads(request.data.decode(charset))
        filenames = data['filenames']
        if 'titles' in filenames:
            filenames.remove('titles')
        delete_title_filenamse(filenames)
    except Exception as err:
        print('pages/split', err)

    filenames = get_exist_title_filenamse()

    return jsonify({
        "filenames": filenames
    })


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')

    app.run()
