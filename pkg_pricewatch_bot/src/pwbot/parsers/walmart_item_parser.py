""" pwbot.parsers.walmart_item_parser
"""

import re
import json
import logging
from scrapy.http import JsonRequest
from scrapy.exceptions import IgnoreRequest
from pwbot import settings, utils, parsers
from pwbot.items import ListingItem


class WalmartComItemParser(object):
    def parse_item(self, response, domain, job_id, crawl_variations=False):
        pass

class WalmartCaItemParser(object):
    _domain = None
    _job_id = None
    _parent_sku = None

    def __init__(self):
        self.logger = logging.getLogger(utils.class_fullname(self))

    def __get_preloaded_data(self, response):
        _pattern = re.compile(r"window\.__PRELOADED_STATE__=({.*?});", re.MULTILINE | re.DOTALL)
        _data = '{}'
        try:
            _data = response.xpath("//script[contains(., 'window.__PRELOADED_STATE__')]/text()").re(_pattern)[0]
        except IndexError as e:
            self.logger.exception("{}: [{}][{}] unable to find preloaded data - {}".format(utils.class_fullname(e), self._domain, self._parent_sku, str(e)))
            raise IgnoreRequest
        return json.loads(_data)

    def parse_item(self, response, domain, job_id, crawl_variations=False):
        self._domain = domain
        self._job_id = job_id
        self._parent_sku = utils.extract_sku_from_url(response.url, self._domain)
        if not self._parent_sku:
            self.logger.exception("[{}][null] Request ignored - no parent SKU".format(self._domain))
            raise IgnoreRequest
        if response.status != 200:
            # broken link or inactive item
            yield self.build_listing_item(response)
        else:
            _data = self.__get_preloaded_data(response)
            yield self.build_listing_item(response, data=_data)
            yield JsonRequest(settings.WALMART_CA_API_ITEM_PRICE_LINK,
                        callback=self.parse_price_offer,
                        errback=parsers.resp_error_handler,
                        meta={
                            # crawlera proxy interrupt ajax calls
                            'dont_proxy': True,
                        },
                        data={
                            "availabilityStoreId": _data['catchment']['storeId'],
                            "fsa": "L5R",
                            "experience": _data['common']['experience'],
                            "products": [
                                {
                                    "productId": _data['product']['item']['id'],
                                    "skuIds": _data['product']['item']['skus'],
                                },
                            ],
                            "lang": _data['locale']['lang'],
                        })

            # r = requests.post('https://www.walmart.ca/api/product-page/price-offer',
            #                     # crawlera proxy interrupt ajax calls
            #                     # proxies={
            #                     #     "https": "https://{}:@{}:{}/".format(settings.CRAWLERA_APIKEY, settings.CRAWLERA_HOST, settings.CRAWLERA_PORT),
            #                     #     "http": "http://{}:@{}:{}/".format(settings.CRAWLERA_APIKEY, settings.CRAWLERA_HOST, settings.CRAWLERA_PORT),
            #                     # },
            #                     # verify=False,
            #                     headers={
            #                         'content-type': 'application/json',
            #                         'accept': '*/*',
            #                         'origin': 'https://www.walmart.ca',
            #                         'referer': 'https://www.walmart.ca/en/ip/scrubstar-womens-core-essentials-stretch-poplin-drawstring-scrub-pant-l/6000201271184?rrid=richrelevance',
            #                         'sec-fetch-dest': 'empty',
            #                         'sec-fetch-mode': 'cors',
            #                         'sec-fetch-site': 'same-origin',
            #                     },
            #                     json={
            #                         "availabilityStoreId":"1061",
            #                         "fsa":"L5R",
            #                         "experience":"whiteGM",
            #                         "products":[{
            #                             "productId":"6000201271184",
            #                             "skuIds":[
            #                                 "6000201271185",
            #                                 "6000201271326",
            #                                 "6000201272766",
            #                                 "6000201272805"]
            #                         }],
            #                         "lang":"en"
            #                     })
            # self.logger.debug("""
            #     Requesting [{}]
            #     through proxy [{}]

            #     Request Headers:
            #     {}

            #     Response Time: {}
            #     Response Code: {}
            #     Response Headers:
            #     {}

            #     """.format('https://www.walmart.ca/api/product-page/price-offer', 
            #                 settings.CRAWLERA_HOST, 
            #                 r.request.headers, 
            #                 r.elapsed.total_seconds(), 
            #                 r.status_code, 
            #                 r.headers))
            # if r.ok:
            #     listing_item = ListingItem()
            #     listing_item['url'] = response.url
            #     listing_item['domain'] = self._domain
            #     listing_item['http_status'] = response.status
            #     listing_item['data'] = r.json()
            #     yield listing_item

            # yield Request('https://www.walmart.ca/api/product-page/price-offer',                        
            #             callback=self.parse_price_offer,
            #             errback=parsers.resp_error_handler,
            #             method='POST',
            #             headers={
            #                 'accept': '*/*',
            #                 'accept-encoding': 'gzip, deflate, br',
            #                 'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
            #                 'cache-control': 'no-cache',
            #                 'content-length': '211',
            #                 'content-type': 'application/json',
            #                 'origin': 'https://www.walmart.ca',
            #                 'pragma': 'no-cache',
            #                 'referer': 'https://www.walmart.ca/en/ip/scrubstar-womens-core-essentials-stretch-poplin-drawstring-scrub-pant-l/6000201271184?rrid=richrelevance',
            #                 'sec-fetch-dest': 'empty',
            #                 'sec-fetch-mode': 'cors',
            #                 'sec-fetch-site': 'same-origin',
            #                 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            #                 'wm_qos.correlation_id': '312aa3cf-022-172149119b1ff4,312aa3cf-022-172149119b1681,312aa3cf-022-172149119b1681',
            #             },
            #             data={
            #                 'products': [
            #                     {
            #                         'productId': _data['product']['item']['id'],
            #                         'skuIds': _data['product']['item']['skus'],
            #                     },
            #                 ],
            #             },
            #             cb_kwargs={
            #                 'domain': self._domain,
            #                 'job_id': self._job_id,
            #                 'crawl_variations': crawl_variations,
            #             })

    def parse_price_offer(self, response):
        try:
            json_data = json.loads(response.text)
        except TypeError as e:
            self.logger.exception("{}: [{}][{}] invalid resp. ({}) - {}".format(utils.class_fullname(e),
                                                                                            self._domain,
                                                                                            self._parent_sku,
                                                                                            response.url,
                                                                                            str(e)))
            raise IgnoreRequest
        except json.decoder.JSONDecodeError as e:
            self.logger.exception("{}: [{}][{}] invalid resp. ({}) - {}".format(utils.class_fullname(e),
                                                                                            self._domain,
                                                                                            self._parent_sku,
                                                                                            response.url,
                                                                                            str(e)))
            raise IgnoreRequest
        else:
            return self.build_listing_item(response, data=json_data)

    def build_listing_item(self, response, data=None):
        """ pwbot.parsers.walmart_item_parser.build_listing_item
            
            response: scrapy.http.response.html.HtmlResponse
            data: json
        """
        listing_item = ListingItem()
        listing_item['url'] = response.url
        listing_item['domain'] = self._domain
        listing_item['http_status'] = response.status
        listing_item['data'] = data
        listing_item['job_id'] = self._job_id
        return listing_item

    # def __parse_item_helper(self, response):
    #     _preloaded_data = self.__get_preloaded_data(response)
    #     data = {}
    #     data['sku'] = _preloaded_data['product']['activeSkuId']
    #     data['parent_sku'] = _preloaded_data['product']['item']['id']
    #     data['variation_skus'] = _preloaded_data['product']['item']['skus']
    #     data['price'] = None
    #     data['original_price'] = None
    #     data['quantity'] = None
    #     data['title'] = _preloaded_data['product']['item']['name']['en']
    #     data['description']
    #     data['specifications']
    #     data['features']
    #     data['review_count'] = _preloaded_data['product']['item']['rating']['totalCount']
    #     data['avg_rating'] = _preloaded_data['product']['item']['rating']['averageRating']
    #     data['brand_name'] = None
    #     data['merchant_id'] = None
    #     data['merchant_name'] = None
    #     return build_listing_item(response, data)

