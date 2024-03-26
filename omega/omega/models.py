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

  def __str__(self):
        return self.vehicle_license_plate

class Member(models.Model):
  account = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                   default=1)
  firstname = models.CharField(max_length=255, default='')
  lastname = models.CharField(max_length=255, default='')
  address = models.CharField(max_length=255, default='')
  drivers_license = models.CharField(max_length=255, default='')

class Location(models.Model):
  title = models.CharField(max_length=255)

  def __str__(self):
        return self.title

class Reservation(models.Model):
  vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT) # Stops you from deleting a vehicle without first deleting the reservation
  account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Deletes reservation if user account is deleted
  reservation_start = models.DateTimeField()
  reservation_end = models.DateTimeField()
  pick_up_location = models.ForeignKey(Location,
                                       related_name='pick_up_reservation',
                                       on_delete=models.CASCADE,
                                         default=None,
                                         blank=True,
                                         null=True)
  drop_off_location = models.ForeignKey(Location,
                                        related_name='drop_off_location',
                                        on_delete=models.CASCADE,
                                         default=None,
                                         blank=True,
                                         null=True)
  rental_period = models.DurationField(blank=True,
                                       null=True)
  mileage_limit = models.FloatField(blank=True,
                                    null=True)
  additional_services = models.CharField(max_length=255,
                                         default=None,
                                         blank=True,
                                         null=True)
  is_signed = models.BooleanField(default=False)

class PaymentInfo(models.Model):
   account = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
   card_number = models.IntegerField()
