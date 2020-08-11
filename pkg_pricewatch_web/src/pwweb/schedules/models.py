from django.db import models

# Create your models here.
class Job(models.Model):
    job_id = models.CharField(max_length=64, primary_key=True)
    project = models.CharField(max_length=32, db_index=True)
    spider = models.CharField(max_length=32, db_index=True)
    version = models.CharField(max_length=32, blank=True, null=True)
    settings = models.JSONField(blank=True, null=True)
    other_params = models.JSONField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {} - {}'.format(self.project, self.version, self.job_id)

    class Meta:
        db_table = 'sched_jobs'


class Version(models.Model):
    project = models.CharField(max_length=32, db_index=True)
    version = models.CharField(max_length=32, db_index=True)
    status = models.SmallIntegerField(default=1)
    added_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.project, self.version)

    class Meta:
        db_table = 'sched_versions'
        constraints = [
            models.UniqueConstraint(fields=['project', 'version'], name='unique_project_version')
        ]
