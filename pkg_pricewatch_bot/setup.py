# build egg command: python setup.py bdist_egg -d /usr/local/etc/pricewatch/dist

from setuptools import setup, find_packages

setup(
    name = 'pricewatch_bot',
    version = '0.0.1',
    package_dir = {'': 'src'},
    packages = find_packages(where='src', exclude=["pwbot.tests", "pwbot.tests.*"]),
    install_requires = [
        'Scrapy==2.0.1',
        'Pillow==7.0.0',
        'scrapy-crawlera==1.7.0',
        'graypy==2.1.0',
        'treq==20.4.1',
        'tldextract==2.2.2',
    ],
    # scripts = ['src/manage.py'],
    entry_points = {'scrapy': ['settings = pwbot.settings']},
)
