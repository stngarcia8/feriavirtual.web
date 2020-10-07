from django import forms


# LoginForm
# Formulario de inicio de sesion.
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(), label="Nombre de Usuario")
    password = forms.CharField(
        widget=forms.PasswordInput(), label="Contraseña")
