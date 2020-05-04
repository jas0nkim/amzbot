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
-a NAME=VALUE           set spider argument (may be repeated)"""
