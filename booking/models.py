from django.db import models
from django.contrib.auth.models import User
from event.models import *


# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ('paid','PAID'),
        ('unpaid','UNPAID')

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.IntegerField()
    payment_status = models.CharField(choices=STATUS_CHOICES, default='unpaid', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


