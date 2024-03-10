from django.contrib import admin
from .models import Member, Reservation, vehicles

admin.site.register(Member)
admin.site.register(vehicles)
admin.site.register(Reservation)
