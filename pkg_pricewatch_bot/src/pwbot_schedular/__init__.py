## config, custom logger

import os
import ast
import uuid
import json
import logging
import configparser
import requests
import graypy
from datetime import datetime
from setuptools import setup, find_packages
from setuptools.dist import Distribution
from scrapyd_api import ScrapydAPI
from scrapyd_api.exceptions import ScrapydResponseError
from pwbot_schedular import settings


## config, custom logger end

# from django.core.exceptions import ObjectDoesNotExist
# from djg.schedules.models import Job, Version


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

config = configparser.ConfigParser()
config.read(settings.APP_CONFIG_FILEPATH)

graylog_handler = graypy.GELFUDPHandler(config['Graylog']['host'], int(config['Graylog']['port']))
graylog_handler.setLevel(logging.DEBUG) # set logging.ERROR later
graylog_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(graylog_handler)

def build_bot(project=settings.BOT_PROJECT, version=settings.BOT_VERISON, path=settings.APP_DIST_DIRPATH):
    setup(
        name=project,
        version=version,
        packages=find_packages(exclude=[
            'pwbot.tests',
            'pwbot.tests.*',
            'pwbot_schedular',
            'pwbot_schedular.*',
            'run',]),
        install_requires=[
            'Scrapy==2.0.1',
            'Pillow==7.1.2',
            'scrapy-crawlera==1.7.0',
            'graypy==2.1.0',
            'treq==20.4.1',
            'tldextract==2.2.2',
        ],
        script_args=['bdist_egg', '-d', path,],
        entry_points={'scrapy': ['settings = pwbot.settings']},
    )


