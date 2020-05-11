from django.http import Http404
from rest_framework import viewsets, generics
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from pwweb.mixins import MultipleFieldLookupMixin
from pwweb.resources.serializers import *


class RawDataListCreate(generics.ListCreateAPIView):
    queryset = RawData.objects.all()
    serializer_class = RawDataSerializer
    # permission_classes = [IsAdminUser]

    # def post(self, request, *args, **kwargs):
    #     """ handle create on post method
    #     """
    #     return self.update(request, *args, **kwargs)


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

