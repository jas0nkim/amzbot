# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from amzbot import utils
utils.setup_djg()

from scrapy import Field
from scrapy_djangoitem import DjangoItem
from django.forms.models import model_to_dict
from djg_resources.models import AmazonParentListing, AmazonListing


class AmzbotDjangoItem(DjangoItem):
    def save(self, commit=True):
        """ override DjangoItem.save in order to handle 'update'
        """
        if commit:
            model_class = type(self.instance)
            pk = self.instance.pk
            if pk is None:
                raise Exception("Primary Key not found. Unable to save to database.")
            update_instance = True
            destination = None
            try:
                destination = model_class.objects.get(pk=pk)
            except model_class.DoesNotExist:
                update_instance = False
            if update_instance:
                source_dict = model_to_dict(self.instance)
                for (key, value) in source_dict.items():
                    if value is not None:
                        setattr(destination, key, value)
                # update self._instance
                self._instance = destination
            self.instance.save()
        return self.instance


class ParentListingItem(AmzbotDjangoItem):
    django_model = AmazonParentListing

class ListingItem(AmzbotDjangoItem):
    django_model = AmazonListing
    _redirected_asins = Field()
    _cached = Field()
