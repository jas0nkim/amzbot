""" utils.py
"""
import re
import urllib
import logging
import io
import tldextract
from PIL import Image
from pwbot import settings


def is_valid_amazon_item_url(url, domain='amazon.com'):
    link_pattern = settings.AMAZON_COM_ITEM_LINK_PATTERN
    if domain == 'amazon.ca':
        link_pattern = settings.AMAZON_CA_ITEM_LINK_PATTERN
    return re.match(link_pattern, url)

def extract_asin_from_url(url, domain='amazon.com'):
    match = is_valid_amazon_item_url(url, domain)
    if match:
        return match.group(3)
    else:
        return None

def is_valid_walmart_com_item_url(url):
    return re.match(settings.WALMART_COM_ITEM_LINK_PATTERN, url)

def is_valid_walmart_ca_item_url(url):
    return re.match(settings.WALMART_CA_ITEM_LINK_PATTERN, url)

def extract_sku_from_url(url, domain):
    if domain in ['amazon.com', 'amazon.ca',]:
        return extract_asin_from_url(url, domain)
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
    else:
        return None

def money_to_float(string):
    # trim everything except number and dot(.)
    return float(re.sub(r'[^\d.]+', '', string))

def extract_int(string):
    # trim everything except number
    return int(re.sub(r'[^\d]+', '', string))

def trim_emojis(string):
    if isinstance(string, str):
        return string.encode('ascii', errors='ignore').decode('utf-8', errors='ignore')
    return string

def replace_html_anchors_to_spans(html):
    # /(<a[^>]*>)([^<]+)(</a>)/
    return re.sub(r'(<a[^>]*>)([^<]+)(</a>)', lambda m: u'<span class="link-replacement">' + m.group(2) + u'</span>', html)

def extract_seller_id_from_uri(uri):
    match = re.match(r'^.+?(?=seller=)([^&]+).*$', uri)
    if match:
        return match.group(1).replace('seller=', '').strip()
    else:
        return None

def get_response_from_url(url):
    """ return http.client.HTTPResponse object
    """
    ret = None
    try:
        response = urllib.request.urlopen(url)
        if response.status != 200:
            raise Exception("HTTP Status is not OK - Status {}".format(response.status))
        ret = response
    except urllib.error.HTTPError as e:
        raise Exception("HTTPError - {}".format(str(e)))
    except urllib.error.URLError as e:
        raise Exception("URLError - {}".format(str(e)))
    return ret

def validate_image_size(url):
    try:
        response = get_response_from_url(url)
        img = Image.open(io.StringIO(response.read()))
    except OSError as e:
        raise Exception("OSError - {}".format(str(e)))
    except ValueError as e:
        raise Exception("ValueError - {}".format(str(e)))
    (width, height) = img.size
    if width < 500 and height < 500:
        raise Exception("Image width and height are less then 500px")
    return True

def true_or_false(string):
    return string.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

def class_fullname(o):
    """ https://stackoverflow.com/a/2020083
    """
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__

def extract_domain_from_url(url):
    # remove tldextract's annoying 'computed TLD diff' log...
    change_single_log_level("tldextract", logging.ERROR)
    return tldextract.extract(url).registered_domain

def change_single_log_level(log_name, level):
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
