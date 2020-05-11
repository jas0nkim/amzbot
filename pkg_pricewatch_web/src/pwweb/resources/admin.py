"""
admin page for raw_data

problems with the raw_data:
    incorrect data

solve the issue:
    1. check 'http_status' for each data
        - by url
        - by sku (asin for amazon)
    2. check 'status' for each data
        - by url
        - by sku
    3. any issued url/sku, visit the site.
        - ignore, if the real site has the same problem
        - run auto-unittest/coverage
            - download the page's source, and store as a html file
            - update testlist.json file
            - run coverage / generate html report page
            - display the report html link on the screen

    speaking of.. auto-unittest/coverage system..
        - find a product link from amazon.com (ie best sellers)
        - download its source page, and store as html file
        - update testlist.json file
        - run coverage / generate html report page

admin screen
    - columns
        - sku
        - url (first 10 letters)
        - title (first 10 letters)
        - price
        - item status
        - http status
        - domain
        - collected time
    - searchable by
        - domain
        - title
        - sku
        - http status
        - item status
    - filtered by
        - domain
"""


from django.contrib import admin
from pwweb.resources.models import RawData


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    list_display = ['sku', 'url_short', 'item_title_short', 'price', 'status_str', 'http_status', 'domain', 'created_at', ]
    search_fields = ['data__asin', 'url', 'data__title', 'domain', 'data__status', 'http_status',]
    list_filter = ['domain', 'http_status',]
