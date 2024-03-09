from django.contrib import admin
from .models import Member
from .models import Reservation

admin.site.register(Member)
admin.site.register(Reservation)
