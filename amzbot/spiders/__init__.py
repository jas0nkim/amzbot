# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import os
import logging, graypy
from scrapy.spiders import CrawlSpider

class BaseAmzBotCrawlSpider(CrawlSpider):

    def __init__(self, *a, **kw):
        self.__set_gelfudphandler()
        super().__init__(*a, **kw)

    def __set_gelfudphandler(self):
        # parse graylog config
        _graylog_host = None
        _graylog_port = '0'
        try:
            import configparser
            from djg.settings import APP_CONFIG_FILEPATH
            _config = configparser.ConfigParser()
            _config.read(APP_CONFIG_FILEPATH)
            _graylog_host = _config['Graylog']['host']
            _graylog_port = _config['Graylog']['port']
        except Exception as e:
            raise Exception("Failed to get graylog connection information - {}".format(str(e)))

        logging.root.addHandler(graypy.GELFUDPHandler(_graylog_host, int(_graylog_port)))
