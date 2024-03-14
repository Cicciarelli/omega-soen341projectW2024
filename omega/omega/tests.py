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
from django.contrib.auth import get_user_model

class TestExample(TestCase):
    def test_example(self):
        self.assertTrue(1==1)

class ReservationTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='testuser', email='me@me.me', password='testpassword'
        )
        
        # Create a vehicle for testing
        self.vehicle = vehicles.objects.create(vehicle_id=0)

        self.test_date = datetime.now()
        
        # Create a reservation for testing
        self.reservation = Reservation.objects.create(
            vehicle=self.vehicle,
            account=self.user,
            reservation_start=datetime.now(),
            reservation_end = self.test_date + timedelta(hours=1)
        )

    def test_create_reservation_created(self):
        self.assertEqual(self.reservation.vehicle, self.vehicle)
        self.assertEqual(self.reservation.account, self.user)
        self.assertEqual(self.reservation.reservation_start, self.test_date)
        self.assertEqual(self.reservation.reservation_end, self.test_date + timedelta(hours=1))

    def test_vehicle_deletion_protected(self):
        # Try to delete the vehicle
        with self.assertRaises(Exception):
            self.vehicle.delete()

    def test_user_deletion_cascades(self):
        # Delete the user
        self.user.delete()
        # Check that the reservation is also deleted
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())