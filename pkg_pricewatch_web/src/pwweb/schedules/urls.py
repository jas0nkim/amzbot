from django.urls import include, path
from rest_framework.routers import DefaultRouter
from pwweb.schedules import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('job', views.JobViewSet)
router.register('version', views.VersionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
