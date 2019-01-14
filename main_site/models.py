from django.db import models

from users.models import CustomUser

import datetime


class Transaction(models.Model):
    vendor = models.ForeignKey(CustomUser, related_name="transaction_vendor_id", on_delete=models.CASCADE)
    consumer = models.ForeignKey(CustomUser, related_name="transaction_consumer_id", on_delete=models.CASCADE)

    amount = models.CharField(max_length=50)
    purchased_date = models.DateTimeField(default=datetime.datetime.now())

    # business_name = models.CharField(max_length=100)
    # vendor_id = models.IntegerField()
    # consumer_id = models.IntegerField()

    # line_number = models.CharField(max_length=50, default='')
    # vendor_status = models.CharField(max_length=50, default="NotAccepted")
    # consumer_status = models.CharField(max_length=50, default="NotPurchased")
    # purchased_date = models.DateTimeField(default=datetime.datetime.now())
    # accepted_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.amount
