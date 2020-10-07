from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Country
# Modelo de datos que representa los paises de residencia de los clientes en el sistema.
class Country(models.Model):
    CountryID = models.AutoField(primary_key=True)
    CountryName = models.CharField(max_length=100)
    CountryPrefix = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        ordering = ('CountryID',)

    def __str__(self):
        return self.CountryName


# City
# Modelo de datos que representa las ciudades de residencia de los clientes en el sistema.
class City(models.Model):
    CityID = models.AutoField(primary_key=True)
    CityName = models.CharField(max_length=100)
    Country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('CityID',)

    def __str__(self):
        return self.CityName


# Profile
# Modelo de datos que representa el rol de usuario en el sistema.
class Profile(models.Model):
    ProfileID = models.AutoField(primary_key=True)
    ProfileName = models.CharField(max_length=50)

    class Meta:
        ordering = ('ProfileID',)

    def __str__(self):
        return self.ProfileName


# ComercialInfo:
# Modelo que representa los datos comerciales de los clientes
class ComercialInfo(models.Model):
    ComercialID = models.CharField(max_length=40)
    ClientID = models.CharField(max_length=40)
    CompanyName = models.CharField(max_length=100, verbose_name='Razón social')
    FantasyName = models.CharField(
        max_length=100, verbose_name='Nombre de fantasía',)
    ComercialBusiness = models.CharField(
        max_length=100, verbose_name='Giro comercial',)
    Email = models.EmailField(verbose_name='Email comercial', validators=[
                              RegexValidator(r'^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')])
    ComercialDNI = models.CharField(
        max_length=20, help_text='(ej: 12345678-9)', verbose_name='DNI comercial',)
    Address = models.CharField(
        max_length=100, verbose_name='Dirección comercial')
    City = models.ForeignKey(
        City, null=True, on_delete=models.SET_NULL, verbose_name='Seleccione ciudad')
    Country = models.ForeignKey(
        Country, null=True, on_delete=models.SET_NULL, verbose_name='Seleccione país')
    PhoneNumber = models.CharField(max_length=30, verbose_name='Teléfono')
    User = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    class meta:
        ordering = ('id',)

    def __str__(self):
        return self.CompanyName
