""" utils.py
"""
import re
import urllib.parse
from pwweb import settings


def is_valid_amazon_item_url(url, domain='amazon.com'):
    link_pattern = settings.AMAZON_COM_ITEM_LINK_PATTERN
    if domain == 'amazon.ca':
        link_pattern = settings.AMAZON_CA_ITEM_LINK_PATTERN
    return re.match(link_pattern, url)

def is_valid_walmart_com_item_url(url):
    return re.match(settings.WALMART_COM_ITEM_LINK_PATTERN, url)

def is_valid_walmart_ca_item_url(url):
    return re.match(settings.WALMART_CA_ITEM_LINK_PATTERN, url)

def is_valid_canadiantire_ca_item_url(url):
    return re.match(settings.CANADIANTIRE_CA_ITEM_LINK_PATTERN, url)

def extract_sku_from_url(url, domain):
    if domain in ['amazon.com', 'amazon.ca',]:
        match = is_valid_amazon_item_url(url, domain)
        if match:
            return match.group(3)
        else:
            return None
    elif domain in ['walmart.com',]:
        match = is_valid_walmart_com_item_url(url)
        if match:
            return match.group(3)
        else:
            return None
    elif domain in ['walmart.ca',]:
        match = is_valid_walmart_ca_item_url(url)
        if match:
            return match.group(4)
        else:
            return None
    elif domain in ['canadiantire.ca',]:
        match = is_valid_canadiantire_ca_item_url(url)
        if match:
            return match.group(5)
        else:
            return None
    else:
        return None

def extract_upc_from_walmart_ca_url(url):
    upc_list = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get('upc', [])
    return upc_list[0] if len(upc_list) > 0 else None