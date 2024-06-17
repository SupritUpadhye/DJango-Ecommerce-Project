from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_type', 'street1', 'street2', 'city', 'pincode', 'mobile_number']
