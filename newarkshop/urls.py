from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_site.urls', namespace='main_site')),
    path('users/', include('users.urls', namespace='users')),
    path('payments/', include('payments.urls', namespace='payments')),
]
