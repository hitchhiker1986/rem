from django.urls import path
# from django.conf.urls import url
from rem.views import *

app_name = 'rem'
urlpatterns = [
    # path('', index_view, name='index'),
    path('test/', test_view, name='test'),
    path('thanks/', thanks, name='thanks'),
    path('apartment_list/', apartment_list, name='apartment_list'),
    path('owner_list/', owner_list, name='owner_list'),
    path('tenant_list/', tenant_list, name='tenant_list'),
    path('tenant_modify/<int:user_id>', tenant_modify, name='tenant_modify'),
    path('utility_list/', utility_list, name='utility_list'),
    path('apartment/<int:apt_id>', apartment_show, name='apartment'),
    path('apartment/<int:apt_id>/details', apartment_details, name='apartment_details'),
    path('apartment/<int:apt_id>/owners', apartment_owners, name='apartment_owners'),
    path('apartment/<int:apt_id>/tenants', apartment_tenants, name='apartment_tenants'),
    path('apartment/<int:apt_id>/utilities', apartment_utilities, name='apartment_utilities'),
    path('apartment/<int:apt_id>/contracts', apartment_contracts, name='apartment_contracts'),
    path('apartment/<int:apt_id>/history', apartment_history, name='apartment_history'),
    path('apartment/<int:apt_id>/checkform', apartment_checkform, name='apartment_checkform'),
    path('apartment/<int:apt_id>/sent_contract_form', apartment_sent_contract_form, name='apartment_sent_contract_form'),
    path('checkform/<int:apt_id>', apartment_checkform, name='apartment_checkform' ),
    path('apartment/create', apartment_createform, name='apartment_createform'),
    path('tenant/<int:user_id>', tenant_show, name='tenant'),
    path('owner/<int:user_id>', owner_show, name='owner'),
    path('apartment/dict/<int:pk_id>', dict_form, name='dict'),
    path('dict_years/', dict_years, name='dict_years'),
    path('dict_list/<int:year>', dict_list, name='dict_list'),
    path('todo_list/', todo_list, name='todo_list'),
    path('payment_bill', payment_bill_view, name='payment_bill'),
    path('bill_form/<int:pb_id>', bill_form_view, name='bill_form'),
    path('create_util_form/', create_utility_form, name='create_utility_form'),
    path('todos/', todo_list, name='todo_list'),
    path('todos/todo_form/<int:pk_id>', task_show_and_modify, name='todo_form'),
    path('todos/create_task/', create_task, name='create_task'),
    # url(r'^dict/(?P<serial>[A-Za-z0-9]*)$', dict_form, name='dict'),
]
