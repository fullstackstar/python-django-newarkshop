"""Defines url patterns for users."""

from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
    # Login page.
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registerAsConsumer/', views.register_consumer_view, name='registerAsConsumer'),
    path('registerAsVendor/', views.register_vendor_view, name='registerAsVendor'),
]
