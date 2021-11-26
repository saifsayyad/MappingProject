import os
from collections import namedtuple

import pytest
import requests

import utils
from Application import Application
from config import DATA_DIR
from monkey_testing_data import ARTICLE_LIST_DATA, DUMMY_ARTICLE_DETAILS, MEDIA_DATA

# Initialising application to be used for all test cases
Args = namedtuple('Args', ['history', 'interval'])
args = Args(True, 5)
app = Application(args)


def substitute_func(url):
    """
    Function to mock `fetch_url_data` function in `utils.py`
    :param url:
    :return: Dummy JSON data
    """
    if url == 'https://mapping-test.fra1.digitaloceanspaces.com/data/list.json':
        return ARTICLE_LIST_DATA
    if url == 'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/test_id.json':
        return DUMMY_ARTICLE_DETAILS
    if 'https://mapping-test.fra1.digitaloceanspaces.com/data/articles' in url:
        data = requests.get(url).json()
        return data
    if 'https://mapping-test.fra1.digitaloceanspaces.com/data/media/test_id.json' in url:
        return MEDIA_DATA
    if 'https://mapping-test.fra1.digitaloceanspaces.com/data/media' in url:
        data = requests.get(url).json()
        return data
    else:
        data = requests.get(url).json()
        return data


@pytest.fixture
def setup(monkeypatch):
    monkeypatch.setattr(utils, 'fetch_url_data', substitute_func)
    yield  # Tear down phase
    if os.path.exists(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, 'test_id.mp'))


def test_doc():
    """
    This test will run for all the documents originally hosted on the api and store them in `data_dump`
    directory
    Asserts the name and number of documents present in `data_dump` directory.
    """
    app.iterate_articles()
    all_history_files = os.listdir(DATA_DIR)
    files_to_check = ['7793073.mp', '7793118.mp', '7793136.mp']
    file_match_count = 0
    for file_name in files_to_check:
        for history_file in all_history_files:
            if file_name in history_file:
                file_match_count += 1
    assert file_match_count == 3


def test_new_doc(setup):
    """
    This test uses `setup` fixture to mock the `fetch_url_data`  function, on the second call of
    `iterate_articles` it will receive mock data present in `monkey_testing_data.py` file,

    This data contains extra dummy article id as `test_id`, which mimics new data bing added on API.

    This test asserts if that `test_id` is also present in `data_dump` folder.

    :param setup: fixture
    """
    app.iterate_articles()
    all_history_files = os.listdir(DATA_DIR)
    files_to_check = ['7793073.mp', '7793118.mp', '7793136.mp', 'test_id.mp']
    file_match_count = 0
    for file_name in files_to_check:
        for history_file in all_history_files:
            if file_name in history_file:
                file_match_count += 1
    assert file_match_count == 4
