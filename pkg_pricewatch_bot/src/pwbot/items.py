# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ListingItem(Item):
    url = Field()
    domain = Field()
    http_status = Field()
    data = Field()


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


