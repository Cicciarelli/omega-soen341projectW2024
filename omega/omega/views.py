from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, SignatureForm, RentalAgreementSetupForm, ReviewForm, PostForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Reservation, Vehicle, Location, Member, Review, ForumPost
from .forms import ReservationForm
from datetime import datetime, timedelta
from django.contrib.auth import logout
import random
from .decorators import login_required_redirect
from django.http import Http404
from .forms import UserCreationFormWithEmail
from django.urls import reverse
from django.db.models import Avg

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

def rental_setup_view(request, reservation_id):
    if request.method == 'POST':
        form = RentalAgreementSetupForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            driving_license = form.cleaned_data['driving_license']
            contact_number = form.cleaned_data['contact_number']
            
            url = reverse('rental_agreement', kwargs={'reservation_id': reservation_id,
                                                       'address': address,
                                                       'driving_license': driving_license,
                                                       'contact_number': contact_number})
            return redirect(url)
    else:
        form = RentalAgreementSetupForm()
    return render(request, 'rental_setup.html', {'form': form})

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
    available_vehicles = Vehicle.objects.all()
    branch_offices = Location.objects.all()
    if available_vehicles.exists():
        random_vehicle = random.choice(available_vehicles)
        start_date = datetime.now()
        pick_up_location = random.choice(branch_offices)
        drop_off_location = random.choice(branch_offices)
        end_date = start_date + timedelta(days=random.randint(1, 7))
        mileage_limit = random.randint(100, 700)
        Reservation.objects.create(vehicle=random_vehicle,
                                   account=user,
                                   reservation_start=start_date,
                                   reservation_end=end_date,
                                   pick_up_location=pick_up_location,
                                   drop_off_location=drop_off_location,
                                   mileage_limit=mileage_limit,
                                   additional_services = "")
    return redirect('reservations')

def rental_agreement_view(request, reservation_id, address, driving_license, contact_number):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == 'POST':
        form = SignatureForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('reservations')
    else:
        form = SignatureForm()
    return render(request, 'rental_agreement.html', {'form': form,
                                                     'reservation_id': reservation_id,
                                                     'reservation': reservation,
                                                     'address': address,
                                                     'driving_license': driving_license,
                                                     'contact_number': contact_number})

def review_page_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    reviews = Review.objects.filter(vehicle_id=vehicle_id)
    average_score = reviews.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'reviews.html', {'vehicle': vehicle,
                                            'average_score': average_score })

def create_review_view(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            score = min(score, 100)
            score = max(score, 0)
            review = form.cleaned_data['review']

            existing_reviews = Review.objects.filter(vehicle=vehicle, account=user)

            if existing_reviews.first():
                Review.objects.all().delete()

            Review.objects.create(vehicle=vehicle,
                                   account=user,
                                   rating=score,
                                   text=review)
            
            return redirect('reviews', vehicle_id=vehicle_id)
    else:
        form = ReviewForm()
    return render(request, 'review_page.html', {'form': form,
                                                'vehicle': vehicle })

def forum_view(request, forumpost_id):
    root = get_object_or_404(ForumPost, pk=forumpost_id)
    return render(request, 'forum.html', {'post': root })

def reply_view(request, forumpost_id):
    parent = get_object_or_404(ForumPost, pk=forumpost_id)
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            date = datetime.now()

            ForumPost.objects.create(parent=parent,
                                     account=user,
                                     date=date,
                                     text=text)
            
            return redirect('forum', forumpost_id=forumpost_id)
    else:
        form = PostForm()
    return render(request, 'reply_form_page.html', {'parent': parent,
                                                    'form': form })

def make_post_view(request):
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            date = datetime.now()

            ForumPost.objects.create(parent=None,
                                     account=user,
                                     date=date,
                                     text=text)
            
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'reply_form_page.html', { 'form': form })

def root_posts_view(request):
    root_posts = ForumPost.objects.filter(parent=None).order_by('date')
    return render(request, 'posts.html', {'root_posts': root_posts})

def checked_in_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.is_signed = True
    reservation.save()
    return render(request, 'checked_in.html', {'reservation_id': reservation_id })

def check_out_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    # Write your view code here
    return render(request, 'CheckOut.html')

def vehicle_view(request):
    return render(request, 'Addvehicle.html')

