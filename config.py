import os

ARTICLE_LIST_URL = 'https://mapping-test.fra1.digitaloceanspaces.com/data/list.json'
ARTICLE_DETAILS_URL = 'https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{}.json'
ARTICLE_MEDIA_URL = 'https://mapping-test.fra1.digitaloceanspaces.com/data/media/{}.json'

DATA_DIR = os.path.abspath("data_dump")

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

HISTORY_EXTENSION = ".mp"
CONVERSION_FACTOR = 60
ALLOWED_DATE_FORMATS = [
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d-%H;%M;%S'
]
