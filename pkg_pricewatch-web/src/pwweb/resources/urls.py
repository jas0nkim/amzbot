from django.urls import include, path
from rest_framework.routers import DefaultRouter
from pwweb.resources import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('amazon_parent_listing', views.AmazonParentListingViewSet)
router.register('amazon_listing', views.AmazonListingViewSet)
router.register('amazon_listing_price', views.AmazonListingPriceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
