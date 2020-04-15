from django.db import models
from django.contrib.postgres.fields import ArrayField


class AmazonParentListing(models.Model):
    parent_asin = models.CharField(max_length=32, unique=True, db_index=True)
    asins = ArrayField(base_field=models.CharField(max_length=32, blank=True, null=True), blank=True, null=True)
    review_count = models.SmallIntegerField(blank=True, null=True, default=0)
    avg_rating = models.FloatField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.parent_asin

    class Meta:
        db_table = 'amazon_parent_listings'


class AmazonListing(models.Model):
    asin = models.CharField(max_length=32, unique=True, db_index=True)
    parent_asin = models.CharField(max_length=32, db_index=True)
    picture_urls = ArrayField(base_field=models.CharField(max_length=255, blank=True, null=True), null=True)
    description = models.TextField(blank=True, null=True)
    url = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    market_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.SmallIntegerField(blank=True, null=True, default=0)
    features = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    variation_specifics = models.CharField(max_length=255, blank=True, null=True)
    is_fba = models.BooleanField(default=0)
    is_addon = models.BooleanField(default=0)
    is_pantry = models.BooleanField(default=0)
    has_sizechart = models.BooleanField(default=0)
    international_shipping = models.BooleanField(default=0)
    merchant_id = models.CharField(max_length=32, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    meta_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1

    def __str__(self):
        return "[{}] {}".format(self.asin, self.title)

    class Meta:
        db_table = 'amazon_listings'
