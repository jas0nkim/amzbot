from pwschedular._common_settings import *

HELP_MESSAGE = """Usage
=====
    python run.py [command] [options]

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
-a NAME=VALUE           set spider argument (may be repeated)"""

DEFAULT_SPIDER = 'AmazonItemPageSpider'
