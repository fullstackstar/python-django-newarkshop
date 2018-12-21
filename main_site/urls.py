from django.urls import path, re_path

from . import views

app_name = 'main_site'

urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    path('vendor/dashboard', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/transactions', views.vendor_transactions, name='vendor_transactions'),
    # path('vendor/transactions/accept/<int:transaction_id>', views.vendor_accept, name='vendor_accept'),
    re_path(r'^vendor/transactions/accept/(?P<transaction_id>\d+)$', views.vendor_accept, name='vendor_accept'),
    path('consumer/dashboard', views.consumer_dashboard, name='consumer_dashboard'),
    path('consumer/vendors', views.vendors, name='consumer_purchase'),
    path('consumer/vendors/<int:vendor_id>', views.vendor, name='vendor'),
]
