import datetime
import glob
import logging
import os
import pickle
import sys

import requests

import models

logging.basicConfig(filename='Mapping.log', filemode='a', format='%(module)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))
logger.addHandler(logging.StreamHandler(sys.stdout))


def get_date(date_string, allowed_datetime_formats):
    for datetime_format in allowed_datetime_formats:
        try:
            return datetime.datetime.strptime(date_string, datetime_format)
        except ValueError as e:
            logger.warning("Exception: " + str(e))
            logger.info("Next time-format will be used ...")
    logger.warning(f'Please introduce new datetime format for {date_string}')
    logger.warning("Returning None")
    return None


def save_article(article_detail, article_id, data_dir, file_ext):
    with open(os.path.join(data_dir, article_id + file_ext), 'wb') as fp:
        pickle.dump(article_detail, fp)


def load_article(data_dir, file_ext):
    all_history_files = glob.glob(os.path.join(data_dir, "*" + file_ext))
    temp_hold = dict()
    for file in all_history_files:
        with open(file, 'rb') as fp:
            temp_hold[os.path.basename(file).replace(file_ext, '')] = models.Article(**pickle.load(fp))
    return temp_hold


def fetch_url_data(url):
    data = requests.get(url).json()
    return data


def print_article(article):
    print(
        "______________________________________________________________________________________________________________")
    print(article.json(indent=4))
    print(
        "______________________________________________________________________________________________________________")
