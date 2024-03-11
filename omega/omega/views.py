from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Reservation, vehicles
from .forms import ReservationForm
from datetime import datetime, timedelta
import random
def my_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or home page
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.password = form.cleaned_data.get('password')
            form.save()
            # Redirect to the home page or any other page after successful sign-up
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def delete_reservation(request, reservation_id):
    item = get_object_or_404(Reservation, pk=reservation_id)
    item.delete()

    return redirect('reservations')

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'edit_reservation.html', {'form': form})

@login_required
def generate_random_reservation(request):
    user = request.user
    available_vehicles = vehicles.objects.all()
    if available_vehicles.exists():
        random_vehicle = random.choice(available_vehicles)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=random.randint(1, 7))
        Reservation.objects.create(vehicle=random_vehicle, account=user, reservation_start=start_date, reservation_end=end_date)
    return redirect('reservations')

def reservations_view(request) -> HttpResponse:
    return render(request, 'reservations.html')

def startres_view(request):
    return render(request, 'startReservation.html')

def economy_view(request):
    return render(request, 'economyReservation.html')

def luxury_view(request):
    return render(request, 'luxuryReservation.html')

def convertible_view(request):
    return render(request, 'convertibleReservation.html')
    
def OMEGACarList(request):
    return render(request, 'OMEGACarList.html')

def toyota_corolla(request):
    return render(request, 'ToyotaCorolla.html')

def honda_civic(request):
    return render(request, 'HondaCivic.html')

def chevrolet_volt(request):
    return render(request, 'ChevroletVolt.html')

def toyota_prius(request):
    return render(request, 'ToyotaPrius.html')

def kia_niro(request):
    return render(request, 'KiaNiro.html')

def ford_mustang(request):
    return render(request, 'FordMustang.html')

def audi_a5(request):
    return render(request, 'AudiA5.html')

def bmw_m4(request):
    return render(request, 'BMWM4.html')

def chevrolet_corvette(request):
    return render(request, 'ChevroletCorvette.html')

def porsche_911(request):
    return render(request, 'Porsche911.html')

def audi_a4(request):
    return render(request, 'AudiA4.html')

def ferrari_roma(request):
    return render(request, 'FerrariRoma.html')

def bentley_bentayga(request):
    return render(request, 'BentleyBentayga.html')
