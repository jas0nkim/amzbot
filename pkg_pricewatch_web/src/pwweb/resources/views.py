from django.http import Http404
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from pwweb.mixins import MultipleFieldLookupMixin
from pwweb.resources.serializers import *
from pwweb.resources.models import RawData, Item, ItemPrice, BuildItemPrice, BuildWalmartCaItemPrice, BuildCanadiantireCaItemPrice


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
        response_code = status.HTTP_201_CREATED
        response_data = {'status': 'ok'}
        error_message = ''
        if job_id:
            for _d in RawData.objects.filter(job_id=job_id):
                if _d.domain in ['amazon.com', 'amazon.ca', 'walmart.com',]:
                    try:
                        BuildItemPrice(_d)
                    except Exception as e:
                        response_code = status.HTTP_400_BAD_REQUEST
                        error_message += '[{}] {}'.format(_d.url, str(e))
        if response_code != status.HTTP_201_CREATED:
            response_data = {'error_message': '[{}] error on building item price - {}'.format(job_id, error_message)}
        return Response(response_data, status=response_code)


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

