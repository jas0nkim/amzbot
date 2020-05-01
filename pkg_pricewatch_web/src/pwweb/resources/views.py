from rest_framework import viewsets, generics
from pwweb.resources.models import AmazonParentListing, AmazonListing, AmazonListingPrice
from pwweb.resources.serializers import AmazonParentListingSerializer, AmazonListingSerializer, AmazonListingPriceSerializer
from pwweb.views import MultipleFieldLookupMixin

class AmazonParentListingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = AmazonParentListing.objects.all()
    serializer_class = AmazonParentListingSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class AmazonListingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = AmazonListing.objects.all()
    serializer_class = AmazonListingSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


# class AmazonListingPriceViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.

#     Additionally we also provide an extra `highlight` action.
#     """
#     queryset = AmazonListingPrice.objects.all()
#     serializer_class = AmazonListingPriceSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#     #                       IsOwnerOrReadOnly]


class AmazonListingPriceList(MultipleFieldLookupMixin, generics.ListAPIView):
    queryset = AmazonListingPrice.objects.all()
    serializer_class = AmazonListingPriceSerializer
    # permission_classes = [IsAdminUser]
    lookup_fields = ['asin', 'domain']

    # def post(self, request, *args, **kwargs):
    #     """ either create or update
    #     """

    #     try:
    #         # update
    #         instance = self.get_object()
    #     except Exception:
    #         # create
    #         instance = None
    #     serializer = self.get_serializer(instance=instance)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
