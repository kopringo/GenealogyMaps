
from django.contrib.auth import views as auth_view

from django.urls import path, re_path
from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from . import views, views_courts, views_account, views_search, views_admin, views_ajax, views_parish, views_area, views_tools

urlpatterns = [

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # strona glowna
    path('', views.home, name='home'),

    # filtrowanie po obszarach
    path('area/diocese/<int:d_id>', views_area.diocese, name='view_diocese'),
    path('area/deanery/<int:d_id>', views_area.deanery, name='view_deanery'),
    path('area/province/<int:p_id>', views_area.province, name='view_province'),
    path('area/county/<int:c_id>', views_area.county, name='view_county'),

    # wyszukiwarka
    path('search', views_search.index),

    # parafia
    path('parish/<int:parish_id>', views_parish.parish, name='view_parish'),
    path('parish/<int:parish_id>/documents', views_parish.documents, name='parish_documents'),
    path('parish/<int:parish_id>/add-document', views_parish.document_add, name='parish_add_document'),
    path('parish/<int:parish_id>/favourite', views_parish.parish_favourite, name='parish_favourite'),
    path('parish/<int:parish_id>/request-access', views_parish.parish_request_access, name='parish_request_access'),
    path('parish/<int:parish_id>/edit', views_parish.parish_edit),
    path('parish/<int:parish_id>/edit2', views_parish.parish_edit2),
    path('parish/<int:parish_id>/edit3', views_parish.parish_edit3),
    path('parish/<int:parish_id>/edit4', views_parish.parish_edit4),
    path('parish/<int:parish_id>/message', views_parish.parish_message),
    path('parish/list.json', views_parish.parish_list_json),

    # for admin
    path('a/users/<int:user_id>', views_admin.users_user),
    path('a/users', views_admin.users),
    path('a/parishes', views_admin.parishes),





    path('contact', views.contact),
    path('accounts/profile', views.profile, name='accounts_profile'),

    path('set', views.set_param, name='set_param'),



    path('courts', views_courts.index, name='view_courts_index'),
    path('courts/office/<int:o_id>', views_courts.office, name='view_courts_office'),
    path('courts/office/<int:o_id>/add-book', views_courts.court_add_book, name='view_courts_add_book'),
    path('courts/book/<int:b_id>', views_courts.book, name='view_courts_book'),

    path('ajax/sources', views_ajax.sources),
    path('ajax/parishes', views_ajax.parishes),

    path('accounts/login/', auth_view.LoginView.as_view(authentication_form=views_account.CustomAuthenticationForm), name='login'),
    path('accounts/logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', auth_view.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

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

    path('login-validation-required', views.validation_required),

    # narzedzia
    path('tools/names', views_tools.names),

]
