from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'amzbot',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = required,
    scripts = ['djg/manage.py'],
    entry_points = {'scrapy': ['settings = amzbot.settings']},
)
