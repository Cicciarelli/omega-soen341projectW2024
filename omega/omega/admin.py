from django.contrib import admin
from .models import Member, Reservation, Vehicle

admin.site.register(Member)
admin.site.register(Vehicle)
admin.site.register(Reservation)
