
# Register your models here.


# Ejecutando las tareas en segundo plano
from maipogrande.tasks import abrir_queues_rabbit
abrir_queues_rabbit.delay()


