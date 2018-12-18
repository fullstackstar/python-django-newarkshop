from django.contrib import admin
from .models import UserProfileInfo, UserPaymentInfo

admin.site.register(UserProfileInfo)
admin.site.register(UserPaymentInfo)
