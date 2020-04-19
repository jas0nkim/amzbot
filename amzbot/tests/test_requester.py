import unittest
from scrapy.http import Request
from amzbot.tests import utils


class TestRequester(unittest.TestCase):
    def setUp(self):
        self.testlist = utils.get_testlist(self.__class__.__name__)

    def test_amazon_url(self):
        pass