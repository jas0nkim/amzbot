from rest_framework import viewsets, generics
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from pwweb.schedules.models import Job, Version
from pwweb.schedules.serializers import JobSerializer, VersionSerializer
from pwweb.mixins import MultipleFieldLookupMixin


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


# class VersionViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.

#     Additionally we also provide an extra `highlight` action.
#     """
#     queryset = Version.objects.all()
#     serializer_class = VersionSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#     #                       IsOwnerOrReadOnly]


class VersionList(CreateModelMixin, UpdateModelMixin, generics.ListAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    # permission_classes = [IsAdminUser]
    # lookup_fields = ['project', 'version']

    _instance = None

    def get_object(self):
        """
        override rest_framework.generics.GenericAPIView.get_object()
        workaround using two lookup fields ('project', 'version') instead of 'pk' field on fetching
        """
        return self._instance

    def post(self, request, *args, **kwargs):
        """ handle both create and update on post method
        """
        try:
            self._instance = Version.objects.get(project=request.data.get('project'),
                version=request.data.get('version'))
        except Version.DoesNotExist:
            # create
            return self.create(request, *args, **kwargs)
        else:
            # update
            return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class VersionDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    # permission_classes = [IsAdminUser]
    lookup_fields = ['project', 'version']
