from django.contrib import admin

# Register your models here.


# Ejecutando las tareas en segundo plano
from maipogrande.tasks import abrir_queues_usuarios, abrir_queues_contratos, abrir_queues_cierre_subasta
abrir_queues_usuarios.apply_async()
abrir_queues_contratos.apply_async()
abrir_queues_cierre_subasta.apply_async()