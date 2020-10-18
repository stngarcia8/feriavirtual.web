from django import forms
from django.forms import ModelForm, TextInput, NumberInput, EmailInput, Select, HiddenInput
from .models import Comercial, City

class CreateComercialForm(ModelForm):
    "Formulario para datos comerciales"
    
    class Meta:
        model = Comercial
        fields = (
            'ComercialID', 'ClientID','CompanyName', 'FantasyName', 'ComercialBusiness', 'Email',
            'ComercialDNI', 'Address', 'Country', 'City', 'PhoneNumber'
        )
        widgets = {
            'ComercialID': HiddenInput(),
            'ClientID': HiddenInput(),
            'CompanyName': TextInput(attrs={'size': '15'}),
            'FantasyName': TextInput(attrs={'size': '15'}),
            'ComercialBusiness': TextInput(attrs={'size': '15'}),
            'Email': EmailInput(),
            'ComercialDNI': NumberInput(),
            'Address': TextInput(attrs={'size': '15'}),
            'Country': Select(attrs={'autofocus': ''}),
            'City': Select(attrs={'autofocus': ''}),
            'PhoneNumber': NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['City'].queryset = City.objects.none()
        if 'Country' in self.data:
            try:
                country_id = int(self.data.get('Country'))
                self.fields['City'].queryset = City.objects.filter(
                    Country_id=country_id).order_by('CityName')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['City'].queryset = self.instance.Country.city_set.order_by(
                'CityName')
