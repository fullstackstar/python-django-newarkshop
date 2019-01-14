from django.urls import path, re_path

from . import views

app_name = 'main_site'

urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    path('admin/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin/dashboard/transactions', views.admin_transactions, name='admin_transactions'),
    path('admin/dashboard/users', views.admin_users, name='admin_users'),
    path('admin/dashboard/users/delete/(?P<user_id>\d+)$', views.admin_user_delete, name='admin_user_delete'),
    path('vendor/dashboard', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/dashboard/transaction', views.vendor_transactions, name='vendor_transactions'),
    path('vendor/dashboard/transaction/phone_verification', views.vendor_phone_verification, name='vendor_phone_verification'),
    path('vendor/dashboard/transaction/transaction/(?P<consumer_id>\d+)$', views.vendor_transaction, name='vendor_transaction'),
    # path('vendor/transactions/accept/<int:transaction_id>', views.vendor_accept, name='vendor_accept'),
    # re_path(r'^vendor/transactions/accept/(?P<transaction_id>\d+)$', views.vendor_accept, name='vendor_accept'),
    path('consumer/dashboard', views.consumer_dashboard, name='consumer_dashboard'),
    path('consumer/vendors', views.vendors, name='consumer_purchase'),
    path('consumer/vendors/<int:vendor_id>', views.vendor, name='vendor'),
]
