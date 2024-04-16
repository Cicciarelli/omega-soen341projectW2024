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

@login_required_redirect
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
@login_required_redirect
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
    reservation.delete()
    return render(request, 'CheckOut.html')

def vehicle_view(request):
    return render(request, 'Vehicles/Addvehicle.html')

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
    return render(request, 'Vehicles/OMEGACarList.html')

def toyota_corolla(request):
    return render(request, 'Vehicles/ToyotaCorolla.html')

def honda_civic(request):
    return render(request, 'Vehicles/HondaCivic.html')

def chevrolet_volt(request):
    return render(request, 'Vehicles/ChevroletVolt.html')

def toyota_prius(request):
    return render(request, 'Vehicles/ToyotaPrius.html')

def kia_niro(request):
    return render(request, 'Vehicles/KiaNiro.html')

def ford_mustang(request):
    return render(request, 'Vehicles/FordMustang.html')

def audi_a5(request):
    return render(request, 'Vehicles/AudiA5.html')

def bmw_m4(request):
    return render(request, 'Vehicles/BMWM4.html')

def chevrolet_corvette(request):
    return render(request, 'Vehicles/ChevroletCorvette.html')

def porsche_911(request):
    return render(request, 'Vehicles/Porsche911.html')

def audi_a4(request):
    return render(request, 'Vehicles/AudiA4.html')

def ferrari_roma(request):
    return render(request, 'Vehicles/FerrariRoma.html')

def bentley_bentayga(request):
    return render(request, 'Vehicles/BentleyBentayga.html')

