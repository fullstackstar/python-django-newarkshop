from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # path('', views.PaymentPageView.as_view(), name='payment'),
    path('', views.home, name='payment'),
    path('charge/', views.charge, name='charge')
]
