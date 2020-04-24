import unittest
from scrapy.http import Request
from amzbot.tests import utils

from botschedular import BotSchedular

# testing purpose
if __name__ == "__main__":
    s = BotSchedular()
    s.addversion()

class TestSchedular(unittest.TestCase):

    def setUp(self):
        self.schedular = BotSchedular()

    def test_addversion(self):
        self.assertEqual(self.schedular.addversion(), 5)
