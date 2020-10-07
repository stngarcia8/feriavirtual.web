from django import forms
from django.forms import ModelForm
from .models import ComercialInfo, City


# ContactForm()
# Formulario de contacto para el registro de usuarios
class ContactForm(forms.Form):
    name = forms.CharField(label="Nombre", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Escriba su nombre completo'}
    ), min_length=3, max_length=100)
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Escriba suemail'}
    ), min_length=3, max_length=100)
    content = forms.CharField(label="Contenido", required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3,
               'placeholder': 'Escriba su mensaje'}
    ), min_length=10, max_length=1000)


# ComercialForm()
# Formulario de mantenimiento de los datos comerciales de los usuarios
class ComercialForm(ModelForm):
    class Meta:
        model = ComercialInfo
        fields = ('CompanyName', 'FantasyName', 'ComercialBusiness', 'Email',
                  'ComercialDNI', 'Address', 'Country', 'City', 'PhoneNumber')

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
