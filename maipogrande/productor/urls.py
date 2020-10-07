from django.conf.urls import url
from django.urls import path
from . import views


# Rutas de la aplicacion
urlpatterns = [
    url(r'^producto/$', views.ListarProductos, name='listarProductos'),
]
