from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, ReservationSignatureForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Reservation, vehicles
from .forms import ReservationForm
from datetime import datetime, timedelta
from django.contrib.auth import logout
import random
from .decorators import login_required_redirect
from django.http import Http404
from .forms import UserCreationFormWithEmail

@login_required_redirect
def my_view(request):
    return render(request, 'startReservation.html')

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
        form = UserCreationFormWithEmail(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,
                                password=raw_password,
                                email = email)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationFormWithEmail()
    return render(request, 'signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def delete_reservation(request, reservation_id):
    item = get_object_or_404(Reservation, pk=reservation_id)
    item.delete()

    return redirect('reservations')

@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

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
def check_in(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    # Write your view code here
    raise Http404

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

@login_required_redirect
def rental_agreement_view(request, reservation_id):
    return render(request, 'rental_agreement.html')

@login_required_redirect
def rental_agreement_signature_view(request):
    if request.method == 'POST':
        form = ReservationSignatureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations')
    else:
        form = ReservationSignatureForm()
    return render(request, 'rental_agreement.html', {'form': form})

def vehicle_view(request):
    return render(request, 'Addvehicle.html')

@login_required_redirect
def reservations_view(request) -> HttpResponse:
    return render(request, 'reservations.html')

@login_required_redirect
def startres_view(request):
    return render(request, 'startReservation.html')

@login_required_redirect
def economy_view(request):
    return render(request, 'economyReservation.html')

@login_required_redirect
def luxury_view(request):
    if request.method == 'POST':
        car_name = request.POST.get('convertibleCarDropdown')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Get the selected vehicle from the database
        vehicle = vehicles.objects.get(name=car_name)

        # Create a new reservation
        reservation = Reservation.objects.create(vehicle=vehicle, account=request.user, reservation_start=start_date, reservation_end=end_date)

        # Optionally, you can redirect the user to a success page or render a template
        return render(request, 'reservations.html', {'reservation': reservation})

    return render(request, 'luxuryReservation.html')  # Render the reservation form template

@login_required_redirect
def convertible_view(request):
    return render(request, 'convertibleReservation.html')

def findabranch_view(request):
    return render(request, 'findABranch.html')

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

