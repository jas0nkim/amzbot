from django.urls import path
from pwweb.resources import views


urlpatterns = [
    path('raw_data/', views.RawDataListCreate.as_view()),
    path('build_item_prices/', views.ItemPricesBuild.as_view())
]
