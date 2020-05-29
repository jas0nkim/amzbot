BOT_PROJECT = 'pricewatch_bot'
BOT_VERISON = '0.0.1'

APP_DATA_DIRPATH = '/usr/local/etc/pricewatch/'
APP_DIST_DIRPATH = APP_DATA_DIRPATH + 'dist/'
APP_CONFIG_FILEPATH = APP_DATA_DIRPATH + 'pricewatch.ini'

# django model statuses
SCHEDULES_JOB_STATUS_CANCELED = 0
SCHEDULES_JOB_STATUS_PENDING = 1
SCHEDULES_JOB_STATUS_RUNNING = 2
SCHEDULES_JOB_STATUS_FINISHED = 3

SCHEDULES_VERSION_STATUS_DELETED = 0
SCHEDULES_VERSION_STATUS_ADDED = 1

RESOURCES_LISTING_ITEM_STATUS_GOOD = 1000
RESOURCES_LISTING_ITEM_STATUS_INACTIVE = 1001
RESOURCES_LISTING_ITEM_STATUS_INVALID_SKU = 1002
RESOURCES_LISTING_ITEM_STATUS_SKU_NOT_IN_VARIATION = 1003
RESOURCES_LISTING_ITEM_STATUS_NO_PRICE_GIVEN = 1004
RESOURCES_LISTING_ITEM_STATUS_OUT_OF_STOCK = 1005
RESOURCES_LISTING_ITEM_STATUS_PARSING_FAILED_UNKNOWN_ERROR = 1006

RESOURCES_LISTING_ITEM_STATUS_STR_SET = {
    RESOURCES_LISTING_ITEM_STATUS_GOOD: 'Good',
    RESOURCES_LISTING_ITEM_STATUS_INACTIVE: 'Inactive',
    RESOURCES_LISTING_ITEM_STATUS_INVALID_SKU: 'Invalid SKU',
    RESOURCES_LISTING_ITEM_STATUS_SKU_NOT_IN_VARIATION: 'SKU not in variation',
    RESOURCES_LISTING_ITEM_STATUS_NO_PRICE_GIVEN: 'No price',
    RESOURCES_LISTING_ITEM_STATUS_OUT_OF_STOCK: 'Out of stock',
    RESOURCES_LISTING_ITEM_STATUS_PARSING_FAILED_UNKNOWN_ERROR: 'Parsing failed',
}


HELP_MESSAGE = """Usage
=====
    python run.py <command> [options]

Run a schedular

Commands
========
discover                discover new product/listing
                            available options:
                                -a domain=...
                                -a urls=... comma separated urls
                                -a asins=... comma separated asins
track                   track existing products/listings
                            available options:
                                -a domain=...
                                -a urls=... comma separated urls
                                -a asins=... comma separated asins
jobs                    monitor/update existing jobs

Options
=======
--help, -h              show this help message and exit
--deploy, -d            deploy new egg to scrapyd server
--project=PROJECT, -p=PROJECT
                        project name
--version=VERSION, -v=VERSION
                        version name
--spider=SPIDER, -s=SPIDER
                        spider name
-a NAME=VALUE list      set spider argument (may be repeated)"""

DEFAULT_SPIDER = 'StoreItemPageSpider'
