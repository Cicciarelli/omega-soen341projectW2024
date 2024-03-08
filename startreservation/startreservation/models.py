from django.db import models

# Create your models here.
class vehicles(models.Model):
    vehicle_id = models.IntegerField()

class Reservation(models.Model):
  Number = models.CharField(max_length=255)
  
