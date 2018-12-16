from django.urls import path

from . import views

app_name = 'main_site'

urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
]
