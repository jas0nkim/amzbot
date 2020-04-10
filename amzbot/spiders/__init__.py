# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import logging, graypy

from scrapy.spiders import CrawlSpider

class BaseAmzBotCrawlSpider(CrawlSpider):

    def __init__(self, *a, **kw):
        self.__set_gelfudphandler()
        super().__init__(*a, **kw)

    def __set_gelfudphandler(self):
        logging.root.addHandler(graypy.GELFUDPHandler('127.0.0.1', 12201))
