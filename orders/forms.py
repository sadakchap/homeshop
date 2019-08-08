from django import forms
from .models import Address

class ShippingAddresForm(forms.ModelForm):
    addr_line_1 = forms.CharField(label='Address Line 1',max_length=120)
    addr_line_2 = forms.CharField(label='Address Line 2',max_length=120, required=False)
    class Meta:
        model = Address
        fields = ('name', 'nickname', 'addr_line_1', 'addr_line_2', 'city', 'state', 'country', 'postal_code')