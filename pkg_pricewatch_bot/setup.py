# build egg command: python setup.py bdist_egg -d /usr/local/etc/pricewatch/dist

from setuptools import setup, find_packages

setup(
    name='pricewatch_bot',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=["pwbot.tests", "pwbot.tests.*", "pwbot_schedular", "pwbot_schedular.*", "run"]),
    install_requires=[
        'Scrapy==2.1.0',
        'Pillow==7.1.2',
        'scrapy-crawlera==1.7.0',
        'graypy==2.1.0',
        'treq==20.4.1',
        'tldextract==2.2.2',
        'requests==2.23.0'
        'python-scrapyd-api==2.1.2',
    ],
    script_args=['bdist_egg', '-d', '/usr/local/etc/pricewatch/dist',],
    entry_points={'scrapy': ['settings = pwbot.settings']},
)
