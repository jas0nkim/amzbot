from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider

from amazoncrawler import settings, parsers


class ListingItemsSpider(CrawlSpider):
    """ crawl amazon items
    """
    name = "listing_items"

    allowed_domains = ["amazon.com"]
    # handle_httpstatus_list = [404]

    # crawlera_enabled = False
    # crawlera_apikey = amazonmws_settings.APP_CRAWLERA_API_KEY

    # tor_privoxy_enabled = True
    # rand_user_agent_enabled = True

    # # task related
    # task_id = None
    # ebay_store_id = None

    # # other task related options
    # list_new = False
    # revise_inventory_only = False
    # max_amazon_price = None
    # min_amazon_price = None

    # force_crawl = False
    # dont_list_ebay = False

    __asins = []
    __asin_cache = {}
    # _scraped_parent_asins_cache = {}
    # _dont_parse_pictures = False
    # _dont_parse_variations = False

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        if 'asins' in kw:
            self.__asins = self.__filter_asins(kw['asins'])
    #     if 'dont_parse_pictures' in kw:
    #         self._dont_parse_pictures = kw['dont_parse_pictures']
    #     if 'dont_parse_variations' in kw:
    #         self._dont_parse_variations = kw['dont_parse_variations']
    #     if 'premium' in kw and kw['premium'] == True:
    #         self.tor_privoxy_enabled = False
    #         self.crawlera_enabled = True
    #     if 'task_id' in kw:
    #         self.task_id = kw['task_id']
    #     if 'ebay_store_id' in kw:
    #         self.ebay_store_id = kw['ebay_store_id']
    #     if 'list_new' in kw:
    #         self.list_new = kw['list_new']
    #     if 'revise_inventory_only' in kw:
    #         self.revise_inventory_only = kw['revise_inventory_only']
    #     if 'max_amazon_price' in kw:
    #         self.max_amazon_price = kw['max_amazon_price']
    #     if 'min_amazon_price' in kw:
    #         self.min_amazon_price = kw['min_amazon_price']
    #     if 'force_crawl' in kw:
    #         self.force_crawl = kw['force_crawl']
    #     if 'dont_list_ebay' in kw:
    #         self.dont_list_ebay = kw['dont_list_ebay']

    def start_requests(self):
        if len(self.__asins) < 1:
            raise CloseSpider

        for asin in self.__asins:
            yield Request(settings.AMAZON_COM_ITEM_LINK_FORMAT % asin,
                        callback=parsers.parse_amazon_item,
                        # meta={
                        #     'dont_parse_pictures': self._dont_parse_pictures,
                        #     'dont_parse_variations': self._dont_parse_variations,
                        # }
                        )

    def __filter_asins(self, asins):
        filtered_asins = []
        for asin in asins:
            asin = asin.strip()
            if asin not in self.__asin_cache:
                self.__asin_cache[asin] = True
                filtered_asins.append(asin)
        return filtered_asins

