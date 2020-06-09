""" pwbot.parsers.canadiantire_item_parser
"""

import json
import logging
import urllib.parse
from scrapy.http import JsonRequest
from scrapy.exceptions import IgnoreRequest
from pwbot import settings, utils, parsers
from pwbot.items import ListingItem


class CanadiantireCaItemParser(object):
    _domain = None
    _job_id = None
    _sku = None
    _parent_sku = None
    _referer_for_jsonrequest = None

    def __init__(self):
        self.logger = logging.getLogger(utils.class_fullname(self))

    def __get_preloaded_data_components(self, response):
        _data = {}
        for _dcomp in response.xpath('//@data-component').extract():
            _xpath_dconf = response.xpath('//*[@data-component="{}"]/@data-config'.format(_dcomp))
            if len(_xpath_dconf) > 0:
                _data[_dcomp] = json.loads(_xpath_dconf[0].extract())
        return _data

    def parse_item(self, response, domain, job_id, crawl_variations, lat='43.769037', lng='-79.371951'):
        self._referer_for_jsonrequest = response.url
        self._domain = domain
        self._job_id = job_id
        self._sku = utils.extract_sku_from_url(response.url, self._domain)
        if not self._sku:
            self.logger.exception("[{}][null] Request ignored - no SKU".format(self._domain))
            raise IgnoreRequest
        if response.status != 200:
            # broken link or inactive item
            yield self.build_listing_item(response)
        else:
            _data = self.__get_preloaded_data_components(response)
            self._parent_sku = _data.get('SkuSelectors', {}).get('pCode', '{}P'.format(self._sku))
            if crawl_variations:
                _skus = list(_data.get('SkuSelectors', {}).get('skuListProperties', {}).keys())
            else:
                _skus = [self._sku]
            yield self.build_listing_item(response, data=_data)
            yield JsonRequest(settings.CANADIANTIRE_CA_API_STORES_LINK_FORMAT.format(lat=lat, lng=lng, pid=self._parent_sku),
                        callback=self.parse_near_stores,
                        errback=parsers.resp_error_handler,
                        meta={
                            # avoid error - Crawled (503) <GET https://api-triangle.canadiantire.ca/robots.txt>
                            'dont_obey_robotstxt': True,
                        },
                        headers={
                            'Referer': self._referer_for_jsonrequest,
                        },
                        cb_kwargs={
                            'skus': _skus,
                        })

    def parse_near_stores(self, response, skus):
        try:
            json_data = json.loads(response.text)
        except TypeError as e:
            self.logger.exception("{}: [{}][{}] invalid resp. ({}) - {}".format(utils.class_fullname(e),
                                                                                            self._domain,
                                                                                            self._sku,
                                                                                            response.url,
                                                                                            str(e)))
            raise IgnoreRequest
        except json.decoder.JSONDecodeError as e:
            self.logger.exception("{}: [{}][{}] invalid resp. ({}) - {}".format(utils.class_fullname(e),
                                                                                            self._domain,
                                                                                            self._sku,
                                                                                            response.url,
                                                                                            str(e)))
            raise IgnoreRequest
        else:
            store_ids = [i.get('storeNumber', '0') for i in json_data]
            yield self.build_listing_item(response, data=json_data)
            yield JsonRequest(settings.CANADIANTIRE_CA_API_ITEM_PRICE_LINK_FORMAT.format(sku=urllib.parse.quote(','.join(skus)),
                                                                                        store=urllib.parse.quote(','.join(store_ids)),
                                                                                        pid=self._parent_sku),
                        callback=self.parse_api,
                        errback=parsers.resp_error_handler,
                        headers={
                            'Referer': self._referer_for_jsonrequest,
                        })

    def parse_api(self, response):
        try:
            json_data = json.loads(response.text)
        except TypeError as e:
            self.logger.exception("{}: [{}][{}] invalid resp. ({}) - {}".format(utils.class_fullname(e),
                                                                                            self._domain,
                                                                                            self._sku,
                                                                                            response.url,
                                                                                            str(e)))
            raise IgnoreRequest
        except json.decoder.JSONDecodeError as e:
            self.logger.exception("{}: [{}][{}] invalid resp. ({}) - {}".format(utils.class_fullname(e),
                                                                                            self._domain,
                                                                                            self._sku,
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
        listing_item['url'] = response.url
        listing_item['domain'] = self._domain
        listing_item['http_status'] = response.status
        listing_item['data'] = data
        listing_item['job_id'] = self._job_id
        return listing_item

