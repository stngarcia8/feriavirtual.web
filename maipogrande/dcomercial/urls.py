from django.conf.urls import url
from django.urls import path
from . import views


# Rutas de la aplicacion
urlpatterns = [
    # Rutas para los datos comerciales
    path('ver/ciudad/', views.CargarCiudades, name='cargarCiudades'),
    url(r'^comercial/$',
        views.IniciarDatoComercial, name='iniciarComercial'),
    url(r'^comercial/ver/(?P<pk>\d+)$',
        views.ComercialDetailView.as_view(), name='verComercial'),
    url(r'^comercial/sindato/$',
        views.ComercialTemplateView.as_view(), name='sinDatoComercial'),
    url(r'^comercial/registrar/$',
        views.ComercialCreateView.as_view(), name='registrarComercial'),
    url(r'^comercial/editar/(?P<pk>\d+)$',
        views.ComercialUpdateView.as_view(), name='editarComercial'),
    url(r'^comercial/eliminar/(?P<pk>\d+)$',
        views.ComercialDeleteView.as_view(), name='eliminarComercial'),
]