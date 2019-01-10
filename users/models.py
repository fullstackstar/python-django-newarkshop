from django.db import models
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10, default='consumer')


class UserProfileInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    business_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address_line_one = models.CharField(max_length=50)
    address_line_two = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50)
    st = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    # of_employees = models.BooleanField(default=False)
    of_employees = models.CharField(max_length=50, null=True)
    company = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class UserPaymentInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    pay_amount = models.CharField(max_length=10, blank=True)
    card_number = models.CharField(max_length=50)
    exp_date = models.DateField(blank=True)
    cvv = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
