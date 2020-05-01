from rest_framework import viewsets
from pwweb.schedules.models import Job, Version
from pwweb.schedules.serializers import JobSerializer, VersionSerializer


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

