from django.db import models

# Create your models here.
class vehicles(models.Model):
    vehicle_id = models.IntegerField()

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

class Reservation(models.Model):
    vehicle_id = models.ForeignKey(vehicles, on_delete=models.PROTECT) # Stops you from deleting a vehicle without first deleting the reservation
    reservation_start = models.DateTimeField()
    reservation_end = models.DateTimeField()
    reservation_price = models.DecimalField(decimal_places = 2, max_digits = 10)