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
        - quantity
        - http status
        - domain
        - collected time
    - searchable by
        - domain
        - title
        - sku
        - http status
    - filtered by
        - domain
"""


from django.contrib import admin
from django.db.models import Q
from pwweb.resources.models import RawData, Item, ItemPrice


@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    ordering = ['-created_at',]
    empty_value_display = '???'
    list_display = ('sku', 'parent_sku', 'url_short', 'item_title_short', 'price', 'quantity', 'http_status', 'domain', )
    list_filter = ('domain', 'http_status',)
    search_fields = ['url', 'domain', 'http_status',]
    # radio_fields = {"http_status": admin.VERTICAL}
    show_full_result_count = False

    def get_search_results(self, request, queryset, search_term):
        """ modify ModelAdmin.get_search_results
        """
        if search_term == '#erroronly':
            _queryset, use_distinct = super().get_search_results(request, queryset, search_term=None)
            _queryset = _queryset.filter(Q(http_status__gte=400))
        else:
            _queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return _queryset, use_distinct

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'parent_sku', 'upc', 'title', 'brand_name', 'domain', )

@admin.register(ItemPrice)
class ItemPriceAdmin(admin.ModelAdmin):
    list_display = ('sku', 'url_short', 'price', 'original_price', 'online_availability', 'online_urgent_quantity', 'domain', 'job_id',)
