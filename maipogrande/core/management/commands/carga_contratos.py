import json
from contratos.serializers import ContratoSerializer
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from maipogrande.rabbitmq import ConectarRabbitMQ


class Command(BaseCommand):
    help = 'Carga contratos desde la base de datos de feria virtual.'

    def handle(self, *args, **kwargs):
        self.conectar_rabbitmq()

    def consumer_callback(self, ch, method, properties, body):
        "Callback de la cola de contratos."
        json_data = json.loads(body)
        print()
        print(json_data)
        print()
        serializador = ContratoSerializer(data=json_data)
        serializador.is_valid()
        serializador.save()
        print()
        print(serializador.errors)
        print()
        return

    def conectar_rabbitmq(self):
        "Conecta a la cola de mensajes de usuarios creados."
        nombre_queue = 'ContractQueue'
        connection = ConectarRabbitMQ().get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=nombre_queue, durable=True)
        channel.basic_consume(on_message_callback=self.consumer_callback, queue=nombre_queue, auto_ack=True)
        try:
            print('Consumiendo mensajes de cola {0}'.format(nombre_queue))
            channel.start_consuming()
        except KeyboardInterrupt:
            print('Conexión a RabbitMQ finalizada.')
            connection.close()
