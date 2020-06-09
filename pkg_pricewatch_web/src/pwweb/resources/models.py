import logging
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from pwweb import settings, utils

class RawData(models.Model):
    url = models.TextField(db_index=True)
    domain = models.CharField(max_length=32, db_index=True)
    http_status = models.SmallIntegerField(blank=True, null=True)
    data = JSONField(blank=True, null=True)
    job_id = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at.short_description = 'collected time'

    @property
    def item_title(self):
        if self.domain in ['amazon.com', 'amazon.ca',]:
            return self.data.get('title', None)
        elif self.domain in ['walmart.com',]:
            if 'item' in self.data and 'product' in self.data['item'] and 'buyBox' in self.data['item']['product'] and 'products' in self.data['item']['product']['buyBox'] and len(self.data['item']['product']['buyBox']['products']) > 0 and 'productName' in self.data['item']['product']['buyBox']['products'][0]:
                return self.data['item']['product']['buyBox']['products'][0]['productName']
        else:
            return None

    @property
    def sku(self):
        if self.data:
            if self.domain in ['amazon.com', 'amazon.ca',]:
                if 'asin' in self.data:
                    return self.data['asin']
            elif self.domain in ['walmart.com',]:
                if len(self.data.get('item', {}).get('product', {}).get('buyBox', {}).get('products', [])) > 0:
                    return self.data['item']['product']['buyBox']['products'][0]['usItemId']
            elif self.domain in ['walmart.ca',]:
                if 'product' in self.data and 'item' in self.data['product'] and 'skus' in self.data['product']['item']:
                    return truncatechars(','.join(self.data['product']['item']['skus']), 50)
        else:
            return None

    @property
    def parent_sku(self):
        if self.data:
            if self.domain in ['amazon.com', 'amazon.ca',]:
                if 'parent_asin' in self.data:
                    return self.data['parent_asin']
            elif self.domain in ['walmart.com',]:
                if 'item' in self.data and 'product' in self.data['item'] and 'buyBox' in self.data['item']['product'] and 'primaryUsItemId' in self.data['item']['product']['buyBox']:
                    return self.data['item']['product']['buyBox']['primaryUsItemId']
            elif self.domain in ['walmart.ca',]:
                if 'product' in self.data and 'item' in self.data['product'] and 'id' in self.data['product']['item']:
                    return self.data['product']['item']['id']
        else:
            return None

    @property
    def price(self):
        if self.data:
            if self.domain in ['amazon.com', 'amazon.ca',]:
                if 'price' in self.data:
                    return self.data['price']
            elif self.domain in ['walmart.com',]:
                if 'item' in self.data and 'product' in self.data['item'] and 'buyBox' in self.data['item']['product'] and 'products' in self.data['item']['product']['buyBox']:
                    return self.data['item']['product']['buyBox']['products'][0]['priceMap']['price']
            elif self.domain in ['walmart.ca',]:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['currentPrice']
                    return truncatechars(str(prices), 50)
        else:
            return None

    @property
    def quantity(self):
        if self.data:
            if self.domain in ['amazon.com', 'amazon.ca',]:
                if 'quantity' in self.data:
                    return self.data['quantity']
            elif self.domain in ['walmart.com',]:
                if 'item' in self.data and 'product' in self.data['item'] and 'buyBox' in self.data['item']['product'] and 'products' in self.data['item']['product']['buyBox']:
                    if self.data['item']['product']['buyBox']['products'][0]['availabilityStatus'] == 'OUT_OF_STACK':
                        return 'out of stock'
                    elif self.data['item']['product']['buyBox']['products'][0]['availabilityStatus'] == 'IN_STOCK':
                        if self.data['item']['product']['buyBox']['products'][0]['urgentQuantity']:
                            return self.data['item']['product']['buyBox']['products'][0]['urgentQuantity']
                        else:
                            return 'in stock'
                    else:
                        return 'N/A'
            elif self.domain in ['walmart.ca',]:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['availableQuantity']
                    return truncatechars(str(prices), 50)
        else:
            return None

    def url_short(self):
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(self.url, truncatechars(self.url, 50)))
    url_short.short_description = 'url'

    def item_title_short(self):
        return truncatechars(self.item_title, 50)
    item_title_short.short_description = 'title'

    class Meta:
        db_table = 'resrc_raw_data'


