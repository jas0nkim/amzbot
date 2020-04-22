from scrapy.exceptions import IgnoreRequest

from amzbot.parsers.amazon_item_parser import AmazonItemParser

""" response: scrapy.http.response.html.HtmlResponse
"""
def parse_amazon_item(response):
    parser = AmazonItemParser()
    try:
        return parser.parse_item(response)
    except IgnoreRequest:
        return None


