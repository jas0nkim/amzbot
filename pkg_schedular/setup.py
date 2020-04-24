from setuptools import setup, find_packages

with open('../requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'amzbot_schedular',
    version = '0.0.1',
    package_dir = {'': 'src'},
    packages = find_packages(where='src', exclude=["amzbot_schedular.tests", "amzbot_schedular.tests.*"]),
    install_requires = required,
    scripts = ['src/djg/manage.py'],
    # entry_points = {'scrapy': ['settings = amzbot.settings']},
)
