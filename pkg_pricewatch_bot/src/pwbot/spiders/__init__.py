# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import os, logging, graypy, treq, json
from scrapy import signals
from scrapy.spiders import CrawlSpider
from scrapy.exceptions import DropItem
from pwbot.settings import config

class BasePwbotCrawlSpider(CrawlSpider):

    def __init__(self, *a, **kw):
        # add graylog handler
        logging.root.addHandler(graypy.GELFUDPHandler(
            config['Graylog']['host'], int(config['Graylog']['port'])))
        super().__init__(*a, **kw)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        return spider

    def item_scraped(self, item, response, spider):
        # Send the scraped item to the server
        if type(item).__name__ == 'ParentListingItem':
            x = 'amazon_parent_listing'
        elif type(item).__name__ == 'ListingItem':
            x = 'amazon_listing'
        else:
            raise DropItem("Invalid item type - {}".format(type(item).__name__))

        d = treq.post('http://{}:{}/api/resource/{}/'.format(
                    config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port'], x),
            json.dumps(item).encode('ascii'),
            headers={b'Content-Type': [b'application/json']}
        )
        # The next item will be scraped only after
        # deferred (d) is fired
        return d
