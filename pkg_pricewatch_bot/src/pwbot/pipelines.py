# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# import logging
# from scrapy.exceptions import DropItem

# from pwbot import utils

# class DbPipeline(object):

#     def __init__(self):
#         self.logger = logging.getLogger('pwbot.pipelines.DbPipeline')

#     def process_item(self, item, spider):
#         try:
#             item.save()
#             return item
#         except Exception as e:
#             self.logger.exception("{}: Error on saving item to db - {}".format(utils.class_fullname(e), str(e)))
#             raise DropItem