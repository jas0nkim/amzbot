# build egg command: python setup.py bdist_egg -d /usr/local/etc/amzbot_schedular/dist

from setuptools import setup, find_packages

with open('../requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'amzbot_schedular',
    version = '0.0.1',
    package_dir = {'': 'src'},
    packages = find_packages(where='src', exclude=["amzbot_schedular.tests", "amzbot_schedular.tests.*"]),
    install_requires = required,
    # entry_points = {'scrapy': ['settings = amzbot.settings']},
)
