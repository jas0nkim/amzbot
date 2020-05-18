""" pwbot.spiders
"""

import os
import logging
import graypy
from scrapy.spiders import CrawlSpider
from pwbot.settings import config

class BasePwbotCrawlSpider(CrawlSpider):
    _job_id = None

    def __init__(self, *a, **kw):
        # add graylog handler
        logging.root.addHandler(graypy.GELFUDPHandler(
            config['Graylog']['host'], int(config['Graylog']['port'])))
        super().__init__(*a, **kw)
        self._job_id = kw['job_id']
