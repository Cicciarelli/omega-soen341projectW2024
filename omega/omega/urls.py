"""
URL configuration for omega project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import my_view
from django.contrib.auth import views as auth_views
from django.urls import include
from . import views

urlpatterns = [
    path('',views.my_view,name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('startReservation/', views.startres_view, name='startres'),
    path('economyReservation/', views.economy_view, name='economyres'),
    path('luxuryReservation/', views.luxury_view, name='luxuryres'),
    path('convertibleReservation/', views.convertible_view, name='convertibleres'),

    path('reservations/', views.reservations_view, name='reservations'),

    path('reservation/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),

    path('admin/', admin.site.urls),
    
    path('convertibleReservation/', views.convertible_view, name='convertibleres'),

#car lists
    
    path('OMEGACarList/',views.OMEGACarList,name='carList'),
    path('ToyotaCorolla/',views.toyota_corolla,name='Corolla'),
    path('HondaCivic/',views.honda_civic,name='Civic'),
    path('ChevroletVolt/',views.chevrolet_volt,name='Volt'),
    path('ToyotaPrius/',views.toyota_prius,name='Prius'),
    path('KiaNiro/',views.kia_niro,name='Niro'),
    path('FordMustang/',views.ford_mustang,name='Mustang'),
    path('AudiA5/',views.audi_a5,name='A5'),
    path('BMWM4/',views.bmw_m4,name='M4'),
    path('ChevroletCorvette/',views.chevrolet_corvette,name='Corvette'),
    path('Porsche911/',views.porsche_911,name='911'),
    path('AudiA4/',views.audi_a4,name='A4'),
    path('FerrariRoma/',views.ferrari_roma,name='Roma'),
    path('BentleyBentayga/',views.bentley_bentayga,name='Bentayga'),


]


