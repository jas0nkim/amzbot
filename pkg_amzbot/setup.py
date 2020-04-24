from setuptools import setup, find_packages

with open('../requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'amzbot',
    version = '0.0.1',
    package_dir = {'': 'src'},
    packages = find_packages(where='src', exclude=["amzbot.tests", "amzbot.tests.*"]),
    install_requires = required,
    scripts = ['src/djg/manage.py'],
    entry_points = {'scrapy': ['settings = amzbot.settings']},
)
