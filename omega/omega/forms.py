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
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email",)

    field_classes = {
        'first_name': forms.CharField,
        'last_name': forms.CharField,
        'email': forms.EmailField,
    }

class RentalAgreementSetupForm(forms.Form):
    address = forms.CharField(label='Address', max_length=100)
    driving_license = forms.CharField(label='Driving License', max_length=100)
    contact_number = forms.CharField(label='Contact Number', max_length=100)

class SignatureForm(forms.Form):
    name = forms.CharField(label='Your Signature', max_length=100)

class ReviewForm(forms.Form):
    score = forms.IntegerField(label='score')
    review = forms.CharField(label='review', max_length=2048, widget=forms.Textarea)

class PostForm(forms.Form):
    text = forms.CharField(label='text', max_length=2048, widget=forms.Textarea)