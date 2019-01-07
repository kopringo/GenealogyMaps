
from django.urls import path, re_path
from django.conf.urls import url, include
from . import views
from . import views_parts

from . import urls_api

urlpatterns = [

    path('api2/', include(urls_api.router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('contact', views.contact),

    path('', views.home, name='home'),
    path('parts/root', views_parts.root, name='parts_root'),
    path('parts/area', views_parts.area, name='parts_area')
]
