from django import forms
from django.forms import ModelForm


class ContactForm(forms.Form):
    "Formulario de contacto"
    name = forms.CharField(label="Nombre", required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Escriba su nombre completo', 'minlength': 8, 'pattern': '[ña-zÑA-Z\s\.]+$'}
        ), min_length=3, max_length=100)
    email = forms.EmailField(label="Email", required=True, 
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Escriba su email',
                   'pattern': '^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'}
        ), min_length=3, max_length=100)
    content = forms.CharField(label="Contenido", required=True, 
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3,
               'placeholder': 'Escriba su mensaje'}
        ), min_length=10, max_length=1000)
