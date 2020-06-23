# -*- coding: utf-8 -*-

# Scrapy settings for pwbot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import configparser
import graypy


APP_DATA_DIRPATH = '/usr/local/etc/pricewatch/'
APP_DIST_DIRPATH = APP_DATA_DIRPATH + 'dist/'
APP_CONFIG_FILEPATH = APP_DATA_DIRPATH + 'pricewatch.ini'

# django model statuses
RESOURCES_LISTING_ITEM_STATUS_GOOD = 1000
RESOURCES_LISTING_ITEM_STATUS_INACTIVE = 1001
RESOURCES_LISTING_ITEM_STATUS_INVALID_SKU = 1002
RESOURCES_LISTING_ITEM_STATUS_SKU_NOT_IN_VARIATION = 1003
RESOURCES_LISTING_ITEM_STATUS_NO_PRICE_GIVEN = 1004
RESOURCES_LISTING_ITEM_STATUS_OUT_OF_STOCK = 1005
RESOURCES_LISTING_ITEM_STATUS_PARSING_FAILED_UNKNOWN_ERROR = 1006


BOT_NAME = 'pwbot'

SPIDER_MODULES = ['pwbot.spiders']
NEWSPIDER_MODULE = 'pwbot.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pwbot (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'pwbot.middlewares.pwbotSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'pwbot.middlewares.pwbotDownloaderMiddleware': 543,
   'pwbot.middlewares.RequestHeaderCostomizerMiddleware': 400,
   'scrapy_crawlera.CrawleraMiddleware': 610
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'pwbot.pipelines.DbPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# scrapy logging
# https://docs.scrapy.org/en/latest/topics/logging.html#topics-logging-settings

# import time
# LOG_FILE = '/var/log/python/pwbot-{}.log'.format(time.time())
LOG_LEVEL = 'DEBUG'

DOWNLOAD_TIMEOUT = 60

## crawlera related
CRAWLERA_HOST = 'proxy.crawlera.com'
CRAWLERA_PORT = '8010'
CRAWLERA_APIKEY = '191582bbbb4144519a78f00776896436'
CRAWLERA_ENABLED = True
CRAWLERA_DOWNLOAD_TIMEOUT = 60

## config, custom logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

config = configparser.ConfigParser()
config.read(APP_CONFIG_FILEPATH)

graylog_handler = graypy.GELFUDPHandler(config['Graylog']['host'], int(config['Graylog']['port']))
graylog_handler.setLevel(logging.ERROR) # set logging.ERROR later
graylog_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(graylog_handler)


## amazon.com related
AMAZON_COM_ITEM_LINK_PATTERN = r'^(https?://www.amazon.com)?/([^/]+/[^/]+|dp)/([A-Z0-9]{10})(/.*$)?'

## amazon.ca related
AMAZON_CA_ITEM_LINK_PATTERN = r'^(https?://www.amazon.ca)?/([^/]+/[^/]+|dp)/([A-Z0-9]{10})(/.*$)?'

AMAZON_ITEM_LINK_FORMAT = 'https://www.{}/dp/{}{}'
AMAZON_ITEM_VARIATION_LINK_POSTFIX = '/?th=1&psc=1'
AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM = r'\._([^_]+)_\.'
AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_PRIMARY = '._SL1500_.'
AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_SECONDARY = '._SX522_.'


## walmart.com related
WALMART_COM_ITEM_LINK_PATTERN = r'^(https?://www.walmart.com)?/([^/]+/[^/]+|ip)/([A-Z0-9]{8,15})(/.*$)?'
WALMART_COM_ITEM_LINK_FORMAT = 'https://www.{}/ip/{}{}'
WALMART_COM_ITEM_VARIATION_LINK_POSTFIX = '?selected=true'

## walmart.ca related
WALMART_CA_ITEM_LINK_PATTERN = r'^(https?://www.walmart.ca)?/(en|fr)/([^/]+/[^/]+|ip)/([A-Z0-9]{8,15})(/.*$)?'
WALMART_CA_ITEM_LINK_FORMAT = 'https://www.{}/en/ip/{}'
WALMART_CA_API_ITEM_PRICE_LINK_FORMAT = 'https://www.walmart.ca/api/product-page/price-offer#{}'
WALMART_CA_API_ITEM_FIND_IN_STORE_LINK_FORMAT = 'https://www.walmart.ca/api/product-page/find-in-store?latitude={lat}&longitude={lng}&lang=en&upc={upc}#{pid}'

## canadiantire.ca related
CANADIANTIRE_CA_ITEM_LINK_PATTERN = r'^(https?://www.canadiantire.ca)?/(en|fr)/([^/]+/[^/]+|pdp)/([\w-]*)([0-9]{7,12})p*.html[.*$]?'
CANADIANTIRE_CA_ITEM_LINK_FORMAT = 'https://www.{}/en/pdp/{}.html'
CANADIANTIRE_CA_API_STORES_LINK_FORMAT = 'https://api-triangle.canadiantire.ca/dss/services/v4/stores?lang=en&radius=1000&maxCount=12&storeType=store&lat={lat}&lng={lng}#{pid}'
# i.e. https://api-triangle.canadiantire.ca/dss/services/v4/stores?lang=en&radius=1000&maxCount=12&storeType=store&lat=43.769037&lng=-79.371951
CANADIANTIRE_CA_API_ITEM_PRICE_LINK_FORMAT = 'https://www.canadiantire.ca/ESB/PriceAvailability?SKU={sku}&Store={store}&Banner=CTR&Language=E#{pid}'
# i.e. https://www.canadiantire.ca/ESB/PriceAvailability?SKU=0782763&Store=0192%2C0126%2C0459%2C0485%2C0030%2C0019%2C0087%2C0264%2C0321%2C0150%2C0273%2C0214&Banner=CTR&Language=E
