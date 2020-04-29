# build egg command: python setup.py bdist_egg -d /usr/local/etc/amzbot/dist

from setuptools import setup, find_packages

setup(
    name = 'pricewatch-web',
    version = '0.0.1',
    package_dir = {'': 'src'},
    packages = find_packages(where='src'),
    install_requires = [
        'psycopg2==2.8.5',
        'Django==3.0.5',
        'djangorestframework==3.11.0',
    ],
    scripts = ['src/manage.py'],
    # entry_points = {'scrapy': ['settings = amzbot.settings']},
)
