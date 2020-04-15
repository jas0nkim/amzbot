# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from . import utils
utils.setup_djg()

from scrapy import Field
from scrapy_djangoitem import DjangoItem
from djg_resources.models import AmazonParentListing, AmazonListing


class ParentListingItem(DjangoItem):
    django_model = AmazonParentListing

class ListingItem(DjangoItem):
    django_model = AmazonListing
    _redirected_asins = Field()
    _cached = Field()
