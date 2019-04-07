from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')



    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    

class OrderDataForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
             'first_name',
             'last_name',
             'house_number',
             'street',
             'city',
             'zip_code',
             'voivodeship',
             'additional_info',
             ]