import os, time

## django integration

os.environ['DJANGO_SETTINGS_MODULE'] = 'djg.settings'
import django
django.setup()

## django integration end

# -*- coding: utf-8 -*-

# Scrapy settings for amzbot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'amzbot'

SPIDER_MODULES = ['amzbot.spiders']
NEWSPIDER_MODULE = 'amzbot.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amzbot (+http://www.yourdomain.com)'

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
#    'amzbot.middlewares.AmzbotSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'amzbot.middlewares.AmzbotDownloaderMiddleware': 543,
   'amzbot.middlewares.RequestHeaderCostomizerMiddleware': 400,
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
   'amzbot.pipelines.DbPipeline': 300,
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

LOG_FILE = '/var/log/python/amzbot-{}.log'.format(time.time())
LOG_LEVEL = 'DEBUG'

# crawlera related
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '191582bbbb4144519a78f00776896436'

## amazon.com related
AMAZON_COM_ITEM_LINK_PATTERN = r'^(https?://www.amazon.com)?/([^/]+/[^/]+|dp)/([A-Z0-9]{10})(/.*$)?'

## amazon.ca related
AMAZON_CA_ITEM_LINK_PATTERN = r'^(https?://www.amazon.ca)?/([^/]+/[^/]+|dp)/([A-Z0-9]{10})(/.*$)?'

AMAZON_ITEM_LINK_FORMAT = 'https://www.{}/dp/{}{}'
AMAZON_ITEM_VARIATION_LINK_POSTFIX = '/?th=1&psc=1'
AMAZON_ITEM_IMAGE_CONVERT_PATTERN_FROM = r'\._([^_]+)_\.'
AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_PRIMARY = '._SL1500_.'
AMAZON_ITEM_IMAGE_CONVERT_STRING_TO_SECONDARY = '._SX522_.'
