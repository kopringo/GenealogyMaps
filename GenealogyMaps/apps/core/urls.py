
from django.urls import path, re_path
from django.conf.urls import url, include
from . import views
from . import views_api

from . import urls_api

urlpatterns = [
    #path('api/parishes', views_api.parishes__get),
    #re_path(r'^api2/', include(urls_api)),
    path('api2/', include(urls_api.router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.home)
]
