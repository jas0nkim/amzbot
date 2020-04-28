## django integration

import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'djg.settings'
django.setup()

## django integration end

## config, custom logger

import logging, graypy
from djg.settings import APP_CONFIG_FILEPATH, APP_DIST_DIRPATH

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

## config, custom logger end

import ast
from datetime import datetime
from scrapyd_api import ScrapydAPI
from scrapyd_api.exceptions import ScrapydResponseError
from django.core.exceptions import ObjectDoesNotExist
from djg.settings import BASE_DIR
from djg.schedules.models import Job, Version



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

    def addversion(self, project, version, egg_filename='amzbot-0.0.1-py3.7.egg'):
        """ Scrapyd API: addversion - https://scrapyd.readthedocs.io/en/stable/api.html#addversion-json
        """
        if not self._scrapyd:
            logger.error("No scrapyd object find. Unable to add a new version.")
            return None
        num_of_spiders = None
        try:
            with open(os.path.join(os.path.dirname(APP_DIST_DIRPATH), egg_filename), 'rb') as egg:
                num_of_spiders = self._scrapyd.add_version(project, version, egg)
        except FileNotFoundError as e:
            logger.error("{}: {}".format(class_fullname(e), str(e)))
        except ScrapydResponseError as e:
            logger.error("{}: Response error - {}".format(class_fullname(e), str(e)))
        except Exception as e:
            logger.error("{}: Failed to add a new version - {}".format(class_fullname(e), str(e)))
        else:
            logger.info("new version '{}' for project '{}' added - {} spider(s)".format(project, version, num_of_spiders))
            v = Version()
            v.project = project
            v.version = version
            v.status = Version.STATUS_ADDED
            v.added_at = datetime.now()
            v.save()
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
            j = Job()
            j.project = project
            j.version = kwargs.pop('_version', None)
            j.settings = settings
            j.other_params = kwargs
            j.status = Job.STATUS_PENDING
            j.save()
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
                try:
                    j = Job.objects.get(job_id=x['id'])
                except ObjectDoesNotExist as e:
                    logger.error("{}: Job '{}' doesn't exist in db - {}".format(class_fullname(e), x['id'], str(e)))
                else:
                    if j.status != Job.STATUS_RUNNING:
                        j.start_time = x['start_time']
                        j.status = Job.STATUS_RUNNING
                        j.save()
            for x in d['finished']:
                try:
                    j = Job.objects.get(job_id=x['id'])
                except ObjectDoesNotExist as e:
                    logger.error("{}: Job '{}' doesn't exist in db - {}".format(class_fullname(e), x['id'], str(e)))
                else:
                    if j.status != Job.STATUS_FINISHED:
                        j.start_time = x['start_time']
                        j.end_time = x['end_time']
                        j.status = Job.STATUS_FINISHED
                        j.save()

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
            for v in Version.objects.filter(project=project, version=version):
                v.status = Version.STATUS_DELETED
                v.save()
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
            for v in Version.objects.filter(project=project):
                v.status = Version.STATUS_DELETED
                v.save()
        finally:
            return deleted

    def close(self):
        self._scrapyd.client.close()
