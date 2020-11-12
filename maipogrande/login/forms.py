from django import forms


class LoginForm(forms.Form):
    "Formulario de inicio de sesion."
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': '', 'minlength': 8}), label="Nombre de Usuario")
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'minlegth': 8}), label="Contraseña")