class Item(models.Model):
    domain = models.CharField(max_length=32, db_index=True)
    sku = models.CharField(max_length=32, db_index=True)
    parent_sku = models.CharField(max_length=32, blank=True, null=True)
    upc = models.CharField(max_length=20, blank=True, null=True)
    title = models.TextField()
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    picture_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resrc_items'


class ItemPrice(models.Model):
    domain = models.CharField(max_length=32, db_index=True)
    job_id = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    sku = models.CharField(max_length=32, db_index=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    original_price = models.DecimalField(max_digits=15, decimal_places=2)
    online_availability = models.SmallIntegerField(default=1)
    online_urgent_quantity = models.SmallIntegerField(blank=True, null=True)
    store_availabilities = JSONField(blank=True, null=True)
    """ store_availabilities json format:
        [
            {
                'store_id': '5027',
                'store_name': 'Lancaster Supercenter',
                'store_address': '4975 Transit Rd'
                'store_city': 'Lancaster'
                'store_state_or_province': 'NY'
                'store_postal_code': '14221'
                'store_phone': '716-206-3050',
                'store_availability': 1 [1 (available) | 0 (unavailable)]
                'store_urgent_quantity': 5 (nullable)
            },
            {
                ...
            },
        ]
    """
    created_at = models.DateTimeField(auto_now_add=True)

    ITEM_PRICE_AVAILABILITY_OUT_OF_STOCK = 0
    ITEM_PRICE_AVAILABILITY_IN_STOCK = 1

    class Meta:
        db_table = 'resrc_item_prices'

class BuildWalmartCaItemPrice:
    """ walmart.ca specific version of BuildItemPrice
    """
    _job_id = None
    _domain = None
    _url = None

    _data = None
    _price_data = None
    _stores_raw_data = None

    _items = []
    _item_prices = []

    def __init__(self, raw_data=None, price_raw_data=None, stores_raw_data=None):
        """ price_raw_data:
                RawData.objects.get(domain=self._domain,
                                    url=settings.WALMART_CA_API_ITEM_PRICE_LINK_FORMAT.format(_parent_sku),
                                    job_id=self._job_id,)

            stores_raw_data:
            ret = {}
            for s in RawData.objects.filter(domain=self._domain,
                                                url__startwith=settings.WALMART_CA_API_ITEM_FIND_IN_STORE_LINK,
                                                job_id=self._job_id,):
                ret[extract_upc_from_url(s.url)] = s
            return ret

            self.logger.error('[{}] walmart.ca: no find in store data scraped - [parent sku:{}] [sku:{}]'.format(self._job_id, _parent_sku, sku))

            i.e.
            {
                upc_1: RawData_1,
                upc_2: RawData_2,
                upc_3: RawData_3,
                ...
            }
        """

        self.logger = logging.getLogger('pwweb.resources.models.BuildWalmartCaItemPrice')
        if not isinstance(raw_data, RawData):
            raise Exception('Invalid raw_data value passed. Not a RawData type')
        if not isinstance(price_raw_data, RawData):
            raise Exception('Invalid price_raw_data value passed. Not a RawData type')
        self._job_id = raw_data.job_id
        self._domain = raw_data.domain
        self._url = raw_data.url
        self._data = raw_data.data
        self._price_data = price_raw_data.data
        self._stores_raw_data = stores_raw_data

        if self._domain in ['walmart.ca',]:
            self._build_walmart_ca_item_price()
        else:
            raise Exception('[{}] domain supposed to be walmart.ca. wrong domain passed instead: {}'.format(self._job_id, self._domain))

    def get_items(self):
        """ get list of walmart.ca model.Item object
        """
        return self._items

    def get_item_prices(self):
        """ get list of walmart.ca model.ItemPrice object
        """
        return self._item_prices

    def _build_walmart_ca_item_price(self):
        """ sku: data['product']['item']['skus'] or data['entities']['skus'][SKU] (multiple)
            parent_sku: data['product']['item']['id']
            upc: data['entities']['skus'][SKU]['upc'][0] (multiple)
            title: data['entities']['skus'][SKU]['name'] (multiple)
            brand_name: data['entities']['skus'][SKU]['brand']['name'] (multiple)
            picture_url: data['entities']['skus'][SKU]['images'][0]['large']['url']

            * from https://www.walmart.ca/api/product-page/price-offer
            price:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['currentPrice']
                    return str(prices)
            original_price:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['regularPrice']
                    return str(prices)
            online_availability:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['gmAvailability'] [ Available or not]
                    return str(prices)
            online_urgent_quantity:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['availableQuantity']
                    return str(prices)

            * from https://www.walmart.ca/api/product-page/find-in-store
            store_availabilities:
                'store_id': data['info'][]['id'],
                'store_name': data['info'][]['displayName'],
                'store_address': data['info'][]['intersection'],
                'store_city': None,
                'store_state_or_province': None,
                'store_postal_code': None,
                'store_phone': None,
                'store_availability': 1 [1 (data['info'][]['availabilityStatus'] == 'LIMITED' | 'AVAILABLE' ) | 0 (unavailable)],
                'store_urgent_quantity': 5 (data['info'][]['availableToSellQty'] | None)
        """
        _parent_sku = utils.extract_sku_from_url(url=self._url, domain=self._domain)
        if _parent_sku is None:
            raise Exception('[{}] SKU cannot be extracted from url - {}'.format(self._job_id, self._url))
        for sku, _product_info in self._data['entities']['skus'].items():
            _upc = _product_info['upc'][0] if len(_product_info.get('upc', [])) > 0 else None
            _item = None
            try:
                _item = Item.objects.get(domain=self._domain, sku=sku)
            except Item.DoesNotExist:
                # create new item
                _item = Item.objects.create(domain=self._domain,
                            sku=sku,
                            parent_sku=_parent_sku,
                            upc=_upc,
                            title=_product_info.get('name'),
                            brand_name=_product_info.get('brand', {}).get('name'),
                            picture_url=_product_info['images'][0].get('large', {}).get('url') if len(_product_info.get('images', [])) > 0 else None,
                        )
            self._items.append(_item)

            # generate store_availabilities json
            store_availabilities = []
            if _upc in self._stores_raw_data:
                for s in self._stores_raw_data[_upc].data['info']:
                    store_availabilities.append({
                        'store_id': str(s.get('id')),
                        'store_name': s.get('displayName'),
                        'store_address': s.get('intersection'),
                        'store_city': None,
                        'store_state_or_province': None,
                        'store_postal_code': None,
                        'store_phone': None,
                        'store_availability': ItemPrice.ITEM_PRICE_AVAILABILITY_IN_STOCK if (s.get('availabilityStatus') in ['LIMITED', 'AVAILABLE',]) else ItemPrice.ITEM_PRICE_AVAILABILITY_OUT_OF_STOCK,
                        'store_urgent_quantity': s.get('availableToSellQty', 0) if s.get('availableToSellQty', 0) > 0 else None
                    })
            _offer_id = self._price_data['skus'][sku][0] if len(self._price_data.get('skus', {}).get(sku, [])) > 0 else None
            if _offer_id:
                _price = self._price_data.get('offers', {}).get(_offer_id, {}).get('currentPrice')
                _item_price = ItemPrice.objects.create(domain=self._domain,
                                job_id=self._job_id,
                                sku=sku,
                                price=_price,
                                original_price=self._price_data.get('offers', {}).get(_offer_id, {}).get('regularPrice', _price),
                                online_availability=ItemPrice.ITEM_PRICE_AVAILABILITY_IN_STOCK if self._price_data.get('offers', {}).get(_offer_id, {}).get('gmAvailability') == 'Available' else ItemPrice.ITEM_PRICE_AVAILABILITY_OUT_OF_STOCK,
                                online_urgent_quantity=self._price_data.get('offers', {}).get(_offer_id, {}).get('availableQuantity'),
                                store_availabilities=store_availabilities if len(store_availabilities) > 0 else None,
                            )
                self._item_prices.append(_item_price)


class BuildCanadiantireCaItemPrice:
    """ canadiantire.ca specific version of BuildItemPrice
    """
    _job_id = None
    _domain = None
    _url = None

    _data = None
    _store_data = None
    _price_data = None

    _items = []
    _item_prices = []

    def __init__(self, raw_data=None, store_raw_data=None, price_raw_data=None):
        """ store_raw_data:
                RawData.objects.get(domain=self._domain,
                                    url__startwith=settings.CANADIANTIRE_CA_API_STORES_LINK,
                                    job_id=self._job_id,)

            price_raw_data:
                RawData.objects.get(domain=self._domain,
                                    url__startwith=settings.CANADIANTIRE_CA_API_ITEM_PRICE_LINK,
                                    job_id=self._job_id,)
        """

        self.logger = logging.getLogger('pwweb.resources.models.BuildCanadiantireCaItemPrice')
        if not isinstance(raw_data, RawData):
            raise Exception('Invalid raw_data value passed. Not a RawData type')
        if not isinstance(store_raw_data, RawData):
            raise Exception('Invalid store_raw_data value passed. Not a RawData type')
        if not isinstance(price_raw_data, RawData):
            raise Exception('Invalid price_raw_data value passed. Not a RawData type')
        self._job_id = raw_data.job_id
        self._domain = raw_data.domain
        self._url = raw_data.url
        self._data = raw_data.data
        self._store_data = self._build_store_data(store_raw_data.data)
        self._price_data = self._build_price_data(price_raw_data.data)

        if self._domain in ['canadiantire.ca',]:
            self._build_canadiantire_ca_item_price()
        else:
            raise Exception('[{}] domain supposed to be canadiantire.ca. wrong domain passed instead: {}'.format(self._job_id, self._domain))

    def get_items(self):
        """ get list of canadiantire.ca model.Item object
        """
        return self._items

    def get_item_prices(self):
        """ get list of canadiantire.ca model.ItemPrice object
        """
        return self._item_prices

    def _build_store_data(self, data):
        """ convert to:
            {
                "0459": {
                    "timeZone":"(GMT -5) Eastern Time (US, Canada) [US/Eastern]",
                    "storeName":"Eglinton & Laird, ON",
                    "storeType":"CTR",
                    "storeNumber":"0459",
                    ...
                },
                ...
            }
        """
        ret = {}
        for _d in data:
            if _d.get('storeNumber') not in ret:
                ret[_d.get('storeNumber')] = _d
        return ret

    def _build_price_data(self, data):
        """ convert to:
            {
                '1871455': [
                    {
                        'SKU': '1871455',
                        'Price': ...,
                        'Store': '0011',
                        'Banner': ...,
                        ...
                    },
                    {
                        'SKU': '1871455',
                        'Price': ...,
                        'Store': '0045',
                        'Banner': ...,
                        ...
                    },
                ],
                '1871456': [
                    {
                        'SKU': '1871456',
                        'Price': ...,
                        'Store': '0011',
                        'Banner': ...,
                        ...
                    },
                    {
                        'SKU': '1871456',
                        'Price': ...,
                        'Store': '0045',
                        'Banner': ...,
                        ...
                    },
                    ...
                ]
                ...
            }
        """
        ret = {}
        for _d in data:
            if _d.get('SKU') not in ret:
                ret[_d.get('SKU')] = []
            ret[_d.get('SKU')].append(_d)
        return ret

    def _build_canadiantire_ca_item_price(self):
        """ sku: data['SkuSelectors']['skuListProperties'] (multiple)
            parent_sku: data['SkuSelectors']['pCode']
            upc: None
            title: data['ProductStickyToc']['productName']
            brand_name: data['SkuSelectors']['BrandLogoLink']['brandName']
            picture_url: data['ProductStickyToc']['imageUrl']

            * from https://www.canadiantire.ca/ESB/PriceAvailability
            price:
                price = data[0].get('Price')
                for _p in data:
                    if _p.get('SKU') == ... and _p.get('Promo', {}).get('Price'):
                        price = _p.get('Promo', {}).get('Price')
                        break
            original_price:
                data[0].get('Price')
            online_availability: if data[0].get('Corporate', {}).get('Quantity', 0) > 0 [ available or not ]
            online_urgent_quantity: data[0].get('Corporate', {}).get('Quantity', 0)
            * from https://api-triangle.canadiantire.ca/dss/services/v4/stores & https://www.canadiantire.ca/ESB/PriceAvailability
            store_availabilities:
                for _p in price_data:
                    for _s in store_data:
                        if _p.get('SKU') == ... and _p.get('Store') == _s.get('storeNumber'):
                            'store_id': _s['storeNumber'],
                            'store_name': _s['storeName'],
                            'store_address': ' '.join(_s['storeAddress1'], _s['storeAddress2']),
                            'store_city': _s['storeCityName'],
                            'store_state_or_province': _s['storeProvince'],
                            'store_postal_code': _s['storePostalCode'],
                            'store_phone': _s['storeTelephone'],
                            'store_availability': if _p.get('Quantity', 0) > 0 [ available or not ],
                            'store_urgent_quantity': _p.get('Quantity', None)
        """
        _sk = utils.extract_sku_from_url(url=self._url, domain=self._domain)
        if _sk is None:
            raise Exception('[{}] SKU cannot be extracted from url - {}'.format(self._job_id, self._url))
        for sku in self._data.get('SkuSelectors', {}).get('skuListProperties', {}.keys()):
            _item = None
            try:
                _item = Item.objects.get(domain=self._domain, sku=sku)
            except Item.DoesNotExist:
                # create new item
                _item = Item.objects.create(domain=self._domain,
                            sku=sku,
                            parent_sku=self._data.get('SkuSelectors', {}).get('pCode'),
                            upc=None,
                            title=self._data.get('ProductStickyToc', {}).get('productName'),
                            brand_name=self._data.get('BrandLogoLink', {}).get('brandName'),
                            picture_url=self._data.get('ProductStickyToc', {}).get('imageUrl'),
                        )
            self._items.append(_item)

            # generate store_availabilities json
            price = None
            original_price = None
            online_availability = ItemPrice.ITEM_PRICE_AVAILABILITY_OUT_OF_STOCK
            online_urgent_quantity = None
            store_availabilities = []
            price_data = self._price_data.get(sku)
            for _p in price_data:
                price = _p.get('Promo', {}).get('Price') if price is None else price
                original_price = _p.get('Price') if original_price is None else original_price
                online_availability = ItemPrice.ITEM_PRICE_AVAILABILITY_IN_STOCK if online_availability or _p.get('Corporate', {}).get('Quantity', 0) > 0 else online_availability
                online_urgent_quantity = _p.get('Corporate', {}).get('Quantity') if online_urgent_quantity is None else online_urgent_quantity
                _p_store_id = _p.get('Store')
                if _p_store_id:
                    store_availabilities.append({
                        'store_id': str(_p_store_id),
                        'store_name': self._store_data.get(_p_store_id, {}).get('storeName'),
                        'store_address': ' '.join([self._store_data.get(_p_store_id, {}).get('storeAddress1', ''), self._store_data.get(_p_store_id, {}).get('storeAddress2', ''),]),
                        'store_city': self._store_data.get(_p_store_id, {}).get('storeCityName'),
                        'store_state_or_province': self._store_data.get(_p_store_id, {}).get('storeProvince'),
                        'store_postal_code': self._store_data.get(_p_store_id, {}).get('storePostalCode'),
                        'store_phone': self._store_data.get(_p_store_id, {}).get('storeTelephone'),
                        'store_availability': ItemPrice.ITEM_PRICE_AVAILABILITY_IN_STOCK if _p.get('Quantity') > 0 else ItemPrice.ITEM_PRICE_AVAILABILITY_OUT_OF_STOCK,
                        'store_urgent_quantity': _p.get('Quantity', 0) if _p.get('Quantity', 0) > 0 else None,
                    })
            _item_price = ItemPrice.objects.create(domain=self._domain,
                            job_id=self._job_id,
                            sku=sku,
                            price=price if price else original_price,
                            original_price=original_price,
                            online_availability=online_availability,
                            online_urgent_quantity=online_urgent_quantity if online_urgent_quantity > 0 else None,
                            store_availabilities=store_availabilities if len(store_availabilities) > 0 else None,
                        )
            self._item_prices.append(_item_price)


class BuildItemPrice:
    """ build resrc_item_prices data from resrc_raw_data
    """

    _job_id = None
    _domain = None
    _url = None
    _data = None

    _item = None
    _item_price = None

    def __init__(self, raw_data=None):
        self.logger = logging.getLogger('pwweb.resources.models.BuildItemPrice')

        if not isinstance(raw_data, RawData):
            raise Exception('Invalid raw_data value passed. Not a RawData type')
        self._job_id = raw_data.job_id
        self._domain = raw_data.domain
        self._url = raw_data.url
        self._data = raw_data.data

        if self._domain in ['amazon.com', 'amazon.ca',]:
            self._build_amazon_item_price()
        elif self._domain in ['walmart.com',]:
            self._build_walmart_com_item_price()
        elif self._domain in ['canadiantire.ca',]:
            self._build_canadiantire_ca_item_price()

    def get_item(self):
        """ get model.Item object
        """
        return self._item

    def get_item_price(self):
        """ get model.ItemPrice object
        """
        return self._item_price

    def _build_amazon_item_price(self):
        """ 1. validate url
            2. check item already exist in resrc_items table
            3. extract and store values
                - sku
                - price
                - original price
                - quantity
        """
        sku = utils.extract_sku_from_url(url=self._url, domain=self._domain)
        if sku is None:
            raise Exception('[{}] SKU cannot be extracted from url - {}'.format(self._job_id, self._url))
        try:
            self._item = Item.objects.get(domain=self._domain, sku=sku)
        except Item.DoesNotExist:
            # create new item
            self._item = Item.objects.create(domain=self._domain,
                        sku=sku,
                        parent_sku=self._data['parent_asin'],
                        upc=None,
                        title=self._data['title'],
                        brand_name=self._data.get('brand_name', None),
                        picture_url=self._data.get('picture_urls', [])[0] if len(self._data.get('picture_urls', [])) > 0 else None,
                    )
        self._item_price = ItemPrice.objects.create(domain=self._domain,
                        job_id=self._job_id,
                        sku=sku,
                        price=self._data['price'],
                        original_price=self._data.get('original_price', self._data['price']),
                        online_availability=ItemPrice.ITEM_PRICE_AVAILABILITY_IN_STOCK if self._data['quantity'] > 0 else ItemPrice.ITEM_PRICE_AVAILABILITY_OUT_OF_STOCK,
                        online_urgent_quantity=self._data['quantity'] if self._data['quantity'] > 0 and self._data['quantity'] < 100 else None,
                        store_availabilities=None,
                    )

    def _build_walmart_com_item_price(self):
        """ sku: data['item']['product']['buyBox']['primaryUsItemId']
            upc: data['item']['product']['buyBox']['products'][0]['upc']
            title: data['item']['product']['buyBox']['products'][0]['productName']
            brand: data['item']['product']['buyBox']['products'][0]['brandName']
            picture_url: data['item']['product']['buyBox']['products'][0]['images'][0]['url']

            price:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['currentPrice']
                    return truncatechars(str(prices), 50)
            original_price: same as price
            online_availability:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['gmAvailability'] [ Available or not]
                    return truncatechars(str(prices), 50)
            online_urgent_quantity:
                if 'skus' in self.data and 'offers' in self.data:
                    prices = {}
                    for sku, offerid in self.data['skus'].items():
                        if len(offerid) < 1:
                            continue
                        prices[sku] = self.data['offers'][offerid[0]]['availableQuantity']
                    return truncatechars(str(prices), 50)
            store_availabilities: data['item']['product']['buyBox']['products'][0]['pickupOptions']
        """
        sku = utils.extract_sku_from_url(url=self._url, domain=self._domain)
        if sku is None:
            raise Exception('[{}] SKU cannot be extracted from url - {}'.format(self._job_id, self._url))
        # todo: need to have better exception handling if this key missing in data (i.e. email me...)
        _product_info = self._data['item']['product']['buyBox']['products'][0]
        try:
            self._item = Item.objects.get(domain=self._domain, sku=sku)
        except Item.DoesNotExist:
            # create new item
            self._item = Item.objects.create(domain=self._domain,
                        sku=sku,
                        parent_sku=self._data['item']['product']['buyBox']['primaryUsItemId'],
                        upc=_product_info['upc'],
                        title=_product_info['productName'],
                        brand_name=_product_info['brandName'],
                        picture_url=_product_info['images'][0]['url'] if len(_product_info['images']) > 0 and 'url' in _product_info['images'][0] else None,
                    )
        # generate store_availabilities json
        store_availabilities = []
        if 'pickupOptions' in _product_info and len(_product_info['pickupOptions']) > 0:
            for s in _product_info['pickupOptions']:
                store_availabilities.append({
                    'store_id': str(s.get('storeId')),
                    'store_name': s.get('storeName'),
                    'store_address': s.get('storeAddress'),
                    'store_city': s.get('storeCity'),
                    'store_state_or_province': s.get('storeStateOrProvinceCode'),
                    'store_postal_code': s.get('storePostalCode'),
                    'store_phone': s.get('storePhone'),
                    'store_availability': ItemPrice.ITEM_PRICE_AVAILABILITY_IN_STOCK if s.get('availability') == 'AVAILABLE' else ItemPrice.ITEM_PRICE_AVAILABILITY_OUT_OF_STOCK,
                    'store_urgent_quantity': s.get('urgentQuantity', 0) if s.get('urgentQuantity', 0) > 0 else None,
                })
        _price = _product_info.get('priceMap', {}).get('price')
        self._item_price = ItemPrice.objects.create(domain=self._domain,
                        job_id=self._job_id,
                        sku=sku,
                        price=_price,
                        original_price=_product_info.get('priceMap', {}).get('wasPrice', _price),
                        online_availability=ItemPrice.ITEM_PRICE_AVAILABILITY_IN_STOCK if _product_info['availabilityStatus'] == 'IN_STOCK' else ItemPrice.ITEM_PRICE_AVAILABILITY_OUT_OF_STOCK,
                        online_urgent_quantity=_product_info.get('urgentQuantity'),
                        store_availabilities=store_availabilities if len(store_availabilities) > 0 else None,
                    )


    def _build_canadiantire_ca_item_price(self):
        pass

# class AmazonParentListing(models.Model):
#     parent_asin = models.CharField(max_length=32, db_index=True)
#     domain = models.CharField(max_length=32, db_index=True)
#     asins = ArrayField(
#         base_field=models.CharField(max_length=32, blank=True, null=True), blank=True,
#         null=True)
#     review_count = models.SmallIntegerField(blank=True, null=True, default=0)
#     avg_rating = models.FloatField(blank=True, null=True, default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.parent_asin

#     class Meta:
#         db_table = 'resrc_amazon_parent_listings'
#         constraints = [
#             models.UniqueConstraint(fields=['parent_asin', 'domain'],name='unique_parent_asin_domain')
#         ]


# class AmazonListing(models.Model):
#     asin = models.CharField(max_length=32, db_index=True)
#     domain = models.CharField(max_length=32, db_index=True)
#     parent_asin = models.CharField(max_length=32, db_index=True)
#     picture_urls = ArrayField(
#         base_field=models.CharField(
#             max_length=255, blank=True, null=True),
#         null=True)
#     url = models.TextField()
#     category = models.CharField(max_length=255, blank=True, null=True)
#     title = models.TextField()
#     price = models.DecimalField(max_digits=15, decimal_places=2)
#     original_price = models.DecimalField(max_digits=15, decimal_places=2)
#     quantity = models.SmallIntegerField(blank=True, null=True, default=0)
#     features = models.TextField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     specifications = models.TextField(blank=True, null=True)
#     variation_specifics = models.CharField(max_length=255, blank=True, null=True)
#     is_fba = models.BooleanField(default=0)
#     is_addon = models.BooleanField(default=0)
#     is_pantry = models.BooleanField(default=0)
#     has_sizechart = models.BooleanField(default=0)
#     international_shipping = models.BooleanField(default=0)
#     merchant_id = models.CharField(max_length=32, blank=True, null=True)
#     merchant_name = models.CharField(max_length=100, blank=True, null=True)
#     brand_name = models.CharField(max_length=100, blank=True, null=True)
#     meta_title = models.TextField(blank=True, null=True)
#     meta_description = models.TextField(blank=True, null=True)
#     meta_keywords = models.TextField(blank=True, null=True)
#     status = models.SmallIntegerField(blank=True, null=True, default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return "[{}] {}".format(self.asin, self.title)

#     def save(self, *args, **kwargs):
#         try:
#             super().save(*args, **kwargs)
#         except ValueError as ve:
#             raise ve
#         except Exception as e:
#             raise e
#         # insert new price, original_price
#         self._save_listing_price()

#     def _save_listing_price(self):
#         new_listing_price = AmazonListingPrice()
#         new_listing_price.asin = self.asin
#         new_listing_price.domain = self.domain
#         new_listing_price.price = self.price
#         new_listing_price.original_price = self.original_price
#         new_listing_price.save()

#     class Meta:
#         db_table = 'resrc_amazon_listings'
#         constraints = [
#             models.UniqueConstraint(fields=['asin', 'domain'],name='unique_asin_domain')
#         ]


# class AmazonListingPrice(models.Model):
#     asin = models.CharField(max_length=32, db_index=True)
#     domain = models.CharField(max_length=32, db_index=True)
#     price = models.DecimalField(max_digits=15, decimal_places=2)
#     original_price = models.DecimalField(max_digits=15, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "{}".format(self.asin)

#     class Meta:
#         db_table = 'resrc_amazon_listing_prices'
#         constraints = [
#             models.UniqueConstraint(fields=['asin', 'domain'],name='unique_asin_price_domain')
#         ]
