from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Crawl(models.Model):
    link = models.TextField()
    domain = models.CharField(max_length=32)
    key_one = models.CharField(max_length=32, blank=True, null=True)
    key_two = models.CharField(max_length=32, blank=True, null=True)
    job_id = models.CharField(max_length=64, db_index=True)
    errors = JSONField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_FAILED = 0
    STATUS_SUCCEEDED = 1

    def __str__(self):
        return '{} @{}'.format(self.key_one, self.domain)

    class Meta:
        db_table = 'rprt_crawls'
