# build egg command: python setup.py bdist_egg -d /usr/local/etc/pwbot_schedular/dist

from setuptools import setup, find_packages

setup(
    name = 'pricewatch_schedular',
    version = '0.0.1',
    package_dir = {'': 'src'},
    packages = find_packages(where='src', exclude=["pwschedular.tests", "pwschedular.tests.*"]),
    install_requires = [
        'treq==20.4.1',
        'python-scrapyd-api==2.1.2',
        'graypy==2.1.0',
    ],
    # entry_points = {'scrapy': ['settings = pwbot.settings']},
)
