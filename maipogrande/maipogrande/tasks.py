from celery import shared_task
from django.core.management import call_command
from core.management.commands import conectar_rabbitmq

@shared_task(ignore_result=True)
def abrir_queues_rabbit():
    call_command("conectar_rabbitmq", )