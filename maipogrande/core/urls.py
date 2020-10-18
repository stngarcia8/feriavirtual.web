from django.conf.urls import url
from . import views


# Rutas de la aplicacion
urlpatterns = [
    # Rutas de la pantalla de inicio.
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^about/$', views.About.as_view(), name='about'),
    url(r'^contact/$', views.Contact, name='contact'),

    # Rutas de las paginas de inicio de cada tipo de cliente
    url(r'^externalcustomer/$', views.HomeExternalCustomer.as_view(),
        name='homeExternalCustomer'),
    url(r'^internalcustomer/$', views.HomeInternalCustomer.as_view(),
        name='homeInternalCustomer'),
    url(r'^dhome/$', views.DinamicHome,
        name='dinamicHome'),

    # Ruta para mensajes de aviso al usuario
    url(r'^servicenotavailable/$', views.ServiceNotAvailable.as_view(),
        name='serviceNotAvailable'),
    url(r'^contactfail/$', views.EmailFail.as_view(),
        name='emailFail'),
    url(r'^contactok/$', views.EmailOk.as_view(),
        name='emailOk'),
]