def final_receipt_view(request):
    return render(request, 'FinalReceipt.html')

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

    """
    if request.method == 'POST':
        car_name = request.POST.get('convertibleCarDropdown')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Get the selected vehicle from the database
        vehicle = Vehicle.objects.get(vehicle_make=car_name)

        # Create a new reservation
        reservation = Reservation.objects.create(vehicle=vehicle, account=request.user, reservation_start=start_date, reservation_end=end_date)

        # Optionally, you can redirect the user to a success page or render a template
        return render(request, 'reservations.html', {'reservation': reservation})
    """
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

@login_required_redirect
def audiA4Reserve_view(request):
    return render(request, 'audiA4Reserve.html')

@login_required_redirect
def porsche911Reserve_view(request):
    if request.method == 'POST':
        start_date911=request.POST.get("start_date")
        end_date911=request.POST.get("end_date")

        start_date = datetime.strptime(start_date911, "%Y/%m/%d")
        end_date = datetime.strptime(end_date911, "%Y/%m/%d")

        vehicle911=Vehicle.objects.create(
            vehicle_vin=123456,
            vehicle_make="porsche",
            vehicle_model="911",
            vehicle_year="2020",
            vehicle_license_plate="a1b2c3",
            vehicle_color="blue",
            is_rented=False
        )

        pick_up_location911=Location.objects.create(
            title="Montreal"
        )
        
        drop_off_location911 = Location.objects.create(
            title="Laval"
        )
        
        rental_period = (end_date - start_date)
        mileage_limit911=300
        additional_services911="extra luggage space"
        is_signed911=True

        reservation=Reservation.objects.create(
            vehicle=vehicle911,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_location911,
            drop_off_location=drop_off_location911,
            rental_period=rental_period,
            mileage_limit=mileage_limit911,
            additional_services=additional_services911,
            is_signed=is_signed911,
        )
    return render(request, 'porsche911Reserve.html')

@login_required_redirect
def ferrariRomaReserve_view(request):
    return render(request, 'ferrariRomaReserve.html')

@login_required_redirect
def bentleyBentaygaReserve_view(request):
    return render(request, 'bentleyBentaygaReserve.html')

@login_required_redirect
def chevroletVoltReserve_view(request):
    return render(request, 'chevroletVoltReserve.html')

@login_required_redirect
def toyotaPriusReserve_view(request):
    return render(request, 'toyotaPriusReserve.html')

@login_required_redirect
def kiaNiroReserve_view(request):
    return render(request, 'kiaNiroReserve.html')

@login_required_redirect
def hondaCivicReserve_view(request):
    if request.method == 'POST':
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        getVehicle = Vehicle.objects.create(
            vehicle_vin=19284756,
            vehicle_make="Honda",
            vehicle_model="Civic",
            vehicle_year="2005",
            vehicle_license_plate="a2b3c4",
            vehicle_color="blue",
            is_rented=False
        )
        random_location1 = Location.objects.order_by('?').first()  # Get a random location
        getPick_up_location = random_location1.title
        random_location2 = Location.objects.order_by('?').first()  # Get a random location
        getDrop_off_location = random_location2.title
        getRental_period = request.POST.get("duration")
        getMileage_limit = 300
        getAdditional_services = "extra luggage space"
        getIs_signed = True
        reservation = Reservation.objects.create(
            vehicle = getVehicle,  # Assuming you have a hidden input for vehicle_id
            account = request.user,
            reservation_start = start_date,
            reservation_end = end_date,
            pick_up_location = getPick_up_location,
            drop_off_location = getDrop_off_location,
            rental_period = getRental_period,
            mileage_limit = getMileage_limit,
            additional_services = getAdditional_services,
            is_signed = getIs_signed,
        )
    return render(request, 'hondaCivicReserve.html')

@login_required_redirect
def fordMustangReserve_view(request):
    return render(request, 'fordMustangReserve.html')

@login_required_redirect
def audiA5Reserve_view(request):
    return render(request, 'audiA5Reserve.html')

@login_required_redirect
def bmwM4Reserve_view(request):
    return render(request, 'bmwM4Reserve.html')

@login_required_redirect
def chevroletCorvetteReserve_view(request):
    return render(request, 'chevroletCorvetteReserve.html')

def checkOutPayment(request):
    return render(request, 'checkOutPayment.html')

def checkOutConfirm(request):
    return render(request, 'checkOutConfirm.html')

