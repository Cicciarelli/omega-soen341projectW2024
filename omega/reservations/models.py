from django.db import models

# Create your models here.
class Reservation(models.Model):
    vehicle_id = models.ForeignKey('vehicles.Vehicle')
    reservation_start = models.DateTimeField()
    reservation_end = models.DateTimeField()
    reservation_price = models.DecimalField()