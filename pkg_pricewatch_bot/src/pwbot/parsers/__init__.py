""" pwbot.parsers
"""
import logging
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import IgnoreRequest
from pwbot.parsers.amazon_item_parser import AmazonItemParser
from pwbot.parsers.walmart_item_parser import WalmartComItemParser, WalmartCaItemParser
from pwbot.parsers.canadiantire_item_parser import CanadiantireCaItemParser

def parse_amazon_item(response, domain, job_id, crawl_variations, lat=None, lng=None):
    """ response: scrapy.http.response.html.HtmlResponse
    """
    parser = AmazonItemParser()
    try:
        return parser.parse_item(response, domain, job_id, crawl_variations, lat, lng)
    except IgnoreRequest:
        return None

def parse_walmart_com_item(response, domain, job_id, crawl_variations, lat, lng):
    parser = WalmartComItemParser()
    try:
        return parser.parse_item(response, domain, job_id, crawl_variations, lat, lng)
    except IgnoreRequest:
        return None

def parse_walmart_ca_item(response, domain, job_id, crawl_variations, lat, lng):
    parser = WalmartCaItemParser()
    try:
        return parser.parse_item(response, domain, job_id, crawl_variations, lat, lng)
    except IgnoreRequest:
        return None

def parse_canadiantire_ca_item(response, domain, job_id, crawl_variations, lat, lng):
    parser = CanadiantireCaItemParser()
    try:
        return parser.parse_item(response, domain, job_id, crawl_variations, lat, lng)
    except IgnoreRequest:
        return None


def resp_error_handler(failure):
    # log all failures
    logger = logging.getLogger('pwbot.parsers.resp_error_handler')

    # in case you want to do something special for some errors,
    # you may need the failure's type:

    if failure.check(HttpError):
        # these exceptions come from HttpError spider middleware
        # you can get the non-200 response
        response = failure.value.response
        logger.error('HttpError on {} - {} - {}'.format(response.url, failure.getErrorMessage(), response.text))

    elif failure.check(DNSLookupError):
        # this is the original request
        request = failure.request
        logger.error('DNSLookupError on {} - {}'.format(request.url, failure.getErrorMessage()))

    elif failure.check(TimeoutError, TCPTimedOutError):
        request = failure.request
        logger.error('TimeoutError on {} - {}'.format(request.url, failure.getErrorMessage()))
