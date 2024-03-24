from django.db import models
from django.conf import settings

# Create your models here.
class vehicles(models.Model):
  vehicle_id = models.IntegerField()

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

class Reservation(models.Model):
  vehicle = models.ForeignKey(vehicles, on_delete=models.PROTECT) # Stops you from deleting a vehicle without first deleting the reservation
  account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Deletes reservation if user account is deleted
  reservation_start = models.DateTimeField()
  reservation_end = models.DateTimeField()

class SignatureModel(models.Model):
    signature = JSignatureField()