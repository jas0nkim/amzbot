# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import logging, graypy

from scrapy.spiders import CrawlSpider

class BaseAmzBotCrawlSpider(CrawlSpider):

    def __init__(self, *a, **kw):
        logging.root.setLevel(logging.DEBUG)
        graylog_handler = graypy.GELFUDPHandler('127.0.0.1', 12201)
        logging.root.addHandler(graylog_handler)
        super().__init__(*a, **kw)
