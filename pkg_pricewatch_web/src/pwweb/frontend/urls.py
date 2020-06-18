from django.urls import path
from pwweb.frontend import views


urlpatterns = [
    path('', views.index, name='home'),
    path('pw/', views.pricewatching, name='pw_home'),
]
