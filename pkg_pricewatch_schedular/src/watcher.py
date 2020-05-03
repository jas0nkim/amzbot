# watcher.py
#
# periodically watch listings already exist in db.
#
# steps
#
# take two options from command - 1. start new jobs (schedule), 2. monitor existing jobs (listjobs)
# 
# start new jobs (schedule)
#
# 0. if no project/version in scrapyd server available, then (addversion)
# 1. retrieve all parent_asins in db
# 2. create a new job with the parent_asins - max 10 parent_asins
# 
#
# monitor existing jobs (listjobs)
#
# 0. if no project/version in scrapyd server available, then (addversion)
# 1. update jobs

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

def get_available_parent_asins(domain):
    """ todo: filter parent asins with 'domain'
    """
    resp = requests.get(
        'http://{}:{}/api/resource/amazon_parent_listing/?format=json'.format(
            config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port']))
    if resp.status_code != 200:
        raise Exception(
            "Failed retrieving parent asins ({})".format(domain))
    r = resp.json()
    return '' if 'results' not in r else ','.join([
        x['parent_asin'] for x in r['results']])

def schedule_jobs(asins, domain, settings=None):
    if schedular.schedule(project=PROJECT,
        spider=SPIDER,
        settings=settings,
        _version=VERISON,
        asins=asins,
        domain=domain) is None:
        raise Exception(
            "Failed schedule a job: ({})".format(domain))
    

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

    domain = 'amazon.com'
    global schedular
    schedular = Schedular()

    addversion_if_non()
    schedule_jobs(asins=get_available_parent_asins(domain=domain),
        domain=domain, settings=None,)


if __name__ == "__main__":
    main(sys.argv[1:])
