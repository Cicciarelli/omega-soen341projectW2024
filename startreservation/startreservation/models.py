from django.db import models

# Create your models here.
class vehicles(models.Model):
    vehicle_id = models.IntegerField()

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

class Reservation(models.Model):
    Reservation_number = models.CharField(max_length=255)
