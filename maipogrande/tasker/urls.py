from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^tasks/usuarios/$',
        views.CargarNuevoUsuario, name='cargarNuevoUsuario'),
]
