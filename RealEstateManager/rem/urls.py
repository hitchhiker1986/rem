from django.urls import path
# from django.conf.urls import url
from rem.views import *

app_name = 'rem'
urlpatterns = [
    # path('', index_view, name='index'),
    path('test/', test_view, name='test'),
    path('apartment_list/', apartment_list, name='apartment_list'),
    path('owner_list/', owner_list, name='owner_list'),
    path('tenant_list/', tenant_list, name='tenant_list'),
    path('utility_list/', utility_list, name='utility_list'),
    path('apartment/<int:apt_id>', apartment_show, name='apartment'),
    path('apartment/<int:apt_id>/details', apartment_details, name='apartment_details'),
    path('apartment/<int:apt_id>/owners', apartment_owners, name='apartment_owners'),
    path('apartment/<int:apt_id>/tenants', apartment_tenants, name='apartment_tenants'),
    path('apartment/<int:apt_id>/utilities', apartment_utilities, name='apartment_utilities'),
    path('apartment/<int:apt_id>/contracts', apartment_contracts, name='apartment_contracts'),
    path('apartment/<int:apt_id>/history', apartment_history, name='apartment_history'),
    path('tenant/<int:user_id>', tenant_show, name='tenant'),
    path('owner/<int:user_id>', owner_show, name='owner'),
    path('dict/<int:serial>', dict_form, name='dict'),
    path('dict_years/', dict_years, name='dict_years'),
    path('dict_list/<int:year>', dict_list, name='dict_list'),
    path('todo_list/', todo_list, name='todo_list'),
    # url(r'^dict/(?P<serial>[A-Za-z0-9]*)$', dict_form, name='dict'),
]
