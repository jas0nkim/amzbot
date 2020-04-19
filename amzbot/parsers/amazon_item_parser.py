import re, json, urllib, uuid, logging

from scrapy import Request
from scrapy.exceptions import IgnoreRequest

# from amazonmws import settings as amazonmws_settings, utils as amazonmws_utils
# from amazonmws.loggers import GrayLogger as logger, StaticFieldFilter, get_logger_name
# from amazonmws.model_managers import *
# from amazonmws.errors import record_amazon_scrape_error

# from amazon_apparel_parser import AmazonApparelParser

from amzbot import utils, settings
from amzbot.items import ParentListingItem, ListingItem

class AmazonItemParser(object):

    __asin = None

    def __init__(self):
        self.logger = logging.getLogger('amzbot.parsers.amazon_item_parser.AmazonItemParser')

    """ response scrapy.http.response.html.HtmlResponse
    """
    def parse_item(self, response):
        asin = utils.extract_asin_from_url(response.url, response.meta['domain'])
        if not asin:
            self.logger.exception("[ASIN:null] Request Ignored - No ASIN")
            raise IgnoreRequest

        self.__asin = asin

        # __stored_variation_asins = []
        # if AmazonItemModelManager.is_given_asin_parent(asin=self.__asin):
        #     __stored_variation_asins = AmazonItemModelManager.fetch_its_variation_asins(parent_asin=self.__asin)
        #     for sv_asin in __stored_variation_asins:
        #         if sv_asin != self.__asin: # ignore any amazon items which have the same parent_asin and asin - which makes endless scrapy requests
        #             yield Request(amazonmws_settings.AMAZON_ITEM_VARIATION_LINK_FORMAT % sv_asin,
        #                     callback=self.parse_item,
        #                     headers={ 'Referer': 'https://www.{}/'.format(response.meta['domain']), },
        #                     meta={
        #                         'dont_parse_pictures': response.meta['dont_parse_pictures'] if 'dont_parse_pictures' in response.meta else False,
        #                         'dont_parse_variations': True,
        #                     })

        # if 'cached_amazon_item' in response.flags:
        #     self.logger.info("[ASIN:{}] cached amazon item - generating by database".format(asin))
        #     yield self.__build_amazon_item_from_cache(response)
        # else:
        if response.status != 200:
            # broken link or inactive amazon item
            listing_item = ListingItem()
            listing_item['_cached'] = False
            listing_item['asin'] = self.__asin
            listing_item['domain'] = response.meta['domain']
            listing_item['status'] = False
            if response.status == 404:
                # RemovedVariationHandleMiddleware.__handle_removed_variations related
                listing_item['parent_asin'] = None
                # self.logger.error('[ASIN:null] Request Ignored - No ASIN')
            return listing_item
        else:
            return self.__parse_item_helper(response)

    def parse_parent_listing_item(self, response, parent_asin, asins):
        parent_listing_item = ParentListingItem()
        parent_listing_item['parent_asin'] = parent_asin
        parent_listing_item['asins'] = asins
        parent_listing_item['review_count'] = self.__extract_review_count(response)
        parent_listing_item['avg_rating'] = self.__extract_avg_rating(response)
        parent_listing_item['domain'] = response.meta['domain']
        return parent_listing_item

    def __parse_item_helper(self, response):
        __parent_asin = self.__extract_parent_asin(response)
        __variation_asins = self.__extract_variation_asins(response)

        if response.meta['parse_parent_listing']:
            yield self.parse_parent_listing_item(response, parent_asin=__parent_asin, asins=__variation_asins)

        # check variations first
        """ TODO: __stored_variation_asins = amazon_parent_listings.asins in db
        """
        __stored_variation_asins = []
        if response.meta['parse_variations']:
            if len(__variation_asins) > 0:
                for v_asin in __variation_asins:
                    if v_asin not in __stored_variation_asins:
                        """ TODO: change settings.AMAZON_ITEM_LINK_FORMAT.format(response.meta['domain'], v_asin, settings.AMAZON_ITEM_VARIATION_LINK_POSTFIX to real amazon url (db query) : avoid ban
                        """
                        yield Request(settings.AMAZON_ITEM_LINK_FORMAT.format(response.meta['domain'], v_asin, settings.AMAZON_ITEM_VARIATION_LINK_POSTFIX),
                                callback=self.parse_item,
                                headers={ 'Referer': 'https://www.{}/'.format(response.meta['domain']), },
                                meta={
                                    'parse_pictures': response.meta['parse_pictures'],
                                    'parse_variations': False,
                                    'parse_parent_listing': False,
                                    'domain': response.meta['domain'],
                                })
                # self.logger.info("[ASIN:{}] Request Ignored - initial asin ignored".format(self.__asin))
                # raise IgnoreRequest
        else:
            listing_item = ListingItem()
            listing_item['_cached'] = False
            listing_item['asin'] = self.__asin
            listing_item['domain'] = response.meta['domain']

            _asin_on_content = self.__extract_asin_on_content(response)
            if _asin_on_content != self.__asin:
                # inactive amazon item
                listing_item['status'] = False
                yield listing_item
            elif self.__asin and __parent_asin and self.__asin != __parent_asin and len(__variation_asins) > 0 and self.__asin not in __variation_asins:
                # a variation, but removed - inactive this variation
                listing_item['status'] = False
                yield listing_item
            else:
                try:
                    listing_item['parent_asin'] = __parent_asin
                    listing_item['picture_urls'] = self.__extract_picture_urls(response) if response.meta['parse_pictures'] else []
                    listing_item['url'] = response.url
                    listing_item['category'] = self.__extract_category(response)
                    listing_item['title'] = self.__extract_title(response)
                    listing_item['price'] = self.__extract_price(response)
                    listing_item['original_price'] = self.__extract_original_price(response, default_price=listing_item['price'])
                    listing_item['quantity'] = self.__extract_quantity(response)
                    listing_item['features'] = self.__extract_features(response)
                    listing_item['description'] = self.__extract_description(response)
                    listing_item['specifications'] = self.__extract_specifications(response)
                    listing_item['variation_specifics'] = self.__extract_variation_specifics(response)
                    listing_item['is_fba'] = self.__extract_is_fba(response)
                    listing_item['is_addon'] = self.__extract_is_addon(response)
                    listing_item['is_pantry'] = self.__extract_is_pantry(response)
                    listing_item['has_sizechart'] = self.__extract_has_sizechart(response)
                    listing_item['merchant_id'] = self.__extract_merchant_id(response)
                    listing_item['merchant_name'] = self.__extract_merchant_name(response)
                    listing_item['brand_name'] = self.__extract_brand_name(response)
                    listing_item['meta_title'] = self.__extract_meta_title(response)
                    listing_item['meta_description'] = self.__extract_meta_description(response)
                    listing_item['meta_keywords'] = self.__extract_meta_keywords(response)
                    listing_item['status'] = True
                    listing_item['_redirected_asins'] = self.__extract_redirected_asins(response)
                except Exception as e:
                    listing_item['status'] = False
                    error_id = uuid.uuid4()
                    self.logger.exception("{}: [ASIN:{}] Failed to parse item <{}> - {}".format(utils.class_fullname(e), self.__asin, error_id, str(e)))
                yield listing_item

                # if listing_item.get('has_sizechart', False) and not AmazonItemApparelModelManager.fetch_one(parent_asin=__parent_asin):
                #     amazon_apparel_parser = AmazonApparelParser()
                #     yield Request(amazonmws_settings.AMAZON_ITEM_APPAREL_SIZE_CHART_LINK_FORMAT % __parent_asin,
                #             callback=amazon_apparel_parser.parse_apparel_size_chart,
                #             meta={'asin': __parent_asin},
                #             dont_filter=True) # we have own filtering function: _filter_asins()

    # def __build_amazon_item_from_cache(self, response):
    #     a = AmazonItemModelManager.fetch_one(asin=self.__asin)
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
            self.logger.exception("{}: [ASIN:{}] index error on parsing asin: ASIN at Add To Cart button missing - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing asin at __extract_asin_on_content - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return None

    def __extract_category(self, response):
        try:
            return ' : '.join(map(str.strip, response.css('#wayfinding-breadcrumbs_feature_div > ul li:not(.a-breadcrumb-divider) > span > a::text').extract()))
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing category - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] error on parsing title - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] error on parsing features - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] error on parsing description - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] error on parsing specifications - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] index error on parsing review count - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return 0
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing review count - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] index error on parsing average rating - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return 0.0
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing average rating - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return 0.0

    def __extract_is_addon(self, response):
        try:
            addon = response.css('#addOnItem_feature_div i.a-icon-addon')
            return True if len(addon) > 0 else False
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing addon - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return False

    def __extract_is_pantry(self, response):
        try:
            pantry = response.css('img#pantry-badge')
            return True if len(pantry) > 0 else False
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing pantry - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return False

    def __extract_has_sizechart(self, response):
        try:
            sizechart = response.css('a#size-chart-url')
            return True if len(sizechart) > 0 else False
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing size chart - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return False

    def __extract_is_fba(self, response):
        try:
            element = response.css('#merchant-info::text')
            if len(element) > 0 and 'sold by {}'.format(response.meta['domain']) in element[0].extract().strip().lower():
                if self.__double_check_prime(response):
                    return True
            element = response.css('#merchant-info a#SSOFpopoverLink::text')
            if len(element) > 0 and 'fulfilled by amazon' in element[0].extract().strip().lower():
                if self.__double_check_prime(response):
                    return True
            element = response.css('#merchant-info #pe-text-availability-merchant-info::text')
            if len(element) > 0 and 'sold by {}'.format(response.meta['domain']) in element[0].extract().strip().lower():
                if self.__double_check_prime(response):
                    return True
            return False
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing FBA - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
                self.logger.info("[ASIN:{}] No price element found".format(self.__asin))
                return 0.00
            else:
                price_string = price_element[0].extract().strip()
                return utils.money_to_float(price_string)
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing price - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return 0.00

    def __extract_original_price(self, response, default_price):
        try:
            original_price_element = response.css('#price table tr td span.a-text-strike::text')
            if len(original_price_element) < 1:
                return default_price
            else:
                original_price_string = original_price_element[0].extract().strip()
                return utils.money_to_float(original_price_string)
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing market price - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] error on parsing quantity - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return 0

    def __extract_parent_asin(self, response):
        ret = None
        try:
            m = re.search(r"\"parent_asin\":\"([A-Z0-9]{10})\"", response.text)
            if m:
                ret = m.group(1)
            return ret
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing parent asin - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] error on parsing item pictures - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return []

    def __extract_merchant_id(self, response):
        try:
            if len(response.css('#merchant-info::text')) > 0 and response.meta['domain'] in response.css('#merchant-info::text')[0].extract().strip().lower():
                return None
            element = response.css('#merchant-info a:not(#SSOFpopoverLink)::attr(href)')
            if len(element) > 0:
                uri = element[0].extract().strip()
                return utils.extract_seller_id_from_uri(uri)
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing merchant id - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return None

    def __extract_merchant_name(self, response):
        try:
            if len(response.css('#merchant-info::text')) > 0 and response.meta['domain'] in response.css('#merchant-info::text')[0].extract().strip().lower():
                return response.meta['domain']
            element = response.css('#merchant-info a:not(#SSOFpopoverLink)::text')
            if len(element) > 0:
                return element[0].extract().strip()
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing merchant name - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.exception("{}: [ASIN:{}] index error on parsing meta title - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing meta title - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return None

    def __extract_meta_description(self, response):
        try:
            if len(response.xpath("//meta[@name='description']/@content")) > 0:
                return response.xpath("//meta[@name='description']/@content")[0].extract()
            else:
                return None
        except IndexError as e:
            self.logger.exception("{}: [ASIN:{}] index error on parsing meta description - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing meta description - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return None

    def __extract_meta_keywords(self, response):
        try:
            if len(response.xpath("//meta[@name='keywords']/@content")) > 0:
                return response.xpath("//meta[@name='keywords']/@content")[0].extract()
            else:
                return None
        except IndexError as e:
            self.logger.exception("{}: [ASIN:{}] index error on parsing meta keywords - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return None
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing meta keywords - {}".format(utils.class_fullname(e), self.__asin, str(e)))
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
            self.logger.warning("[ASIN:{}] error on parsing variation asins - unable to parse either asin_variation_values or asinVariationValues".format(self.__asin))
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
            self.logger.warning("[ASIN:{}] error on parsing variation specifics - unable to parse variationDisplayLabels".format(self.__asin))
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
            self.logger.warning("[ASIN:{}] error on parsing variation specifics - unable to parse selected_variations".format(self.__asin))
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
                    r_asin = utils.extract_asin_from_url(r_url, response.meta['domain'])
                    if r_asin == self.__asin:
                        continue
                    redirected_asins[index] = r_asin
                    index += 1
            return redirected_asins
        except Exception as e:
            self.logger.exception("{}: [ASIN:{}] error on parsing redirected asins - {}".format(utils.class_fullname(e), self.__asin, str(e)))
            return {}
