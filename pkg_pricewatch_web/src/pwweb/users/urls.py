from django.urls import include, path
from rest_framework.routers import DefaultRouter
from pwweb.users import views

router = DefaultRouter()
router.register('product', views.UserProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
