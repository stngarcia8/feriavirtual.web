from django.contrib.auth.models import User
from django.db import models


class LoginSession(models.Model):
    "Define la sesion de un usuario logeado en el sistema."
    id = models.AutoField(primary_key=True)
    UserId = models.CharField(max_length=150)
    ClientId = models.CharField(max_length=150)
    Username = models.CharField(max_length=150)
    FullName = models.CharField(max_length=250)
    Email = models.CharField(max_length=254)
    ProfileId = models.PositiveIntegerField(
        default=0, verbose_name='id perfil')
    ProfileName = models.CharField(max_length=50)
    User = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.FullName

    class meta:
        ordering = ['FullName']
