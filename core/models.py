from django.db import models
from django.contrib.auth.models import User

class Bicycle(models.Model):
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)