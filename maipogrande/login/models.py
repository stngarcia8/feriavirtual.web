from django.db import models
from django.contrib.auth.models import User


# LoginSession
# Clase que define el inicio de sesion de los usuarios
class LoginSession(models.Model):
    id = models.AutoField(primary_key=True)
    UserId = models.CharField(max_length=150)
    ClientID = models.CharField(max_length=150)
    Username = models.CharField(max_length=150)
    FullName = models.CharField(max_length=250)
    Email = models.CharField(max_length=254)
    ProfileID = models.PositiveIntegerField(
        default=0, verbose_name='id perfil')
    ProfileName = models.CharField(max_length=50)
    User = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.FullName

    class meta:
        ordering = ['FullName']
