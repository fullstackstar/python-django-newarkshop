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

    path('register/consumer/stepOne', views.register_step_one, name='registerConsumerStepOne'),
    path('register/consumer/stepTwo', views.register_step_two, name='registerConsumerStepTwo'),
    path('register/consumer/stepThree', views.register_step_four, name='registerConsumerStepThree'),

    path('register/vendor/stepOne', views.register_step_one, name='registerVendorStepOne'),
    path('register/vendor/stepTwo', views.register_step_two, name='registerVendorStepTwo'),
    path('register/vendor/stepThree', views.register_step_three, name='registerVendorStepThree'),
    path('register/vendor/stepFour', views.register_step_four, name='registerVendorStepFour'),
]
