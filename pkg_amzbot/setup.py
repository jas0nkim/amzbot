# build egg command: python setup.py bdist_egg -d /usr/local/etc/amzbot/dist

from setuptools import setup, find_packages

with open('../requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'amzbot',
    version = '0.0.1',
    package_dir = {'': 'src'},
    packages = find_packages(where='src', exclude=["amzbot.tests", "amzbot.tests.*"]),
    install_requires = required,
    scripts = ['src/manage.py'],
    entry_points = {'scrapy': ['settings = amzbot.settings']},
)
