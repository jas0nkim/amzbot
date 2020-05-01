from django.urls import include, path
from rest_framework.routers import DefaultRouter
from pwweb.resources import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('amazon_parent_listing', views.AmazonParentListingViewSet)
router.register('amazon_listing', views.AmazonListingViewSet)

urlpatterns = [
    path('amazon_listing_price/<str:asin>/<str:domain>/', views.AmazonListingPriceList.as_view()),
    path('', include(router.urls)),
]
