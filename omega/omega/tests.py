from django.test import TestCase, Client
from .models import  Reservation, vehicles
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import redirect
from . import views
from django.urls import reverse
import random

class TestExample(TestCase):
    def test_example(self):
        self.assertTrue(1==1)

class ReservationTest(TestCase):
    def test_create_reservation_with_valid_inputs(self):
        vehicle = vehicles.objects.create(vehicle_id=0)
        account = User.objects.create(username='test_user')
        reservation_start = datetime.now()
        reservation_end = reservation_start + timedelta(hours=1)
    
        reservation = Reservation(vehicle=vehicle, account=account, reservation_start=reservation_start, reservation_end=reservation_end)
        self.assertIsInstance(reservation, Reservation)