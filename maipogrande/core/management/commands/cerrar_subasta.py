import json
from django.core.management.base import BaseCommand
from transportista.models import Auction
from maipogrande.rabbitmq import ConectarRabbitMQ


class Command(BaseCommand):
    help = 'Se conecta con la cola de resultados de subastas.'

    def handle(self, *args, **kwargs):
        self.conectar_rabbitmq()

    def consumer_callback(self, ch, method, properties, body):
        "Callback de la cola de cierre de subastas."
        json_data = json.loads(body)
        subasta = Auction.objects.get(AuctionId=json_data['AuctionId'])
        subasta.Status = json_data['Status']
        subasta.save()
        return

    def conectar_rabbitmq(self):
        "Conecta a la cola de mensajes de subastas abiertas."
        nombre_queue = 'AuctionWasClose'
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
