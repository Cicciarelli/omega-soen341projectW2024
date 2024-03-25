from django.db import models
from django.conf import settings

# Create your models here.
class Vehicle(models.Model):
  vehicle_vin = models.IntegerField()
  vehicle_make = models.CharField(max_length=255)
  vehicle_model = models.CharField(max_length=255)
  vehicle_year = models.CharField(max_length=255)
  vehicle_license_plate = models.CharField(max_length=255)
  vehicle_color = models.CharField(max_length=255)
  is_rented = models.BooleanField(null=False)

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

class Reservation(models.Model):
  vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT) # Stops you from deleting a vehicle without first deleting the reservation
  account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Deletes reservation if user account is deleted
  reservation_start = models.DateTimeField()
  reservation_end = models.DateTimeField()

  
