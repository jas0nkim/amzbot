from django.http import Http404
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from pwweb import settings, utils
from pwweb.mixins import MultipleFieldLookupMixin
from pwweb.resources.serializers import *
from pwweb.resources.models import RawData, Item, ItemPrice
from pwweb.resources.modelBuilders import BuildItemPrice, BuildWalmartCaItemPrice, BuildCanadiantireCaItemPrice


class RawDataListCreate(generics.ListCreateAPIView):
    queryset = RawData.objects.all()
    serializer_class = RawDataSerializer
    # permission_classes = [IsAdminUser]

    # def post(self, request, *args, **kwargs):
    #     """ handle create on post method
    #     """
    #     return self.update(request, *args, **kwargs)


class ItemPricesBuild(APIView):
    # permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        """ build item prices
        """
        job_id = request.data.get('job_id')
        response_code = status.HTTP_400_BAD_REQUEST
        response_data = {'status': 'ok'}
        error_message = ''
        if job_id:
            _bip_success, _bip_error_messages = self._build_item_price(job_id)
            _wcabip_success, _wcabip_error_messages = self._build_walmart_ca_item_price(job_id)
            _ccabip_success, _ccabip_error_messages = self._build_canadiantire_ca_item_price(job_id)
            response_code = status.HTTP_201_CREATED if _bip_success and _wcabip_success and _ccabip_success else response_code
            error_message = '\n'.join(_bip_error_messages + _wcabip_error_messages + _ccabip_error_messages)
        if response_code != status.HTTP_201_CREATED:
            response_data = {'error_message': '[{}] error on building item price - {}'.format(job_id, error_message)}
        return Response(response_data, status=response_code)

    def _build_item_price(self, job_id):
        success = True
        error_messages = []
        for _raw in RawData.objects.filter(job_id=job_id, domain__in=['amazon.com', 'amazon.ca', 'walmart.com',], http_status__lt=400):
            try:
                BuildItemPrice(_raw)
            except Exception as e:
                success = False
                error_messages.append('[{}] {}'.format(_raw.url, str(e)))
        return (success, error_messages)

    def _build_walmart_ca_item_price(self, job_id):
        success = True
        error_messages = []
        _q = RawData.objects.filter(job_id=job_id, domain='walmart.ca', http_status__lt=400)
        # get base raw
        for _base_raw in _q.filter(url__regex=settings.WALMART_CA_ITEM_LINK_PATTERN):
            _parent_sku = utils.extract_sku_from_url(url=_base_raw.url, domain='walmart.ca')
            # get price_raw
            for link_format in settings.WALMART_CA_API_ITEM_PRICE_LINK_FORMATS:
                try:
                    _price_raw = _q.get(url=link_format.format(_parent_sku))
                except RawData.DoesNotExist:
                    continue
                else:
                    break
            # get stores_raw
            _stores_raw = {}
            for _s_raw in _q.filter(url__startswith=settings.WALMART_CA_API_ITEM_FIND_IN_STORE_LINK,
                                        url__endswith='#{}'.format(_parent_sku)):
                _upc = utils.extract_upc_from_walmart_ca_url(_s_raw.url)
                _stores_raw[_upc] = _s_raw
            try:
                BuildWalmartCaItemPrice(raw_data=_base_raw, price_raw_data=_price_raw, stores_raw_data=_stores_raw)
            except Exception as e:
                success = False
                error_messages.append('[{}] {}'.format(_base_raw.url, str(e)))
        return (success, error_messages)

    def _build_canadiantire_ca_item_price(self, job_id):
        success = True
        error_messages = []
        _q = RawData.objects.filter(job_id=job_id, domain='canadiantire.ca', http_status__lt=400)
        # get base raw
        for _base_raw in _q.filter(url__regex=settings.CANADIANTIRE_CA_ITEM_LINK_PATTERN):
            _sku = utils.extract_sku_from_url(url=_base_raw.url, domain='canadiantire.ca')
            _parent_sku = _base_raw.data.get('SkuSelectors', {}).get('pCode', '{}P'.format(_sku))
            # get store_raw
            _store_raw = _q.get(url__startswith=settings.CANADIANTIRE_CA_API_STORES_LINK, url__iendswith='#{}'.format(_parent_sku))
            # get price_raw
            _price_raw = _q.get(url__startswith=settings.CANADIANTIRE_CA_API_ITEM_PRICE_LINK, url__iendswith='#{}'.format(_parent_sku))
            try:
                BuildCanadiantireCaItemPrice(raw_data=_base_raw, store_raw_data=_store_raw, price_raw_data=_price_raw)
            except Exception as e:
                success = False
                error_messages.append('[{}] {}'.format(_base_raw.url, str(e)))
        return (success, error_messages)


# class AmazonParentListingList(CreateModelMixin, UpdateModelMixin, generics.ListAPIView):
#     queryset = AmazonParentListing.objects.all()
#     serializer_class = AmazonParentListingSerializer
#     # permission_classes = [IsAdminUser]

#     _instance = None

#     def get_object(self):
#         """
#         override rest_framework.generics.GenericAPIView.get_object()
#         workaround using two lookup fields ('parent_asin', 'domain') instead of 'pk' field on fetching
#         """
#         return self._instance

#     def post(self, request, *args, **kwargs):
#         """ handle both create and update on post method
#         """
#         try:
#             self._instance = AmazonParentListing.objects.get(parent_asin=request.data.get('parent_asin'),
#                 domain=request.data.get('domain'))
#         except AmazonParentListing.DoesNotExist:
#             # create
#             return self.create(request, *args, **kwargs)
#         else:
#             # update
#             return self.update(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


# class AmazonParentListingDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
#     queryset = AmazonParentListing.objects.all()
#     serializer_class = AmazonParentListingSerializer
#     # permission_classes = [IsAdminUser]
#     lookup_fields = ['parent_asin', 'domain']


# class AmazonListingList(CreateModelMixin, UpdateModelMixin, generics.ListAPIView):
#     queryset = AmazonListing.objects.all()
#     serializer_class = AmazonListingSerializer
#     # permission_classes = [IsAdminUser]

#     _instance = None

#     def get_object(self):
#         """
#         override rest_framework.generics.GenericAPIView.get_object()
#         workaround using two lookup fields ('asin', 'domain') instead of 'pk' field on fetching
#         """
#         return self._instance

#     def post(self, request, *args, **kwargs):
#         """ handle both create and update on post method
#         """
#         try:
#             self._instance = AmazonListing.objects.get(asin=request.data.get('asin'),
#                 domain=request.data.get('domain'))
#         except AmazonListing.DoesNotExist:
#             # create
#             return self.create(request, *args, **kwargs)
#         else:
#             # update
#             return self.update(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)


# class AmazonListingDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
#     queryset = AmazonListing.objects.all()
#     serializer_class = AmazonListingSerializer
#     # permission_classes = [IsAdminUser]
#     lookup_fields = ['asin', 'domain']


# class AmazonListingPriceList(MultipleFieldLookupMixin, generics.ListAPIView):
#     queryset = AmazonListingPrice.objects.all()
#     serializer_class = AmazonListingPriceSerializer
#     # permission_classes = [IsAdminUser]
#     lookup_fields = ['asin', 'domain']

#     # def post(self, request, *args, **kwargs):
#     #     """ either create or update
#     #     """

#     #     try:
#     #         # update
#     #         instance = self.get_object()
#     #     except Exception:
#     #         # create
#     #         instance = None
#     #     serializer = self.get_serializer(instance=instance)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()

