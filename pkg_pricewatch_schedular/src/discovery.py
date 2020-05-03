# discovery.py
#
# find new product/listing and store in database


#!/usr/bin/env python3

import sys, os, getopt
import requests
from pwschedular import Schedular, logger, class_fullname
from pwschedular import _common_settings as settings

import configparser
config = configparser.ConfigParser()
config.read(settings.APP_CONFIG_FILEPATH)


PROJECT = 'pricewatch_bot'
VERISON = 'v01'
SPIDER = 'ListingItemsSpider'

schedular = None

def addversion_if_non():
    egg = 'pricewatch_bot-0.0.1-py3.7.egg'
    num_of_spiders = 0
    try:
        num_of_spiders = schedular.addversion(project=PROJECT,version=VERISON)
    except Exception as e:
        logger.error("{}: {}".format(
            class_fullname(e), str(e)))
    if num_of_spiders < 1:
        raise Exception("Failed adding new project version.")

def schedule_jobs(settings, **kwargs):
    if schedular.schedule(project=PROJECT,
        spider=SPIDER,
        settings=settings,
        _version=VERISON,
        **kwargs) is None:
        raise Exception("Failed schedule a job")

def main(argv):
    # fname = os.path.basename(__file__)
    # try:
    #     opts, args = getopt.getopt(argv, "ho:", ["order="])
    # except getopt.GetoptError:
    #     print('{} -o <recent>'.format(fname))
    #     sys.exit(2)

    # for opt, arg in opts:
    #     if opt == '-h':
    #         print('{} -o <recent>'.format(fname))
    #         sys.exit()
    #     elif opt in ("-o", "--order"):
    #         order = arg
    # run(order, restockonly)

    # domain = 'amazon.com'
    global schedular
    schedular = Schedular()

    # addversion_if_non()

    extra_params = [
        {
            'asins': 'B077HZ4XR6,B07X9STSZR',
            'domain': 'amazon.com',
        },
        {
            'asins': 'B01M1OIS3H,B077ZKFDHX',
            'domain': 'amazon.ca',
        },
    ]

    for p in extra_params:
        schedule_jobs(settings=None, **p)


if __name__ == "__main__":
    main(sys.argv[1:])
