import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.urls import reverse


class Country(models.Model):
    "Modelo que representa los países de residencia de los clientes"
    CountryID = models.IntegerField(default=1)
    CountryName = models.CharField(max_length=100)
    CountryPrefix = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.CountryName

class City(models.Model):
    "Modelo que representa las ciudades de residencia de los clientes"
    CityID = models.IntegerField(default=1)
    CityName = models.CharField(max_length=100)
    Country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.CityName


class Profile(models.Model):
    ProfileID = models.AutoField(primary_key=True)
    ProfileName = models.CharField(max_length=50)

    class Meta:
        ordering = ('ProfileID',)

    def __str__(self):
        return self.ProfileName        


class Comercial(models.Model):
    "Modelo que representa los datos comerciales de los clientes"
    ComercialID = models.UUIDField(default=uuid.uuid4, unique=True)
    ClientID = models.CharField(max_length=40, blank=True, null=True)
    CompanyName = models.CharField(max_length=100, verbose_name='Razón social')
    FantasyName = models.CharField(
        max_length=100, verbose_name='Nombre de fantasía')
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
    PhoneNumber = models.CharField(max_length=15, verbose_name='Teléfono')
    User = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class meta:
        ordering = ('id',)

    def __str__(self):
        return self.CompanyName

    def get_absolute_url(self):
        "Define la ruta absoluta de los datos comerciales."
        return reverse('verComercial', args=[self.User.id])        

