from rest_framework import viewsets, generics
from pwweb.schedules.models import Job, Version
from pwweb.schedules.serializers import JobSerializer, VersionSerializer
from pwweb.views import MultipleFieldLookupMixin


class JobViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class VersionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]


class VersionList(MultipleFieldLookupMixin, generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    # permission_classes = [IsAdminUser]
    lookup_fields = ['project', 'version']

    def post(self, request, *args, **kwargs):
        """ handle both create and update on post method
        """
        try:
            # update
            instance = self.get_object()
        except Exception:
            # create
            instance = None
        serializer = self.get_serializer(instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def put(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)


class VersionDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    # permission_classes = [IsAdminUser]
    lookup_fields = ['project', 'version']
