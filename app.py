import json
import os
from typing import List

import chardet
from flask import Flask, jsonify, request
from flask_cors import CORS

from model.DataSetGenerator import DataSetGenerator
from model.PagesCrawler import PagesCrawler
from model.TitlesCrawler import TitlesCrawler

# app - simplest Flask server, app.run() to run server
from my_types.Filter import Filter
from scripts.separate_titles import split_titles
from utils.io import get_exist_title_filenamse, delete_title_filenamse, hook_up

app = Flask(__name__)
CORS(app)
titles_crawler = TitlesCrawler()
pages_crawler = PagesCrawler()
dataset_generator = DataSetGenerator(Filter(), "default")
titles_path = 'titles/titles'
pages_count = 0


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


@app.route("/dataset/filter/set", methods=['POST'])
def set_filter():  # ToDo *Do nothing if generating now*
    """
        Set filter properties. If dataset already generating, then do nothing. Always return Status
        :return:
    """
    global dataset_generator
    try:
        charset = chardet.detect(request.data)['encoding']
        data = json.loads(request.data.decode(charset))
        # properties

        ffilter = Filter(
            min_cols=data['min_cols'],
            max_cols=data['max_cols'],
            min_rows=data['min_rows'],
            max_rows=data['max_rows'],
            min_empty=data['min_empty'],
            max_empty=data['max_empty'],
            min_rus_ratio=data['min_rus_ratio'],
            max_rus_ratio=data['max_rus_ratio'],
            max_empty_ratio_table=data['max_empty_ratio_table'],
            max_empty_ratio_column=data['max_empty_ratio_column'],
            min_rus_cel_in_table_ratio=data['min_rus_cel_in_table_ratio'],
            min_rus_cel_ratio=data['min_rus_cel_ratio'],
            min_rus_cel_in_col_ratio=data['min_rus_cel_in_col_ratio'],
            not_rus_symbols_pattern=data['not_rus_symbols_pattern'],
            keep_only_pattern=data['keep_only_pattern'],
            is_keep_only=data['is_keep_only'],
            use_white_list_table=data['use_white_list_table'],
            use_black_list_table=data['use_black_list_table'],
            use_black_list_column=data['use_black_list_column'],
            use_white_list_column=data['use_white_list_column'],
            white_list_table=data['white_list_table'],
            black_list_table=data['black_list_table'],
            black_list_column=data['black_list_column'],
            white_list_column=data['white_list_column'],
            min_rus_col_ratio=data['min_rus_col_ratio'],
            skip_only_numbers=data['skip_only_numbers'],
        )
        dataset_generator = DataSetGenerator(ffilter, data['dataset_name'])
    except Exception as err:
        print('/dataset/filter/set', err)

    return jsonify({
        "isLoading": dataset_generator.is_loading,
        "isFinished": dataset_generator.is_finished,
        "downloadedCount": dataset_generator.status_counter,
        "totalCount": pages_count
    })


@app.route("/dataset/filter/get", methods=['GET'])
def get_filter():  # ToDo
    """
        Returns current filter properties. By default returns initial filter properties.
        If black/white lists were set by files, then return fields:
        {black_list_table_filename: str, ..., black_list_table: [], ...}, else return:
        {black_list_table_filename: '', ..., black_list_table: str[], ...}
        :return:
    """
    return jsonify({})


@app.route("/dataset/filter/start", methods=['POST'])
def filter_start():
    """
        Start generate dataset
        :return:
    """
    dataset_generator.start()
    return jsonify({
        "isLoading": dataset_generator.is_loading,
        "isFinished": dataset_generator.is_finished,
        "downloadedCount": dataset_generator.status_counter,
        "totalCount": pages_count
    })


@app.route("/dataset/filter/stop", methods=['POST'])
def filter_stop():  # ToDo Delete if there is no stop function
    """
        Stop generate dataset
        :return:
    """
    return jsonify({})


@app.route("/dataset/filter/status", methods=['GET'])
def get_filter_status():
    """
        Return dataset generating status
        :return:
    """

    return jsonify({
        "isLoading": dataset_generator.is_loading,
        "isFinished": dataset_generator.is_finished,
        "downloadedCount": dataset_generator.status_counter,
        "totalCount": pages_count
    })


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('titles'):
        os.mkdir('titles')
    if not os.path.exists('titles_parsed'):
        os.mkdir('titles_parsed')
    if not os.path.exists('datasets'):
        os.mkdir('datasets')
    pages_count = len([name for name in os.listdir('data') if os.path.isdir(name)])

    app.run(host='0.0.0.0')
