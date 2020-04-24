## django integration

import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'djg.settings'
django.setup()

## django integration end

## config, custom logger
import logging, graypy
from djg.settings import APP_CONFIG_FILEPATH

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

import configparser
config = configparser.ConfigParser()
config.read(APP_CONFIG_FILEPATH)

graylog_handler = graypy.GELFUDPHandler(config['Graylog']['host'], int(config['Graylog']['port']))
graylog_handler.setLevel(logging.DEBUG) # set logging.ERROR later
graylog_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(graylog_handler)


from scrapyd_api import ScrapydAPI
from djg.settings import BASE_DIR


def class_fullname(o):
    """ https://stackoverflow.com/a/2020083
    """
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__

class Schedular(object):

    def __init__(self):
        try:
            self._scrapyd = ScrapydAPI('http://{}:{}'.format(config['Scrapyd']['host'], config['Scrapyd']['port']))
        except KeyError as e:
            logger.error("{}: No such key exists - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to create a scrapyd object - {}".format(class_fullname(e), str(e)))

    def addversion(self, project_name='amzbot', version_name='v1', egg_filename='amzbot-0.0.1-py3.7.egg'):
        """ Scrapyd API: addversion - https://scrapyd.readthedocs.io/en/stable/api.html#addversion-json
        """
        if not self._scrapyd:
            logger.error("No scrapyd object find. Unable to add a new version.")
            return
        try:
            with open(os.path.join(os.path.dirname(BASE_DIR), 'dist', egg_filename), 'rb') as egg:
                result = self._scrapyd.add_version(project_name, version_name, egg)
                """ TODO: store result in db
                """ 
            logger.info("new version '{}' for project '{}' added - {} spider(s)".format(project_name, version_name, result))
            return result
        except FileNotFoundError as e:
            logger.error("{}: {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to add a new version - {}".format(class_fullname(e), str(e)))


