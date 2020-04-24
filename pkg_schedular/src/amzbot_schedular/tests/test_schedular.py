import unittest
from scrapy.http import Request

from amzbot_schedular import Schedular

class TestSchedular(unittest.TestCase):

    def setUp(self):
        self.schedular = Schedular()

    def test_addversion(self):
        self.assertEqual(self.schedular.addversion(), 5)