class Runner:
    def _schedule_jobs(self, project, version, spider, **kwargs):
        if self.schdlr.schedule(project=project,
            spider=spider,
            _version=version,
            **kwargs) is None:
            raise Exception("Failed schedule a job")

    def _addversion_if_non(self):
        num_of_spiders = 0
        try:
            egg_filename = '{}-{}-py3.7.egg'.format(settings.BOT_PROJECT, settings.BOT_VERISON)
            build_bot(project=settings.BOT_PROJECT, version=settings.BOT_VERISON)
            num_of_spiders = self.schdlr.addversion(project=settings.BOT_PROJECT,
                                                    version=settings.BOT_VERISON,
                                                    egg_filename=egg_filename)
        except Exception as e:
            logger.error("{}: {}".format(class_fullname(e), str(e)))
        if num_of_spiders < 1:
            raise Exception("Failed adding new project version.")

    def _get_available_parent_asins(self, domain):
        """ todo: filter parent asins with 'domain'
        """
        resp = requests.get(
            'http://{}:{}/api/resource/amazon_parent_listing/?format=json'.format(
                config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port']))
        if resp.status_code != 200:
            raise Exception(
                "Failed retrieving parent asins ({})".format(domain))
        r = resp.json()
        return '' if 'results' not in r else ','.join([
            x['parent_asin'] for x in r['results']])

    def __init__(self):
        self.schdlr = Schedular()

    def discover(self, add_version, project=None, version=None, spider=None, **kwargs):
        if add_version:
            self._addversion_if_non()
        if project is None:
            project = settings.BOT_PROJECT
        if version is None:
            version = settings.BOT_VERISON
        if spider is None:
            spider = settings.DEFAULT_SPIDER
        self._schedule_jobs(project, version, spider, **kwargs)

    def track(self, add_version, project=None, version=None, spider=None, **kwargs):
        if add_version:
            self._addversion_if_non()
        if project is None:
            project = settings.BOT_PROJECT
        if version is None:
            version = settings.BOT_VERISON
        if spider is None:
            spider = settings.DEFAULT_SPIDER
        if 'domain' in kwargs and 'asins' not in kwargs:
            kwargs['asins'] = self._get_available_parent_asins(domain=kwargs['domain'])
        self._schedule_jobs(project, version, spider **kwargs)

    def jobs(self):
        self.schdlr.listjobs(project=settings.BOT_PROJECT)



def class_fullname(o):
    """ https://stackoverflow.com/a/2020083
    """
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__

class Schedular:

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
            with open(os.path.join(settings.APP_DIST_DIRPATH, egg_filename), 'rb') as egg:
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
                    'status': settings.SCHEDULES_VERSION_STATUS_ADDED,
                    'added_at': str(datetime.now()),
                })
            if not response.ok:
                logger.error("{} HTTP Error: Failed to add a version - {} - {}".format(response.status_code, response.reason, response.text))
        finally:
            return num_of_spiders

    def schedule(self, project, spider, **kwargs):
        if not self._scrapyd:
            logger.error("No scrapyd object find. Unable to schedule a job.")
            return None
        _jobid = str(uuid.uuid4())
        kwargs['jobid'] = _jobid # a scrapyd parameter
        kwargs['job_id'] = _jobid # passing to a spider
        try:
            _s = None # scrapy settings in dict. eg {'DOWNLOAD_DELAY': 2}
            jobid = self._scrapyd.schedule(project, spider, settings=_s, **kwargs)
        except ScrapydResponseError as e:
            logger.error("{}: Response error - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to schedule a job - {}".format(class_fullname(e), str(e)))
        else:
            if jobid != _jobid:
                logger.error("{}: Invalid jobid [enteredid vs returnedid] [{} vs {}] - {}".format(class_fullname(e), _jobid, jobid, str(e)))
            else:
                logger.info("new scheduled job '{}' for project '{}', spider '{}' has been set".format(jobid, project, spider))
                # call API to create a job
                response = requests.post('http://{}:{}/api/schedule/job/'.format(
                        config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port']),
                    json={'job_id': jobid,
                        'project': project,
                        'spider': spider,
                        'version': kwargs.pop('_version', None),
                        'settings': _s,
                        'other_params': kwargs,
                        'status': settings.SCHEDULES_JOB_STATUS_PENDING,
                    })
                if not response.ok:
                    logger.error("{} HTTP Error: Failed to add a new job - {} - {}".format(response.status_code, response.reason, response.text))
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
            self._store_jobs(project, jobs)
        finally:
            return jobs

    def _store_jobs(self, project, jobs):
        """ parse jobs and store information into db
        """
        if all(_j in jobs for _j in ['running', 'finished']):
            for x in jobs['running']:
                # call API to update a running job
                response = requests.put('http://{}:{}/api/schedule/job/{}/'.format(
                        config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port'], x['id']),
                    json={'job_id': x['id'],
                        'project': project,
                        'spider': x['spider'],
                        'start_time': x['start_time'],
                        'status': settings.SCHEDULES_JOB_STATUS_RUNNING,
                    })
                if not response.ok:
                    logger.error("{} HTTP Error: Failed to update a running job - {} - {}".format(response.status_code, response.reason, response.text))
            for x in jobs['finished']:
                # call API to update a finished job
                response = requests.put('http://{}:{}/api/schedule/job/{}/'.format(
                        config['PriceWatchWeb']['host'], config['PriceWatchWeb']['port'], x['id']),
                    json={'job_id': x['id'],
                        'project': project,
                        'spider': x['spider'],
                        'start_time': x['start_time'],
                        'end_time': x['end_time'],
                        'status': settings.SCHEDULES_JOB_STATUS_FINISHED,
                    })
                if not response.ok:
                    logger.error("{} HTTP Error: Failed to update a finished job - {} - {}".format(response.status_code, response.reason, response.text))

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
                    'status': settings.SCHEDULES_VERSION_STATUS_DELETED,
                })
            if not response.ok:
                logger.error("{} HTTP Error: Failed to update a deleted version - {} - {}".format(response.status_code, response.reason, response.text))
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
                    'status': settings.SCHEDULES_VERSION_STATUS_DELETED,
                })
            if not response.ok:
                logger.error("{} HTTP Error: Failed to update deleted project - {} - {}".format(response.status_code, response.reason, response.text))
        finally:
            return deleted

    def close(self):
        self._scrapyd.client.close()
