""" pwbot.spiders
"""

import logging
from scrapy.spiders import CrawlSpider
from pwbot.settings import graylog_handler

class BasePwbotCrawlSpider(CrawlSpider):
    _job_id = None

    def __init__(self, *a, **kw):
        # add graylog handler
        logging.root.addHandler(graylog_handler)
        super().__init__(*a, **kw)
        self._job_id = kw['job_id']
