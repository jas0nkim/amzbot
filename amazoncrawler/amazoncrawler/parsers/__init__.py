from scrapy.exceptions import IgnoreRequest

from .amazon_item_parser import AmazonItemParser


def parse_amazon_item(response):
    parser = AmazonItemParser()
    try:
        return parser.parse_item(response)
    except IgnoreRequest:
        return None


