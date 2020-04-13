# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from . import utils
utils.setup_djg()

import scrapy
from scrapy_djangoitem import DjangoItem
from djg_resources.models import AmazonListing, AmazonListingPicture


class ListingItem(DjangoItem):
    django_model = AmazonListing
    _redirected_asins = scrapy.Field()
    _cached = scrapy.Field()

class ListingPictureItem(DjangoItem):
    django_model = AmazonListingPicture
