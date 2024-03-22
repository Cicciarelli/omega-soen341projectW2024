from django.test import TestCase, Client
from .models import  Reservation, Vehicle
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
        self.vehicle = Vehicle.objects.create(vehicle_vin=101)

        self.test_date = datetime.now()
        
        # Create a reservation for testing
        self.reservation = Reservation.objects.create(
            vehicle=self.vehicle,
            account=self.user,
            reservation_start=self.test_date,
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

class LogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))  # Assuming the URL name for logout is 'logout'
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue('_auth_user_id' not in self.client.session)  # Asserting user is logged out
        self.assertEqual(response.url, reverse('home'))  # Asserting redirection to the home page

    def tearDown(self):
        self.client.logout()