@login_required_redirect
def audiA4Reserve_view(request):
    if request.method == 'POST':
        start_dateA4=request.POST.get("start_date")
        end_dateA4=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateA4, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateA4, "%Y/%m/%d")

        vehicleA4=Vehicle.objects.create(
            vehicle_vin=612978,
            vehicle_make="Audi",
            vehicle_model="A4",
            vehicle_year="2020",
            vehicle_license_plate="H9R77S",
            vehicle_color="black",
            is_rented=False
        )

        pick_up_locationA4=Location.objects.create(
            title="Montreal"
        )
        
        drop_off_locationA4 = Location.objects.create(
            title="Laval"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitA4=300
        additional_servicesA4="extra luggage space"
        is_signedA4=False

        reservation=Reservation.objects.create(
            vehicle=vehicleA4,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationA4,
            drop_off_location=drop_off_locationA4,
            rental_period=rental_period,
            mileage_limit=mileage_limitA4,
            additional_services=additional_servicesA4,
            is_signed=is_signedA4,
        )
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
        is_signed911=False

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
def toyotaCorolla_view(request):
    return render(request, 'toyotaCorollaReserve.html')

""" ^^^ toyotaCorollaReserve.html does not exist yet"""

@login_required_redirect
def bentleyBentaygaReserve_view(request):
    if request.method == 'POST':
        start_dateBTA=request.POST.get("start_date")
        end_dateBTA=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateBTA, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateBTA, "%Y/%m/%d")

        vehicleBTA=Vehicle.objects.create(
            vehicle_vin=947322,
            vehicle_make="Bentley",
            vehicle_model="Bentayga",
            vehicle_year="2023",
            vehicle_license_plate="H1N1N1",
            vehicle_color="Red",
            is_rented=False
        )

        pick_up_locationBTA=Location.objects.create(
            title="Montreal"
        )

        drop_off_locationBTA = Location.objects.create(
            title="Laval"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitBTA=300
        additional_servicesBTA="N/A"
        is_signedBTA=False

        reservation=Reservation.objects.create(
            vehicle=vehicleBTA,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationBTA,
            drop_off_location=drop_off_locationBTA,
            rental_period=rental_period,
            mileage_limit=mileage_limitBTA,
            additional_services=additional_servicesBTA,
            is_signed=is_signedBTA,
        )
    return render(request, 'bentleyBentaygaReserve.html')

@login_required_redirect
def chevroletVoltReserve_view(request):
    if request.method == 'POST':
        start_dateV=request.POST.get("start_date")
        end_dateV=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateV, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateV, "%Y/%m/%d")

        vehicleV=Vehicle.objects.create(
            vehicle_vin=192837,
            vehicle_make="Chevrolet",
            vehicle_model="Volt",
            vehicle_year="2018",
            vehicle_license_plate="GR33NY",
            vehicle_color="Blue",
            is_rented=False
        )

        pick_up_locationV=Location.objects.create(
            title="Montreal"
        )
        
        drop_off_locationV = Location.objects.create(
            title="Mont Tremblant"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitV=300
        additional_servicesV="N/A"
        is_signedV=False

        reservation=Reservation.objects.create(
            vehicle=vehicleV,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationV,
            drop_off_location=drop_off_locationV,
            rental_period=rental_period,
            mileage_limit=mileage_limitV,
            additional_services=additional_servicesV,
            is_signed=is_signedV,
        )
    return render(request, 'chevroletVoltReserve.html')

@login_required_redirect
def toyotaPriusReserve_view(request):
    if request.method == 'POST':
        start_dateP=request.POST.get("start_date")
        end_dateP=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateP, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateP, "%Y/%m/%d")

        vehicleP=Vehicle.objects.create(
            vehicle_vin=675849,
            vehicle_make="Toyota",
            vehicle_model="Prius",
            vehicle_year="2015",
            vehicle_license_plate="G04T3D",
            vehicle_color="Black",
            is_rented=False
        )

        pick_up_locationP=Location.objects.create(
            title="Montreal"
        )
        
        drop_off_locationP = Location.objects.create(
            title="Sherbrooke"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitP=300
        additional_servicesP="extra luggage space"
        is_signedP=False

        reservation=Reservation.objects.create(
            vehicle=vehicleP,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationP,
            drop_off_location=drop_off_locationP,
            rental_period=rental_period,
            mileage_limit=mileage_limitP,
            additional_services=additional_servicesP,
            is_signed=is_signedP,
        )
    return render(request, 'toyotaPriusReserve.html')

@login_required_redirect
def kiaNiroReserve_view(request):
    if request.method == 'POST':
        start_dateN=request.POST.get("start_date")
        end_dateN=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateN, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateN, "%Y/%m/%d")

        vehicleN=Vehicle.objects.create(
            vehicle_vin=284756,
            vehicle_make="KIA",
            vehicle_model="Niro",
            vehicle_year="2019",
            vehicle_license_plate="D3N1R0",
            vehicle_color="White",
            is_rented=False
        )

        pick_up_locationN=Location.objects.create(
            title="Montreal"
        )
        
        drop_off_locationN = Location.objects.create(
            title="Dorval"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitN=300
        additional_servicesN="N/A"
        is_signedN=False

        reservation=Reservation.objects.create(
            vehicle=vehicleN,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationN,
            drop_off_location=drop_off_locationN,
            rental_period=rental_period,
            mileage_limit=mileage_limitN,
            additional_services=additional_servicesN,
            is_signed=is_signedN,
        )
    return render(request, 'kiaNiroReserve.html')

@login_required_redirect
def hondaCivicReserve_view(request):
    if request.method == 'POST':
        start_dateCIV=request.POST.get("start_date")
        end_dateCIV=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateCIV, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateCIV, "%Y/%m/%d")

        vehicleCIV=Vehicle.objects.create(
            vehicle_vin=420420,
            vehicle_make="Honda",
            vehicle_model="Civic",
            vehicle_year="2005",
            vehicle_license_plate="G3TR3KT",
            vehicle_color="MATTE BLACK",
            is_rented=False
        )

        pick_up_locationCIV=Location.objects.create(
            title="Ottawa"
        )
        
        drop_off_locationCIV = Location.objects.create(
            title="Cote Sud"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitCIV=300
        additional_servicesCIV="1100 HP Supercharger"
        is_signedCIV=False

        reservation=Reservation.objects.create(
            vehicle=vehicleCIV,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationCIV,
            drop_off_location=drop_off_locationCIV,
            rental_period=rental_period,
            mileage_limit=mileage_limitCIV,
            additional_services=additional_servicesCIV,
            is_signed=is_signedCIV,
        )
    return render(request, 'hondaCivicReserve.html')

@login_required_redirect
def fordMustangReserve_view(request):
    if request.method == 'POST':
        start_dateMust=request.POST.get("start_date")
        end_dateMust=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateMust, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateMust, "%Y/%m/%d")

        vehicleMust=Vehicle.objects.create(
            vehicle_vin=100101,
            vehicle_make="Ford",
            vehicle_model="Mustang",
            vehicle_year="2018",
            vehicle_license_plate="ST4NKY",
            vehicle_color="Navy with white stripes",
            is_rented=False
        )

        pick_up_locationMust=Location.objects.create(
            title="Villeray"
        )
        
        drop_off_locationMust = Location.objects.create(
            title="Montreal Nord"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitMust=300
        additional_servicesMust="Supercharger"
        is_signedMust=False

        reservation=Reservation.objects.create(
            vehicle=vehicleMust,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationMust,
            drop_off_location=drop_off_locationMust,
            rental_period=rental_period,
            mileage_limit=mileage_limitMust,
            additional_services=additional_servicesMust,
            is_signed=is_signedMust,
        )
    return render(request, 'fordMustangReserve.html')

@login_required_redirect
def audiA5Reserve_view(request):
    if request.method == 'POST':
        start_dateA5=request.POST.get("start_date")
        end_dateA5=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateA5, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateA5, "%Y/%m/%d")

        vehicleA5=Vehicle.objects.create(
            vehicle_vin=225019,
            vehicle_make="Audi",
            vehicle_model="A5",
            vehicle_year="2021",
            vehicle_license_plate="Z00M1E",
            vehicle_color="Matte White",
            is_rented=False
        )

        pick_up_locationA5=Location.objects.create(
            title="Dorval"
        )
        
        drop_off_locationA5 = Location.objects.create(
            title="Laval"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitA5=300
        additional_servicesA5="Twin Turbo for fuel efficiency"
        is_signedA5=False

        reservation=Reservation.objects.create(
            vehicle=vehicleA5,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationA5,
            drop_off_location=drop_off_locationA5,
            rental_period=rental_period,
            mileage_limit=mileage_limitA5,
            additional_services=additional_servicesA5,
            is_signed=is_signedA5,
        )
    return render(request, 'audiA5Reserve.html')

@login_required_redirect
def bmwM4Reserve_view(request):
    if request.method == 'POST':
        start_dateM4=request.POST.get("start_date")
        end_dateM4=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateM4, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateM4, "%Y/%m/%d")

        vehicleM4=Vehicle.objects.create(
            vehicle_vin=696969,
            vehicle_make="BMW",
            vehicle_model="M4",
            vehicle_year="2022",
            vehicle_license_plate="BRR44T",
            vehicle_color="Matte Black",
            is_rented=False
        )

        pick_up_locationM4=Location.objects.create(
            title="Dorval"
        )
        
        drop_off_locationM4 = Location.objects.create(
            title="Laval"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitM4=300
        additional_servicesM4="Baby Seat"
        is_signedM4=False

        reservation=Reservation.objects.create(
            vehicle=vehicleM4,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationM4,
            drop_off_location=drop_off_locationM4,
            rental_period=rental_period,
            mileage_limit=mileage_limitM4,
            additional_services=additional_servicesM4,
            is_signed=is_signedM4,
        )
    return render(request, 'bmwM4Reserve.html')

@login_required_redirect
def chevroletCorvetteReserve_view(request):
    if request.method == 'POST':
        start_dateCorv=request.POST.get("start_date")
        end_dateCorv=request.POST.get("end_date")

        start_date = datetime.strptime(start_dateCorv, "%Y/%m/%d")
        end_date = datetime.strptime(end_dateCorv, "%Y/%m/%d")

        vehicleCorv=Vehicle.objects.create(
            vehicle_vin=228474,
            vehicle_make="Chevrolet",
            vehicle_model="Corvette",
            vehicle_year="2019",
            vehicle_license_plate="TURNUP",
            vehicle_color="Black with Red Stripes",
            is_rented=False
        )

        pick_up_locationCorv=Location.objects.create(
            title="Montreal"
        )
        
        drop_off_locationCorv = Location.objects.create(
            title="Brossard"
        )
        
        rental_period = (end_date - start_date)
        mileage_limitCorv=300
        additional_servicesCorv="N/A"
        is_signedCorv=False

        reservation=Reservation.objects.create(
            vehicle=vehicleCorv,  
            account=request.user,
            reservation_start=start_date,
            reservation_end=end_date,
            pick_up_location=pick_up_locationCorv,
            drop_off_location=drop_off_locationCorv,
            rental_period=rental_period,
            mileage_limit=mileage_limitCorv,
            additional_services=additional_servicesCorv,
            is_signed=is_signedCorv,
        )
    return render(request, 'chevroletCorvetteReserve.html')

def checkOutPayment(request):
    return render(request, 'checkOutPayment.html')

def checkOutConfirm(request):
    return render(request, 'checkOutConfirm.html')

def final_receipt_view(request):
    damages = True if request.POST.get('damages') == 'Yes' else False
    rental_price = 750  
    deposited_amount = 500 if damages else 0
    context = {
        'damages': damages,
        'rental_price': rental_price,
        'deposited_amount': deposited_amount,
    }
    return render(request, 'FinalReceipt.html', context)

