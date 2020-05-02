from django.urls import path
from pwweb.resources import views


urlpatterns = [
    path('amazon_parent_listing/', views.AmazonParentListingList.as_view()),
    path('amazon_parent_listing/<str:parent_asin>/<str:domain>/',
        views.AmazonParentListingDetail.as_view()),
    path('amazon_listing/', views.AmazonListingList.as_view()),
    path('amazon_listing/<str:asin>/<str:domain>/',
        views.AmazonListingDetail.as_view()),
    path('amazon_listing_price/<str:asin>/<str:domain>/',
        views.AmazonListingPriceList.as_view()),
]
