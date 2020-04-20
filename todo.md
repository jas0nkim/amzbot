## Apr 20 2020
- deploy to scrapyd server
- eBay publisher
- login service
- project focus
    - price watch
    - showing graph of price changing
    - crawl price daily

## Apr 19 2020
- improve tests
    - check variation asins
    - request url (check http status == 200)
        actually this depends on crawlera...
    - parse original (before sale) price
- new table amazon_listing_prices - log price history
    - asin
    - price
    - origina_price
    - created_at

## Apr 18 2020
- bug fix
    https://www.amazon.ca/Hotel-Spa-Collection-Herringbone-Textured/dp/B008I25JB2/ref=sr_1_28?fst=as%3Aoff&qid=1587160260&refinements=p_85%3A5690392011&rnid=5690384011&rps=1&s=apparel&sr=1-28&th=1
    doesn't insert into db
- test driven development
    - write test first!

## Apr 17 2020
- unit testing
    https://docs.python.org/3/library/unittest.html
    https://stackoverflow.com/questions/6456304/scrapy-unit-testing
- microservices
    - crawling service (dockers)
        - amzbot application
        - scrapyd server
        - graylog
    - login service
    - frontend - amzbotweb
        - display result

## Apr 16 2020
- django model handle update
    https://docs.djangoproject.com/en/3.0/topics/db/models/#overriding-predefined-model-methods
    https://docs.djangoproject.com/en/3.0/ref/models/instances/#saving-objects

## Apr 15 2020
- implement crawlera
- store items in postgres db
- crawl variations

## Apr 13 2020
- switch db from MySQL to PostgreSQL
    - json field
    https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField
- install postgres
    https://www.robinwieruch.de/postgres-sql-macos-setup
- connect django to postgres
    https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django
    pip install psycopg2 # python driver for postgres

## Apr 10 2020
- graylog
    - modify docker config: sync data directories to the host machine
        https://docs.graylog.org/en/latest/pages/configuration/file_location.html
    - dashboard
        https://docs.graylog.org/en/latest/pages/dashboards.html
- setup amzbot database, and django models

## Apr 04 2020
- logging system
    - graylog
- mysql connection

### Week of 2020-03-29 - 2020-04-04
- scrapy-djangoitem install/implement to scrapy items
- rename: amazoncrawler -> amazonlistingsbot
- run scrapyd with docker-compose
- docker-compose services:
    1. scrapyd server
    2. mysql database server
    3. scrapy/django app
        amzbot
            scrapy.cfg
            requirements.txt
            ...
            amzbot
                __init__.py
                items.py
                pipelines.py
                settings.py (path hacking: https://stackoverflow.com/questions/19068308/access-django-models-with-scrapy-defining-path-to-django-project)
                spiders
                    __init__.py
                    ...
            djg (django application)
                manage.py
                djg
                    __init__.py
                    asgi.py
                    wsgi.py
                    setting.py
                    ...

### Week of 2020-03-22 - 2020-03-28
- setup.py (scrapy cloud)
    - https://medium.com/@chiayinchen/crawler-what-can-i-do-with-scrapy-cloud-edc336bc85e7
    .
    ├── CarolCrawler
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       ├── __init__.py
    │       └── QuotesSpider.py
    ├── bin
    │   └── Hello.py
    │   └── Hello2Crawler.py
    ├── scrapinghub.yml
    ├── scrapy.cfg
    └── setup.py

## Mar 16 2020
- scrapyd
    https://github.com/scrapy/scrapyd-client
    https://scrapyd.readthedocs.io/en/latest/overview.html#how-scrapyd-works
- scrapydweb
    https://github.com/my8100/scrapydweb

## Mar 13 2020
- checkout distributed crawls
    https://docs.scrapy.org/en/latest/topics/practices.html#distributed-crawls
- You can access the cached version for any page that has been saved by Google with this:
    https://webapps.stackexchange.com/a/22111

## Mar 12 2020
- django migration
- init scrapy

### Week of 2020-03-08 - 2020-03-14

- scraping amazon.com product data (price history)
    web scraping platform
- update amazonmws with a modern python3, angular, and docker
    scrape amazon.com products
- Technical Stack
    database - MySQL 8.x/Django 3.0.*
    backend - python 3.7.x/Scrapy 2.0.x/Flask 1.1.x
    frontend - Angular 1.7.x
- Docker based applications
