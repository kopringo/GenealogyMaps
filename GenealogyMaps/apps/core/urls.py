
from django.urls import path
from django.conf.urls import url, include
from . import views
from . import views_api

from .urls_api import router

urlpatterns = [
    #path('api/parishes', views_api.parishes__get),
    url('api2', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.home)
]
