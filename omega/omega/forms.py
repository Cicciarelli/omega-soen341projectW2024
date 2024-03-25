from django import forms
from .models import Reservation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['vehicle',
                  'reservation_start',
                  'reservation_end',
                  'pick_up_location',
                  'drop_off_location',
                  'mileage_limit',
                  'additional_services']

class UserCreationFormWithEmail(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
        field_classes = {'email': forms.EmailField}

class SignatureForm(forms.Form):
    name = forms.CharField(label='Your Signature', max_length=100)