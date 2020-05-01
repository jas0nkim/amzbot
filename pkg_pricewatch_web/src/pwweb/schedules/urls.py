from django.urls import include, path
from rest_framework.routers import DefaultRouter
from pwweb.schedules import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('job', views.JobViewSet)

urlpatterns = [
    path('version/<str:project>/<str:version>/', views.VersionDetail.as_view()),
    path('version/', views.VersionList.as_view()),
    path('', include(router.urls)),
]
