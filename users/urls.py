"""Defines url patterns for users."""

from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm
from django.urls import reverse_lazy
from django.conf import settings

app_name = 'users'

urlpatterns = [
    # Login page.
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html', authentication_form=LoginForm
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('register/consumer/stepOne', views.register_step_one, name='registerConsumerStepOne'),
    path('register/consumer/stepTwo', views.register_step_two, name='registerConsumerStepTwo'),
    path('register/consumer/stepThree', views.register_step_four, name='registerConsumerStepThree'),

    path('register/vendor/stepOne', views.register_step_one, name='registerVendorStepOne'),
    path('register/vendor/stepTwo', views.register_step_two, name='registerVendorStepTwo'),
    path('register/vendor/stepThree', views.register_step_three, name='registerVendorStepThree'),
    path('register/vendor/stepFour', views.register_step_four, name='registerVendorStepFour'),

    # re_path(r'^password_reset/$', views.password_reset_view, name='password_reset'),
    #re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #         views.password_reset_confirm, name='password_reset_confirm'),

    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        from_email=settings.DEFAULT_FROM_EMAIL,
        success_url=reverse_lazy('users:password_reset_done')
        ),
        name='password_reset'
    ),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='users/password_reset_confirm.html',
                success_url=reverse_lazy('users:password_reset_complete')
            ), name='password_reset_confirm'),
    re_path(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(
                template_name='users/password_reset_complete.html'
            ), name='password_reset_complete'),
]
