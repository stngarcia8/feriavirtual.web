from django.apps import AppConfig
from maipogrande.tasks import abrir_queues_usuarios

class CoreConfig(AppConfig):
    name = 'core'
