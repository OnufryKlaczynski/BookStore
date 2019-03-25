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



class DotPayForm(forms.Form):
    api_version = forms.CharField(widget = forms.HiddenInput())
    id = forms.IntegerField(widget = forms.HiddenInput())
    amount = forms.CharField(widget = forms.HiddenInput())
    current = forms.CharField(widget = forms.HiddenInput())
    description = forms.CharField(widget = forms.HiddenInput())
    type = forms.IntegerField(widget = forms.HiddenInput())
    URL = forms.CharField(widget = forms.HiddenInput())
    URLC = forms.CharField(widget = forms.HiddenInput())
    bylaw = forms.CharField(widget = forms.HiddenInput())
    personal_data = forms.CharField(widget = forms.HiddenInput())

    firstname = forms.CharField(widget = forms.HiddenInput())
    lastname = forms.CharField(widget = forms.HiddenInput())
    email = forms.EmailField(widget = forms.HiddenInput())