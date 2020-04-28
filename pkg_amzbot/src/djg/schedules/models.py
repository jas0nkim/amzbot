from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Job(models.Model):
    job_id = models.CharField(max_length=64, primary_key=True)
    project = models.CharField(max_length=32, db_index=True)
    spider = models.CharField(max_length=32, db_index=True)
    version = models.CharField(max_length=32, blank=True, null=True)
    settings = JSONField(blank=True, null=True)
    other_params = JSONField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CANCELED = 0
    STATUS_PENDING = 1
    STATUS_RUNNING = 2
    STATUS_FINISHED = 3

    def __str__(self):
        return '{} {} - {}'.format(self.project, self.version, self.job_id)

    class Meta:
        db_table = 'sched_jobs'


class Version(models.Model):
    project = models.CharField(max_length=32, db_index=True)
    version = models.CharField(max_length=32, db_index=True)
    status = models.SmallIntegerField(default=1)
    added_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    STATUS_DELETED = 0
    STATUS_ADDED = 1

    def __str__(self):
        return '{} {}'.format(self.project, self.version)

    class Meta:
        db_table = 'sched_versions'
        unique_together = ['project', 'version']
