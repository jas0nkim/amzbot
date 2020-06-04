""" pwbot.parsers.amazon_item_parser
"""

import re
import json
import urllib
import logging
from scrapy import Request
from scrapy.exceptions import IgnoreRequest
from pwbot import utils, settings, parsers
from pwbot.items import ListingItem


class AmazonItemParser(object):
    _domain = None
    _job_id = None
    _asin = None

    def __init__(self):
        self.logger = logging.getLogger('pwbot.parsers.amazon_item_parser.AmazonItemParser')

    """ response scrapy.http.response.html.HtmlResponse
    """
    def parse_item(self, response, domain, job_id, crawl_variations, lat=None, lng=None):
        self._domain = domain
        self._job_id = job_id
        self._asin = utils.extract_sku_from_url(response.url, self._domain)
        if not self._asin:
            self.logger.exception("[ASIN:null] Request Ignored - No ASIN")
            raise IgnoreRequest

        # __stored_variation_asins = []
        # if AmazonItemModelManager.is_given_asin_parent(asin=self._asin):
        #     __stored_variation_asins = AmazonItemModelManager.fetch_its_variation_asins(parent_asin=self._asin)
        #     for sv_asin in __stored_variation_asins:
        #         if sv_asin != self._asin: # ignore any amazon items which have the same parent_asin and asin - which makes endless scrapy requests
        #             yield Request(amazonmws_settings.AMAZON_ITEM_VARIATION_LINK_FORMAT % sv_asin,
        #                     callback=self.parse_item,
        #                     headers={ 'Referer': 'https://www.{}/'.format(domain), },
        #                     meta={
        #                         'dont_parse_pictures': response.meta['dont_parse_pictures'] if 'dont_parse_pictures' in response.meta else False,
        #                         'dont_crawl_variations': True,
        #                     })

        # if 'cached_amazon_item' in response.flags:
        #     self.logger.info("[ASIN:{}] cached amazon item - generating by database".format(asin))
        #     yield self.__build_amazon_item_from_cache(response)
        # else:
        if response.status != 200:
            # broken link or inactive amazon item
            amazon_item = ListingItem()
            amazon_item['url'] = response.url
            amazon_item['domain'] = self._domain
            amazon_item['http_status'] = response.status
            amazon_item['job_id'] = self._job_id
            # if response.status == 404:
                # RemovedVariationHandleMiddleware.__handle_removed_variations related
                # amazon_item['parent_asin'] = None
                # self.logger.error('[ASIN:null] Request Ignored - No ASIN')
            yield amazon_item
        else:
            # check variations first
            """ TODO: __stored_variation_asins = amazon_parent_listings.asins in db
            """
            __variation_asins = self.__extract_variation_asins(response)
            __stored_variation_asins = []
            if crawl_variations:
                if len(__variation_asins) > 0:
                    for v_asin in __variation_asins:
                        if v_asin not in __stored_variation_asins:
                            """ TODO: change settings.AMAZON_ITEM_LINK_FORMAT.format(self._domain, v_asin, settings.AMAZON_ITEM_VARIATION_LINK_POSTFIX to real amazon url (db query) : avoid ban
                            """
                            yield Request(settings.AMAZON_ITEM_LINK_FORMAT.format(self._domain, v_asin, settings.AMAZON_ITEM_VARIATION_LINK_POSTFIX),
                                    callback=parsers.parse_amazon_item,
                                    errback=parsers.resp_error_handler,
                                    headers={'Referer': 'https://www.{}/'.format(self._domain),},
                                    cb_kwargs={
                                        'domain': self._domain,
                                        'job_id': self._job_id,
                                        'crawl_variations': False,
                                    })
                    # self.logger.info("[ASIN:{}] Request Ignored - initial asin ignored".format(self._asin))
                    # raise IgnoreRequest
            yield self.__parse_amazon_item(response, variation_asins=__variation_asins)

                    # if listing_item.get('has_sizechart', False) and not AmazonItemApparelModelManager.fetch_one(parent_asin=__parent_asin):
                    #     amazon_apparel_parser = AmazonApparelParser()
                    #     yield Request(amazonmws_settings.AMAZON_ITEM_APPAREL_SIZE_CHART_LINK_FORMAT % __parent_asin,
                    #             callback=amazon_apparel_parser.parse_apparel_size_chart,
                    #             meta={'asin': __parent_asin},
                    #             dont_filter=True) # we have own filtering function: _filter_asins()


    def __parse_amazon_item(self, response, variation_asins):
        amazon_item = ListingItem()
        amazon_item['url'] = response.url
        amazon_item['domain'] = self._domain
        amazon_item['http_status'] = response.status
        amazon_item['job_id'] = self._job_id

        _parent_asin = self.__extract_parent_asin(response)
        amazon_item['data'] = {
            'asin': self._asin,
            'parent_asin': _parent_asin,
            'variation_asins': variation_asins,
        }
        _price = self.__extract_price(response)
        _quantity = self.__extract_quantity(response)
        if _price is None:
            amazon_item['data']['status'] = settings.RESOURCES_LISTING_ITEM_STATUS_NO_PRICE_GIVEN
        elif _quantity == 0:
            amazon_item['data']['status'] = settings.RESOURCES_LISTING_ITEM_STATUS_OUT_OF_STOCK
        elif self.__extract_asin_on_content(response) != self._asin:
            # invalid asin
            amazon_item['data']['status'] = settings.RESOURCES_LISTING_ITEM_STATUS_INVALID_SKU
        elif self._asin and _parent_asin and self._asin != _parent_asin and len(variation_asins) > 0 and self._asin not in variation_asins:
            # a variation, but removed - inactive this variation
            amazon_item['data']['status'] = settings.RESOURCES_LISTING_ITEM_STATUS_SKU_NOT_IN_VARIATION
        else:
            try:
                amazon_item['data']['picture_urls'] = self.__extract_picture_urls(response)
                amazon_item['data']['category'] = self.__extract_category(response)
                amazon_item['data']['title'] = self.__extract_title(response)
                amazon_item['data']['price'] = _price
                amazon_item['data']['original_price'] = self.__extract_original_price(response, default_price=_price)
                amazon_item['data']['quantity'] = _quantity
                amazon_item['data']['features'] = self.__extract_features(response)
                amazon_item['data']['description'] = self.__extract_description(response)
                amazon_item['data']['specifications'] = self.__extract_specifications(response)
                amazon_item['data']['variation_specifics'] = self.__extract_variation_specifics(response)
                amazon_item['data']['is_fba'] = self.__extract_is_fba(response)
                amazon_item['data']['review_count'] = self.__extract_review_count(response)
                amazon_item['data']['avg_rating'] = self.__extract_avg_rating(response)
                amazon_item['data']['is_addon'] = self.__extract_is_addon(response)
                amazon_item['data']['is_pantry'] = self.__extract_is_pantry(response)
                amazon_item['data']['is_pantry'] = self.__extract_is_pantry(response)
                amazon_item['data']['has_sizechart'] = self.__extract_has_sizechart(response)
                amazon_item['data']['merchant_id'] = self.__extract_merchant_id(response)
                amazon_item['data']['merchant_name'] = self.__extract_merchant_name(response)
                amazon_item['data']['brand_name'] = self.__extract_brand_name(response)
                amazon_item['data']['meta_title'] = self.__extract_meta_title(response)
                amazon_item['data']['meta_description'] = self.__extract_meta_description(response)
                amazon_item['data']['meta_keywords'] = self.__extract_meta_keywords(response)
            except Exception as e:
                self.logger.exception("{}: [ASIN:{}] Failed parsing page - {}".format(utils.class_fullname(e), self._asin, str(e)))
                amazon_item['data']['status'] = settings.RESOURCES_LISTING_ITEM_STATUS_PARSING_FAILED_UNKNOWN_ERROR
            else:
                amazon_item['data']['status'] = settings.RESOURCES_LISTING_ITEM_STATUS_GOOD
        return amazon_item


    # def __build_amazon_item_from_cache(self, response):
    #     a = AmazonItemModelManager.fetch_one(asin=self._asin)
    #     if not a:
    #         return None

    #     amazon_item = AmazonItem()
    #     amazon_item['_cached'] = True
    #     amazon_item['asin'] = a.asin
    #     amazon_item['parent_asin'] = a.parent_asin
    #     amazon_item['variation_asins'] = AmazonItemModelManager.fetch_its_variation_asins(parent_asin=a.parent_asin)
    #     amazon_item['url'] = amazonmws_utils.str_to_unicode(response.url)
    #     amazon_item['category'] = a.category
    #     amazon_item['title'] = a.title
    #     amazon_item['price'] = a.price
    #     amazon_item['original_price'] = a.original_price
    #     amazon_item['quantity'] = a.quantity
    #     amazon_item['features'] = a.features
    #     amazon_item['description'] = a.description
    #     amazon_item['specifications'] = a.specifications
    #     amazon_item['variation_specifics'] = a.variation_specifics
    #     amazon_item['review_count'] = a.review_count
    #     amazon_item['avg_rating'] = a.avg_rating
    #     amazon_item['is_fba'] = a.is_fba
    #     amazon_item['is_addon'] = a.is_addon
    #     amazon_item['is_pantry'] = a.is_pantry
    #     amazon_item['has_sizechart'] = a.has_sizechart
    #     amazon_item['merchant_id'] = a.merchant_id
    #     amazon_item['merchant_name'] = a.merchant_name
    #     amazon_item['brand_name'] = a.brand_name
    #     amazon_item['meta_title'] = a.meta_title
    #     amazon_item['meta_description'] = a.meta_description
    #     amazon_item['meta_keywords'] = a.meta_keywords
    #     amazon_item['status'] = a.status
    #     amazon_item['_redirected_asins'] = {}
    #     return amazon_item

    def __extract_asin_on_content(self, response):
        try:
            # get asin from Add To Cart button
            return response.css('form#addToCart input[type=hidden][name=ASIN]::attr(value)').extract()[0]
        except IndexError as e:
            self.logger.exception("{}: [ASIN:{}] index error on parsing asin: ASIN at Add To Cart button missing - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing asin at __extract_asin_on_content - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_category(self, response):
        try:
            return ' : '.join(map(str.strip, response.css('#wayfinding-breadcrumbs_feature_div > ul li:not(.a-breadcrumb-divider) > span > a::text').extract()))
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing category - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_title(self, response):
        try:
            summary_col = response.css('#centerCol')
            if len(summary_col) < 1:
                summary_col = response.css('#leftCol')
            if len(summary_col) < 1:
                raise Exception("No title element found")
            title = None
            title_element = summary_col.css('h1#title > span::text')
            if len(title_element) > 0:
                title = title_element[0].extract().strip()
                if title == "":
                    title = title_element[1].extract().strip()
                return title
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing title - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_features(self, response):
        try:
            feature_block = response.css('#feature-bullets')
            if len(feature_block) < 1:
                feature_block = response.css('#fbExpandableSectionContent')
            if len(feature_block) < 1:
                return None
            ret = ''
            features = feature_block.css('li:not(#replacementPartsFitmentBullet)')
            if len(features) > 0:
                ret = '<div id="feature-bullets" class="a-section a-spacing-medium a-spacing-top-small"><ul class="a-vertical a-spacing-none">'
                for each_feature in features:
                    ret = ret + utils.trim_emojis(each_feature.extract().strip())
                ret = ret + '</ul></div>'
            return utils.replace_html_anchors_to_spans(ret)
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing features - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_description_helper(self, response):
        try:
            description_block = response.css('#productDescription .productDescriptionWrapper')
            if len(description_block) < 1:
                description_block = response.css('#productDescription')
            if len(description_block) < 1:
                description_block = response.css('#descriptionAndDetails .productDescriptionWrapper')
            if len(description_block) < 1:
                description_block = response.css('#aplus .aplus-v2')
            if len(description_block) < 1:
                return None
            description = description_block[0].extract()
            disclaim_block = description_block.css('.disclaim')
            if len(disclaim_block) > 0:
                disclaim = description_block.css('.disclaim')[0].extract()
                description.replace(disclaim, '')
            return utils.replace_html_anchors_to_spans(description.strip())
        except Exception as e:
            raise e

    def __extract_description(self, response):
        try:
            m = re.search(r"var iframeContent = \"(.+)\";\n", response.text)
            if m:
                description_iframe_str = urllib.parse.unquote(m.group(1))
                from scrapy.http import HtmlResponse
                description_iframe_response = HtmlResponse(url="description_iframe_string", body=description_iframe_str)
                return self.__extract_description_helper(description_iframe_response)
            else:
                return self.__extract_description_helper(response)
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing description - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_specifications(self, response):
        try:
            prod_det_tables = response.css('#prodDetails table.prodDetTable')
            specs = []
            for prod_det_table in prod_det_tables:
                spec_entries = prod_det_table.css('tr')
                for spec_entry in spec_entries:
                    th_text_element = spec_entry.css('th::text')
                    td_text_element = spec_entry.css('td::text')
                    if len(th_text_element) > 0 and len(td_text_element) > 0:
                        key = th_text_element[0].extract().strip()
                        val = td_text_element[0].extract().strip()
                        specs.append({ key: val })
            if len(specs) > 0:
                return json.dumps(specs)
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing specifications - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_review_count(self, response):
        try:
            if len(response.css('#summaryStars a::text')) > 0:
                return utils.extract_int(response.css('#summaryStars a::text')[1].extract().replace(',', '').strip())
            elif len(response.css('#acrCustomerReviewText::text')) > 0:
                if len(response.css('#acrCustomerReviewText::text')) == 1:
                    return utils.extract_int(response.css('#acrCustomerReviewText::text')[0].extract().replace(',', '').replace('customer reviews', '').replace('customer review', '').strip())
                else:
                    return utils.extract_int(response.css('#acrCustomerReviewText::text')[1].extract().replace(',', '').replace('customer reviews', '').replace('customer review', '').strip())
            else:
                return 0
        except IndexError as e:
            self.logger.exception("{}: [ASIN:{}] index error on parsing review count - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return 0
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing review count - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return 0

    def __extract_avg_rating(self, response):
        try:
            if len(response.css('#avgRating a > span::text')) > 0:
                return float(response.css('#avgRating a > span::text')[0].extract().replace('out of 5 stars', '').strip())
            elif len(response.css('#acrPopover a > i > span::text')) > 0:
                return float(response.css('#acrPopover a > i > span::text')[0].extract().replace('out of 5 stars', '').strip())
            else:
                return 0.0
        except IndexError as e:
            self.logger.exception("{}: [ASIN:{}] index error on parsing average rating - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return 0.0
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing average rating - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return 0.0

    def __extract_is_addon(self, response):
        try:
            addon = response.css('#addOnItem_feature_div i.a-icon-addon')
            return True if len(addon) > 0 else False
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing addon - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return False

    def __extract_is_pantry(self, response):
        try:
            pantry = response.css('img#pantry-badge')
            return True if len(pantry) > 0 else False
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing pantry - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return False

    def __extract_has_sizechart(self, response):
        try:
            sizechart = response.css('a#size-chart-url')
            return True if len(sizechart) > 0 else False
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing size chart - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return False

    def __extract_is_fba(self, response):
        try:
            element = response.css('#merchant-info::text')
            if len(element) > 0 and 'sold by {}'.format(self._domain) in element[0].extract().strip().lower():
                if self.__double_check_prime(response):
                    return True
            element = response.css('#merchant-info a#SSOFpopoverLink::text')
            if len(element) > 0 and 'fulfilled by amazon' in element[0].extract().strip().lower():
                if self.__double_check_prime(response):
                    return True
            element = response.css('#merchant-info #pe-text-availability-merchant-info::text')
            if len(element) > 0 and 'sold by {}'.format(self._domain) in element[0].extract().strip().lower():
                if self.__double_check_prime(response):
                    return True
            return False
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing FBA - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return False

    def __double_check_prime(self, response):
        # some fba are not prime
        return response.text.find('bbop-check-box') > 0 or len(response.css('#pe-bb-signup-button')) > 0 or (len(response.css('#ourprice_shippingmessage span b::text')) > 0 and response.css('#ourprice_shippingmessage span b::text')[0].extract().strip().lower() == 'free shipping')

    def __extract_price(self, response):
        # 1. check deal price block first
        # 2. check sale price block second
        # 3. if no deal/sale price block exists, check our price block
        try:
            #####################################################
            # UNABLE TO MATCH DEAL PRICE AT THIS MOMENT
            #####################################################
            #
            # price_element = response.css('#priceblock_dealprice::text')
            # if len(price_element) < 1:
            #     price_element = response.css('#priceblock_saleprice::text')
            #     if len(price_element) < 1:
            #         price_element = response.css('#priceblock_ourprice::text')
            #         if len(price_element) < 1: # for dvd
            #             price_element = response.css('#buyNewSection span.a-color-price.offer-price::text')
            #
            #####################################################

            price_element = response.css('#priceblock_saleprice::text')
            if len(price_element) < 1:
                price_element = response.css('#priceblock_ourprice::text')
                if len(price_element) < 1: # for dvd
                    price_element = response.css('#buyNewSection span.a-color-price.offer-price::text')
            if len(price_element) < 1:
                self.logger.info("[ASIN:{}] No price element found".format(self._asin))
                return None
            else:
                price_string = price_element[0].extract().strip()
                return utils.money_to_float(price_string)
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing price - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_original_price(self, response, default_price):
        try:
            original_price_element = response.css('#price table tr td span.a-text-strike::text')
            if len(original_price_element) < 1:
                return default_price
            else:
                original_price_string = original_price_element[0].extract().strip()
                return utils.money_to_float(original_price_string)
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing market price - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return default_price

    def __extract_quantity(self, response):
        try:
            quantity = 0
            element = response.css('#availability:not(.a-hidden) span::text')
            if len(element) < 1:
                element = response.css('#availability:not(.a-hidden)::text')
            if len(element) < 1:
                element = response.css('#pantry-availability:not(.a-hidden) span::text')
            if len(element) < 1:
                return quantity # element not found

            element_text = element[0].extract().strip().lower()
            if 'out' in element_text:
                quantity = 0 # out of stock
            elif 'only' in element_text:
                if 'more on the way' in element_text:
                    quantity = 1000 # enough stock
                else:
                    quantity = utils.extract_int(element_text)
            elif 'in stock on' in element_text: # will be stock on someday... so currently out of stock...
                quantity = 0
            elif 'will be released on' in element_text: # will be released on someday... so currently out of stock...
                quantity = 0
            elif 'usually ships within' in element_text: # delay shipping... so currently out of stock...
                quantity = 0
            else:
                quantity = 1000 # enough stock
            return quantity
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing quantity - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return 0

    def __extract_parent_asin(self, response):
        ret = None
        try:
            m = re.search(r"\"parent_asin\":\"([A-Z0-9]{10})\"", response.text)
            if m:
                ret = m.group(1)
            return ret
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing parent asin - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_picture_urls(self, response):
        ret = []
        try:
            m = re.search(r"'colorImages': \{(.+)\},\n", response.text)
            if m:
                # work with json
                json_dump = "{%s}" % m.group(1).replace('\'', '"')
                image_data = json.loads(json_dump)
                for key in image_data:
                    images = image_data[key]
                    for image in images:
                        if "hiRes" in image and image["hiRes"] != None:
                            ret.append(image["hiRes"])
                        elif "large" in image and image["large"] != None:
                            ret.append(image["large"])
                    break
                return ret
            if len(ret) > 0:
                return ret
            else:
                original_image_url = response.css('#main-image-container > ul li.image.item img::attr(src)')
                # try primary image url
                converted_picture_url = re.sub(settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_PRIMARY, original_image_url)
                if not utils.validate_image_size(converted_picture_url):
                    # try secondary image url
                    converted_picture_url = re.sub(settings.AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM, settings.AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_SECONDARY, original_image_url)
                    if not utils.validate_image_size(converted_picture_url):
                        ret.append(original_image_url)
                if len(ret) < 1:
                    ret.append(converted_picture_url)
                return ret
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing item pictures - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return []

    def __extract_merchant_id(self, response):
        try:
            if len(response.css('#merchant-info::text')) > 0 and self._domain in response.css('#merchant-info::text')[0].extract().strip().lower():
                return None
            element = response.css('#merchant-info a:not(#SSOFpopoverLink)::attr(href)')
            if len(element) > 0:
                uri = element[0].extract().strip()
                return utils.extract_seller_id_from_uri(uri)
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing merchant id - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_merchant_name(self, response):
        try:
            if len(response.css('#merchant-info::text')) > 0 and self._domain in response.css('#merchant-info::text')[0].extract().strip().lower():
                return self._domain
            element = response.css('#merchant-info a:not(#SSOFpopoverLink)::text')
            if len(element) > 0:
                return element[0].extract().strip()
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing merchant name - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_brand_name(self, response):
        brand = None
        if len(response.css('#brand')) > 0:
            try:
                if len(response.css('#brand::text')) > 0:
                    brand = response.css('#brand::text')[0].extract().strip()
            except Exception:
                brand = None
            if brand is not None and brand != '':
                return brand
            try:
                if len(response.css('#brand::attr(href)')) > 0:
                    brand_url = response.css('#brand::attr(href)')[0].extract().strip()
                    if brand_url:
                        urlquerys = urllib.parse.parse_qs(urllib.parse.urlparse(brand_url).query)
                        if 'field-lbr_brands_browse-bin' in urlquerys:
                            brand = urlquerys['field-lbr_brands_browse-bin'][0]
            except Exception:
                brand = None
            if brand is not None and brand != '':
                return brand
        elif len(response.css('#bylineInfo')) > 0:
            try:
                if len(response.css('#bylineInfo::text')) > 0:
                    brand = response.css('#bylineInfo::text')[0].extract().strip()
            except Exception:
                brand = None
            if brand is not None and brand != '':
                return brand
            try:
                if len(response.css('#bylineInfo::attr(href)')) > 0:
                    brand_url = response.css('#bylineInfo::attr(href)')[0].extract().strip()
                    if brand_url:
                        urlquerys = urllib.parse.parse_qs(urllib.parse.urlparse(brand_url).query)
                        if 'field-lbr_brands_browse-bin' in urlquerys:
                            brand = urlquerys['field-lbr_brands_browse-bin'][0]
            except Exception:
                brand = None
            if brand is not None and brand != '':
                return brand
        return None

    def __extract_meta_title(self, response):
        try:
            if len(response.xpath("//meta[@name='title']/@content")) > 0:
                return response.xpath("//meta[@name='title']/@content")[0].extract()
            else:
                return None
        except IndexError as e:
            self.logger.exception("{}: [ASIN:{}] index error on parsing meta title - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing meta title - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_meta_description(self, response):
        try:
            if len(response.xpath("//meta[@name='description']/@content")) > 0:
                return response.xpath("//meta[@name='description']/@content")[0].extract()
            else:
                return None
        except IndexError as e:
            self.logger.exception("{}: [ASIN:{}] index error on parsing meta description - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing meta description - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_meta_keywords(self, response):
        try:
            if len(response.xpath("//meta[@name='keywords']/@content")) > 0:
                return response.xpath("//meta[@name='keywords']/@content")[0].extract()
            else:
                return None
        except IndexError as e:
            self.logger.exception("{}: [ASIN:{}] index error on parsing meta keywords - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing meta keywords - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return None

    def __extract_variation_asins(self, response):
        ret = []
        m = re.search(r"\"asin_variation_values\":(\{.+?(?=\}\})\}\})", response.text)
        if m:
            try:
                json_dump = m.group(1)
                variations_data = json.loads(json_dump)
                ret = list(variations_data.keys())
            except Exception:
                ret = []
        if len(ret) < 1:
            m = re.search(r"\"asinVariationValues\" : (\{.+?(?=\}\})\}\})", response.text)
            if m:
                try:
                    json_dump = m.group(1)
                    variations_data = json.loads(json_dump)
                    ret = list(variations_data.keys())
                except Exception:
                    ret = []
        if len(ret) < 1:
            self.logger.warning("[ASIN:{}] error on parsing variation asins - unable to parse either asin_variation_values or asinVariationValues".format(self._asin))
        return ret

    def __extract_variation_specifics(self, response):
        ret = {}
        # variation labels
        variation_labels = {}
        l = re.search(r"\"variationDisplayLabels\":(\{.+?(?=\})\})", response.text)
        if l:
            try:
                variation_labels = json.loads(l.group(1))
            except Exception:
                variation_labels = {}
        if not variation_labels:
            l = re.search(r"\"variationDisplayLabels\" : (\{.+?(?=\})\})", response.text)
            if l:
                try:
                    variation_labels = json.loads(l.group(1))
                except Exception:
                    variation_labels = {}
        if not variation_labels:
            self.logger.warning("[ASIN:{}] error on parsing variation specifics - unable to parse variationDisplayLabels".format(self._asin))
            return None
        # selected variations
        selected_variations = {}
        m = re.search(r"\"selected_variations\":(\{.+?(?=\})\})", response.text)
        if m:
            try:
                selected_variations = json.loads(m.group(1))
            except Exception:
                selected_variations = {}
        if not selected_variations:
            m = re.search(r"\"selected_variations\" : (\{.+?(?=\})\})", response.text)
            if m:
                try:
                    selected_variations = json.loads(m.group(1))
                except Exception:
                    selected_variations = {}
        if not selected_variations:
            self.logger.warning("[ASIN:{}] error on parsing variation specifics - unable to parse selected_variations".format(self._asin))
            return None
        for v_key, v_val in variation_labels.items():
            if v_key not in selected_variations:
                # selected variations must contains all variation options
                return None
            ret[v_val] = selected_variations[v_key]
        return json.dumps(ret)

    def __extract_redirected_asins(self, response):
        try:
            redirected_asins = {}
            redirect_urls = response.request.meta.get('redirect_urls', [])
            if len(redirect_urls) > 0:
                index = 0
                for r_url in redirect_urls:
                    r_asin = utils.extract_sku_from_url(r_url, self._domain)
                    if r_asin == self._asin:
                        continue
                    redirected_asins[index] = r_asin
                    index += 1
            return redirected_asins
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing redirected asins - {}".format(utils.class_fullname(e), self._asin, str(e)))
            return {}
