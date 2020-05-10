## May 9 2020
- finish docker/docker-compose.yml
    - django migrate database
    - setup Gunicorn + Nginx for production (keep django built-in web server for development)
- what are the problems again?
    - "Coding is not enough. Software engineering is solving problems.. So what is my problem?"
        - not accurate scraping
            cannot handle scraping errors
            slow scraping
        - not accurate ebay listing
            cannot handle ebay listing errors
        - not fully automated order handling
        - not a good customer services
- UI
    - scraping status screen (error report)
- secure API connection
    - provide token
    - check out django + django restful framework
- how would handle http errors on api?? log in db?

## May 8 2020
- build separate postgres docker container and network with 'web' package.
    - docker-composer
        - nginx
        - web/api app (django)
        - db (postgres)
        - scrapyd (bot egg)
        - scrapy schedular
        - graylog
        - mongodb (graylog-related)
        - elasticsearch (graylog-related)

## May 7 2020
- either 'domain' + 'asins' OR 'urls'
    if 'urls' entered 'domain' will be ignored
- listing_item_spider.py line 78 error:
    unable to retrieve asin from url - check function utils.extract_asin_from_url:
    https://www.amazon.com/Gildan-Mens-T-Shirt-Assortment-Small/dp/B077ZKF9ZN/ref=zg_bs_fashion_1?_encoding=UTF8&refRID=NSX2F9SWW59TZN9SDX7K&th=1

## May 6 2020
- store original crawling data in raw_* table
    - domain
    - url
    - data (json)
    - created_at

## May 5 2020
- research mongodb and ScrapydWeb https://github.com/my8100/scrapydweb
    - mongodb for django: djongo https://djongo.readthedocs.io/docs/get-started/
- use coverage.py (https://coverage.readthedocs.io/en/latest/) for testing
    - command line:
        coverage run -m unittest discover src/ -v
        coverage report -m
        coverage html

## May 4 2020
- finish discovery.py and watcher.py. and combine into a single script
    - 1. add new job to discover new product/listing
    - 2. add new job to track existing products/listings
    - 3. monitor jobs

## May 2 2020
- need to fix 'bot' treq calls.. 'bot' only 'post' to api. api server need to decide either create or update from the 'post' calls. just like 'schedule.vision' we did.

## May 1 2020
- fix api to handle 'bot', and 'schedular' package
    - for schedular
        - create Version
        - update Version
        - create Job
        - update Job

## Apr 30 2020
- no 'treq' for scheduler... gave up. switch to 'requests'.
- complete/test seperation of 'pricewatch_web' package
    - test REST with scrapy deferred signal handlers (rename package from 'pwbot' to 'pricewatch_bot')
    - make 'schedular' to work with REST (rename package from 'schedular' to 'pricewatch_schedular')
- django-angular for the website

## Apr 29 2020
- "Coding is not enough. Software engineering is solving problems.. So what is my problem?"
    - not accurate scraping
        cannot handle scraping errors
        slow scraping
    - not accurate ebay listing
        cannot handle ebay listing errors
    - not fully automated order handling
    - not a good customer services

## Apr 28 2020
- usd scrapy signals Deferred signal handlers https://docs.scrapy.org/en/latest/topics/signals.html#deferred-signal-handlers
    - separate django and scrapy packages
- Django REST framework https://www.django-rest-framework.org/
- rprt_crawls
    - link
    - domain
    - key_one
    - key_two
    - jobid
    - errors
    - status (succeed, failed)
    - created_at
- scrapy signals (https://docs.scrapy.org/en/latest/topics/signals.html)
- reports (analyse crawl) screen
    - number of crawled pages per day
    - 매번 crawling 할때 마다 어떤 asin/link를 crawl 했는지 (scrapy schedule 할때 입력된 asin/link 보여주기)
    - 각 schedule 당 에러가 몇개 났는지. 그리고 그 에러의 중요도는 어떤지
    - 각 schedule/asin 당 에러가 몇개 났는지. 그리고 그 에러의 중요도는 어떤지. 중요한 에러 보여주기
- eBay publisher
- login service
- dashboard screen
    - show any asins/links NOT been crawled more than 24 hours
    - list of asins/links got ERROR messages during the last 24 hours
    - total number of links crawled during last 24 hours
    - total number of links got ERRORS during last 24 hours
    - price monitor
- scrapinghub crawlera alternative
    - http://scrapoxy.io/

## Apr 27 2020
- problem
    - scraping monitoring
    - ebay listing monitoring
    - ordering automation
## Apr 25-26 2020
- good web crawling blogs
    https://towardsdatascience.com/https-towardsdatascience-com-5-tips-to-create-a-more-reliable-web-crawler-3efb6878f8db
    https://blog.hubspot.com/marketing/google-cache
- scrapinghub crawlera alternative
    - http://scrapoxy.io/
    - https://infatica.io/
- scrapy-splash: Scrapy & JavaScript integration through Splash
    https://github.com/scrapy-plugins/scrapy-splash
- jobs (db table)
    - scheduled_at
    - job_started_at
    - job_ended_at
    - project
    - spider
    - asins
    - domain
- build a test spider egg
- scrapyd + python-scrapyd-api +  scrapy signals (https://docs.scrapy.org/en/latest/topics/signals.html)
    - crawl_statuses (new db table)
        - status
        - scrapyd schedule id
        - url
        - asin
        - error
        - error message

## Apr 23 2020
- schedular package based on python-scrapyd-api

## Apr 22 2020
- scrapyd
    - setup.py
        - handle config files.. may not install config files within a package.. different approach..
    - control scrapyd with python-scrapyd-api (https://github.com/djm/python-scrapyd-api)
        - schedule with given asins/urls

## Apr 21 2020
- scrapyd
    - test
    - docker

## Apr 20 2020
- deploy to scrapyd server
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
        - pwbot application
        - scrapyd server
        - graylog
    - login service
    - frontend - pwbotweb
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
- setup pwbot database, and django models

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
        pwbot
            scrapy.cfg
            requirements.txt
            ...
            pwbot
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
