# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import os
import logging, graypy
from amzbot.settings import config
from scrapy.spiders import CrawlSpider

class BaseAmzBotCrawlSpider(CrawlSpider):

    def __init__(self, *a, **kw):
        self.__set_gelfudphandler()
        super().__init__(*a, **kw)

    def __set_gelfudphandler(self):
        # add graylog handler
        logging.root.addHandler(graypy.GELFUDPHandler(config['Graylog']['host'], int(config['Graylog']['port'])))
