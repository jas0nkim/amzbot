## config, custom logger

import logging, graypy
from pwschedular import _common_settings as s

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

import configparser
config = configparser.ConfigParser()
config.read(s.APP_CONFIG_FILEPATH)

graylog_handler = graypy.GELFUDPHandler(config['Graylog']['host'], int(config['Graylog']['port']))
graylog_handler.setLevel(logging.DEBUG) # set logging.ERROR later
graylog_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(graylog_handler)

## config, custom logger end

import os, ast, json
from datetime import datetime
from scrapyd_api import ScrapydAPI
from scrapyd_api.exceptions import ScrapydResponseError
import requests
# from django.core.exceptions import ObjectDoesNotExist
# from djg.schedules.models import Job, Version



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
        self._scrapyd = None
        try:
            self._scrapyd = ScrapydAPI('http://{}:{}'.format(config['Scrapyd']['host'], config['Scrapyd']['port']))
        except KeyError as e:
            logger.error("{}: No such key exists - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to create a scrapyd object - {}".format(class_fullname(e), str(e)))

    def addversion(self, project, version, egg_filename='pricewatch_bot-0.0.1-py3.7.egg'):
        """ Scrapyd API: addversion - https://scrapyd.readthedocs.io/en/stable/api.html#addversion-json
        """
        if not self._scrapyd:
            logger.error("No scrapyd object find. Unable to add a new version.")
            return None
        num_of_spiders = None
        try:
            with open(os.path.join(s.APP_DIST_DIRPATH, egg_filename), 'rb') as egg:
                num_of_spiders = self._scrapyd.add_version(project, version, egg)
        except FileNotFoundError as e:
            logger.error("{}: {}".format(class_fullname(e), str(e)))
        except ScrapydResponseError as e:
            logger.error("{}: Response error - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to add a version - {}".format(class_fullname(e), str(e)))
        else:
            logger.info("version '{}' for project '{}' added/updated - {} spider(s)".format(project, version, num_of_spiders))
            # call API to create a version
            response = requests.post('http://{}:{}/api/schedule/version/'.format(
                    config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port']),
                json={'project': project,
                    'version': version,
                    'status': s.SCHEDULES_VERSION_STATUS_ADDED,
                    'added_at': str(datetime.now()),
                })
            if not response.ok:
                logger.error("{} HTTP Error: Failed to add a version - {}".format(response.status_code, response.reason))
        finally:
            return num_of_spiders

    def schedule(self, project, spider, settings=None, **kwargs):
        if not self._scrapyd:
            logger.error("No scrapyd object find. Unable to schedule a job.")
            return None
        jobid = None
        try:
            jobid = self._scrapyd.schedule(project, spider, settings, **kwargs)
        except ScrapydResponseError as e:
            logger.error("{}: Response error - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to schedule a job - {}".format(class_fullname(e), str(e)))
        else:
            logger.info("new scheduled job '{}' for project '{}', spider '{}' has been set".format(jobid, project, spider))
            # call API to create a job
            response = requests.post('http://{}:{}/api/schedule/job/'.format(
                    config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port']),
                json={'job_id': jobid,
                    'project': project,
                    'spider': spider,
                    'version': kwargs.pop('_version', None),
                    'settings': settings,
                    'other_params': kwargs,
                    'status': s.SCHEDULES_JOB_STATUS_PENDING,
                })
            if not response.ok:
                logger.error("{} HTTP Error: Failed to add a new job - {}".format(response.status_code, response.reason))
        finally:
            return jobid

    def listjobs(self, project):
        if not self._scrapyd:
            logger.error("No scrapyd object find. Unable to list jobs.")
            return None
        jobs = None
        try:
            jobs = self._scrapyd.list_jobs(project)
        except ScrapydResponseError as e:
            logger.error("{}: Response error - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to list jobs - {}".format(class_fullname(e), str(e)))
        else:
            logger.info("list of jobs for project '{}' - {}".format(project, str(jobs)))
            self._store_jobs(jobs)
        finally:
            return jobs

    def _store_jobs(self, jobs):
        """ parse jobs and store information into db
        """
        try:
            d = ast.literal_eval(jobs)
            """ convert string to dictionaty
                https://www.geeksforgeeks.org/python-convert-string-dictionary-to-dictionary/
            """
        except Exception as e:
            logger.error("{}: Failed to parse jobs - {}".format(class_fullname(e), str(e)))
        else:
            for x in d['running']:
                # call API to update a running job
                response = requests.put('http://{}:{}/api/schedule/job/{}/'.format(
                        config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port'], x['id']),
                    json={'start_time': x['start_time'],
                        'status': s.SCHEDULES_JOB_STATUS_RUNNING,
                    })
                if not response.ok:
                    logger.error("{} HTTP Error: Failed to update a running job - {}".format(response.status_code, response.reason))
            for x in d['finished']:
                # call API to update a finished job
                response = requests.put('http://{}:{}/api/schedule/job/{}/'.format(
                        config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port'], x['id']),
                    json={'start_time': x['start_time'],
                        'end_time': x['end_time'],
                        'status': s.SCHEDULES_JOB_STATUS_FINISHED,
                    })
                if not response.ok:
                    logger.error("{} HTTP Error: Failed to update a finished job - {}".format(response.status_code, response.reason))

    def delversion(self, project, version):
        """ delversion
        """
        if not self._scrapyd:
            logger.error("No scrapyd object find. Unable to delete version.")
            return False
        deleted = False
        try:
            deleted = self._scrapyd.delete_version(project, version)
        except ScrapydResponseError as e:
            logger.error("{}: Response error - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to delete version - {}".format(class_fullname(e), str(e)))
        else:
            logger.info("successfully deleted project '{}' version '{}'".format(project, version))
            # update deleted version
            response = requests.post('http://{}:{}/api/schedule/version/'.format(
                    config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port']),
                json={'project': project,
                    'version': version,
                    'status': s.SCHEDULES_VERSION_STATUS_DELETED,
                })
            if not response.ok:
                logger.error("{} HTTP Error: Failed to update a deleted version - {}".format(response.status_code, response.reason))
        finally:
            return deleted

    def delproject(self, project):
        """ delproject
        """
        if not self._scrapyd:
            logger.error("No scrapyd object find. Unable to delete version.")
            return False
        deleted = False
        try:
            deleted = self._scrapyd.delete_project(project)
        except ScrapydResponseError as e:
            logger.error("{}: Response error - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to delete project - {}".format(class_fullname(e), str(e)))
        else:
            logger.info("successfully deleted project '{}'".format(project))
            # update deleted project
            response = requests.post('http://{}:{}/api/schedule/version/'.format(
                    config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port']),
                json={'project': project,
                    'status': s.SCHEDULES_VERSION_STATUS_DELETED,
                })
            if not response.ok:
                logger.error("{} HTTP Error: Failed to update deleted project - {}".format(response.status_code, response.reason))
        finally:
            return deleted

    def close(self):
        self._scrapyd.client.close()
