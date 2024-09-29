from django.db import models
from user.models import CustomUser

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.CharField(max_length=255)
    booking_date = models.DateTimeField()
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"{self.user.email} - {self.service}"
