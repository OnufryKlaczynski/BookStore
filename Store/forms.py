from django import forms

from .models import Order

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'email', 'first_name', 'last_name',
            'house_number', 'street', 'city',
            'zip_code', 'voivodeship', 'additional_info'
            )