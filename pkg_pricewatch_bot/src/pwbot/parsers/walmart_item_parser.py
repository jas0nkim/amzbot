""" pwbot.parsers.walmart_item_parser
"""

import re
import json
import logging
from scrapy.http import JsonRequest, Request
from scrapy.exceptions import IgnoreRequest
from pwbot import settings, utils, parsers
from pwbot.items import ListingItem


class WalmartComItemParser(object):
    _domain = None
    _job_id = None
    _sku = None

    def __init__(self):
        self.logger = logging.getLogger(utils.class_fullname(self))

    def __get_preloaded_data(self, response):
        try:
            _data = response.xpath('//script[@id="item"]/text()').extract()[0]
        except IndexError as e:
            self.logger.exception("{}: [{}][{}] unable to find preloaded data - {}".format(utils.class_fullname(e), self._domain, self._sku, str(e)))
            raise IgnoreRequest
        return json.loads(_data)

    def parse_item(self, response, domain, job_id, crawl_variations=False, lat=None, lng=None):
        self._domain = domain
        self._job_id = job_id
        self._sku = utils.extract_sku_from_url(response.url, self._domain)
        if not self._sku:
            self.logger.exception("[{}][null] Request ignored - no parent SKU".format(self._domain))
            raise IgnoreRequest
        if response.status != 200:
            # broken link or inactive item
            yield self.build_listing_item(response)
        else:
            _data = self.__get_preloaded_data(response)
            if crawl_variations:
                for p in _data.get('item', {}).get('product', {}).get('buyBox', {}).get('products', []):
                    if 'usItemId' in p:
                        yield Request(settings.WALMART_COM_ITEM_LINK_FORMAT.format(self._domain,
                                                                                p['usItemId'],
                                                                                settings.WALMART_COM_ITEM_VARIATION_LINK_POSTFIX),
                                    callback=parsers.parse_walmart_com_item,
                                    errback=parsers.resp_error_handler,
                                    cb_kwargs={
                                        'domain': self._domain,
                                        'job_id': self._job_id,
                                        'crawl_variations': False,
                                        'lat': lat,
                                        'lng': lng,
                                    })
            yield self.build_listing_item(response, data=_data)

    def build_listing_item(self, response, data=None):
        """ response: scrapy.http.response.html.HtmlResponse
            data: json
        """
        listing_item = ListingItem()
        listing_item['url'] = response.request.url
        listing_item['domain'] = self._domain
        listing_item['http_status'] = response.status
        listing_item['data'] = data
        listing_item['job_id'] = self._job_id
        return listing_item

class WalmartCaItemParser(object):
    _domain = None
    _job_id = None
    _parent_sku = None
    _referer_for_jsonrequest = None

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

    def parse_item(self, response, domain, job_id, crawl_variations=False, lat=None, lng=None):
        self._referer_for_jsonrequest = response.request.url
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
            yield JsonRequest(settings.WALMART_CA_API_ITEM_PRICE_LINK_FORMAT.format(self._parent_sku),
                        callback=self.parse_json_response,
                        errback=parsers.resp_error_handler,
                        meta={
                            # crawlera proxy interrupt ajax calls
                            'dont_proxy': True,
                        },
                        headers={
                            'Referer': self._referer_for_jsonrequest,
                        },
                        data={
                            "availabilityStoreId": _data['catchment']['storeId'],
                            "fsa": "L5R", # based on user
                            "experience": _data['common']['experience'],
                            "products": [
                                {
                                    "productId": _data['product']['item']['id'],
                                    "skuIds": _data['product']['item']['skus'],
                                },
                            ],
                            "lang": _data['locale']['lang'],
                        })
            # curl -d '{"availabilityStoreId":"1061","fsa":"M2N","experience":"whiteGM","products":[{"productId":"1455223333562","skuIds":["10271820","10271833","10271990","10272011","10272074","10272294","10272452","10272673","10272930","10273052","6000196162683","6000196162686","6000196162689","6000196162692","6000196162695","6000198676038","6000198676606","6000198676624","6000198676966","6000198677013"]}],"lang":"en"}' -H "Content-Type: application/json" -X POST https://www.walmart.ca/api/product-page/price-offer

            for _, sku_data in _data['entities']['skus'].items():
                if len(sku_data.get('upc', [])) > 0:
                    yield JsonRequest(settings.WALMART_CA_API_ITEM_FIND_IN_STORE_LINK_FORMAT.format(lat=lat,
                                                                                                    lng=lng,
                                                                                                    upc=sku_data['upc'][0],
                                                                                                    pid=self._parent_sku),
                            callback=self.parse_json_response,
                            errback=parsers.resp_error_handler,
                            meta={
                                # crawlera proxy interrupt ajax calls
                                'dont_proxy': True,
                            },
                            headers={
                                'Referer': self._referer_for_jsonrequest,
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

    def parse_json_response(self, response):
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
        """ response: scrapy.http.response.html.HtmlResponse
            data: json
        """
        listing_item = ListingItem()
        listing_item['url'] = response.request.url
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

