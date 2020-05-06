# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AmazonItem(Item):
    """ amazon(.com, .ca) item
    """
    domain = Field()
    asin = Field()
    parent_asin = Field()
    variation_asins = Field()
    picture_urls = Field()
    description = Field()
    url = Field()
    category = Field()
    title = Field()
    price = Field()
    original_price = Field()
    quantity = Field()
    features = Field()
    specifications = Field()
    variation_specifics = Field()
    review_count = Field()
    avg_rating = Field()
    is_fba = Field()
    is_addon = Field()
    is_pantry = Field()
    has_sizechart = Field()
    international_shipping = Field()
    merchant_id = Field()
    merchant_name = Field()
    brand_name = Field()
    meta_title = Field()
    meta_description = Field()
    meta_keywords = Field()
    http_status = Field()
    status = Field()


# class PwbotDjangoItem(DjangoItem):
#     def save(self, commit=True):
#         """ override DjangoItem.save in order to handle 'update'
#         """
#         if commit:
#             model_class = type(self.instance)
#             pk = self.instance.pk
#             if pk is None:
#                 raise Exception("Primary Key not found. Unable to save to database.")
#             update_instance = True
#             destination = None
#             try:
#                 destination = model_class.objects.get(pk=pk)
#             except model_class.DoesNotExist:
#                 update_instance = False
#             if update_instance:
#                 source_dict = model_to_dict(self.instance)
#                 for (key, value) in source_dict.items():
#                     if value is not None:
#                         setattr(destination, key, value)
#                 # update self._instance
#                 self._instance = destination
#             self.instance.save()
#         return self.instance


