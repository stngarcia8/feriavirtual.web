from celery import shared_task
from django.core.management import call_command


@shared_task
def abrir_queues_usuarios():
    call_command("crea_usuario", )


@shared_task
def abrir_queues_contratos():
    call_command("carga_contratos", )


@shared_task
def abrir_queues_cierre_subasta():
    call_command("cerrar_subasta", )