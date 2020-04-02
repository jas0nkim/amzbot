# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListingItem(scrapy.Item):
    asin = scrapy.Field()
    parent_asin = scrapy.Field()
    variation_asins = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    market_price = scrapy.Field()
    quantity = scrapy.Field()
    features = scrapy.Field()
    description = scrapy.Field()
    specifications = scrapy.Field()
    variation_specifics = scrapy.Field()
    review_count = scrapy.Field()
    avg_rating = scrapy.Field()
    is_fba = scrapy.Field()
    is_addon = scrapy.Field()
    is_pantry = scrapy.Field()
    has_sizechart = scrapy.Field()
    merchant_id = scrapy.Field()
    merchant_name = scrapy.Field()
    brand_name = scrapy.Field()
    meta_title = scrapy.Field()
    meta_description = scrapy.Field()
    meta_keywords = scrapy.Field()
    status = scrapy.Field()
    _redirected_asins = scrapy.Field()
    _cached = scrapy.Field()


class ListingPictureItem(scrapy.Item):
    asin = scrapy.Field()
    picture_urls = scrapy.Field()
