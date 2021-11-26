import time

import data_cleaner
import models
import utils
from config import *
from utils import logger


class Application:
    def __init__(self, args):
        self.use_history = args.history
        self.refresh_interval = args.interval
        self.article_list_url = ARTICLE_LIST_URL
        self.article_detail_url = ARTICLE_DETAILS_URL
        self.article_media_url = ARTICLE_MEDIA_URL
        self.article_dict = utils.load_article(DATA_DIR, HISTORY_EXTENSION)

    def start(self):
        """
        Starts the application and loops till infinite based upon set interval.
        :return:
        """
        logger.info("Application started ...")

        while True:
            self.iterate_articles()
            time.sleep(self.refresh_interval * CONVERSION_FACTOR)

    def iterate_articles(self):
        article_list = utils.fetch_url_data(self.article_list_url)
        for article in article_list:
            article_id = article['id']
            logger.info("Processing " + article_id + " article ...")
            if not self.record_exists(article_id):
                article_detail = self.process_articles(article_id)
                self.article_dict[article_id] = models.Article(**article_detail)
                utils.print_article(self.article_dict[article_id])
                utils.save_article(article_detail, article_id, DATA_DIR, HISTORY_EXTENSION)

    def process_articles(self, article_id):
        article_detail = utils.fetch_url_data(self.article_detail_url.format(article_id))
        article_sections = []
        for section in article_detail['sections']:
            section = data_cleaner.remove_html(section, 'text')
            self.process_section(article_id, article_sections, section)

        article_detail['sections'] = article_sections
        article_detail['publication_date'] = utils.get_date(article_detail['pub_date'], ALLOWED_DATE_FORMATS)
        return article_detail

    def process_section(self, article_id, article_sections, section):
        if section['type'] in ['media', 'image']:
            article_sections.append(self.process_media_section(section, article_id))
        else:
            article_sections.append(self.get_section(section['type'])(**section))

    def process_media_section(self, section_data, article_id):
        articles_media = utils.fetch_url_data(self.article_media_url.format(article_id))
        section_per_id = self.__filter_media_data(articles_media, section_data['id'])
        if section_per_id['type'] == 'media':
            section_per_id['publication_date'] = utils.get_date(section_per_id['pub_date'], ALLOWED_DATE_FORMATS)
            return models.MediaSection(**section_per_id)
        elif section_per_id['type'] == 'image':
            return models.ImageSection(**section_per_id)
        else:
            # This should never execute as per current data
            return None

    def record_exists(self, article_id):
        if not self.use_history:
            return False
        else:
            if article_id in self.article_dict:
                return True

    @staticmethod
    def get_section(section_name):
        section_dict = {
            'text': models.TextSection,
            'title': models.TitleSection,
            'lead': models.LeadSection,
            'header': models.HeaderSection
        }
        return section_dict[section_name]

    @staticmethod
    def __filter_media_data(articles_media, media_id):
        for article_media in articles_media:
            if article_media['id'] == media_id:
                return article_media
