
from django.urls import path, re_path
from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from . import views, views_courts, views_account, views_search, views_admin

urlpatterns = [

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('contact', views.contact),
    path('accounts/profile', views.profile, name='accounts_profile'),

    path('', views.home, name='home'),
    path('parish/<int:parish_id>', views.parish, name='view_parish'),
    path('parish/<int:parish_id>/documents', views.documents, name='parish_documents'),
    path('parish/<int:parish_id>/add-document', views.document_add, name='parish_add_document'),
    path('parish/<int:parish_id>/favourite', views.parish_favourite, name='parish_favourite'),
    path('parish/<int:parish_id>/request-access', views.parish_request_access, name='parish_request_access'),

    path('parish/list.json', views.parish_list_json),

    # filtrowanie po obszarach
    path('area/diocese/<int:d_id>', views.diocese, name='view_diocese'),
    path('area/deanery/<int:d_id>', views.deanery, name='view_deanery'),
    path('area/province/<int:p_id>', views.province, name='view_province'),
    path('area/county/<int:c_id>', views.county, name='view_county'),

    path('courts', views_courts.index, name='view_courts_index'),
    path('courts/office/<int:o_id>', views_courts.office, name='view_courts_office'),
    path('courts/office/<int:o_id>/add-book', views_courts.court_add_book, name='view_courts_add_book'),
    path('courts/book/<int:b_id>', views_courts.book, name='view_courts_book'),

    path('search', views_search.index),

    # for admin
    path('a/users', views_admin.users),

    #path('accounts/register/', views_account.register),
    url(r'^accounts/register/$', views_account.RegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/register/closed/$',
        TemplateView.as_view(
            template_name='django_registration/registration_closed.html'
        ),
        name='registration_disallowed'),
    url(r'^accounts/register/complete/$',
        TemplateView.as_view(
            template_name='django_registration/registration_complete.html'
        ),
        name='registration_complete'),

]
