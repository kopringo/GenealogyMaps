
from django.urls import path, re_path
from django.conf.urls import url, include
from . import views

urlpatterns = [

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('contact', views.contact),
    path('accounts/profile', views.profile, name='accounts_profile'),

    path('', views.home, name='home'),
    path('parish/<int:parish_id>', views.parish, name='view_parish'),
    path('parish/<int:parish_id>/documents', views.documents, name='parish_documents'),
    path('parish/<int:parish_id>/add-document', views.document_add, name='parish_add_document'),

    path('parish/list.json', views.parish_list_json),

    # filtrowanie po obszarach
    path('area/diocese/<int:d_id>', views.diocese, name='view_diocese'),
    path('area/deanery/<int:d_id>', views.deanery, name='view_deanery'),
    path('area/province/<int:p_id>', views.province, name='view_province'),
    path('area/county/<int:c_id>', views.county, name='view_county'),


]
