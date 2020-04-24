## django integration

import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'djg.settings'
django.setup()

## django integration end

from scrapyd_api import ScrapydAPI
from amzbot import utils
from amzbot.settings import logger, config
from djg.settings import BASE_DIR


class BotSchedular(object):

    def __init__(self):
        try:
            self._scrapyd = ScrapydAPI('http://{}:{}'.format(config['Scrapyd']['host'], config['Scrapyd']['port']))
        except KeyError as e:
            logger.error("{}: No such key exists - {}".format(utils.class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to create a scrapyd object - {}".format(utils.class_fullname(e), str(e)))

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
            logger.error("{}: {}".format(utils.class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to add a new version - {}".format(utils.class_fullname(e), str(e)))


