import json
from django.core.management.base import BaseCommand
from maipogrande.rabbitmq import ConectarRabbitMQ
from .user_events import UserEvents
from .order_events import OrderEvents
from .auction_events import AuctionEvents
from .contract_events import ContractEvents
from .payment_events import PaymentEvents
from .product_events import ProductEvents
from .offer_events import OfferEvents

class Command(BaseCommand):
    help = 'Procesa los mensajes provenientes de RabbitMQ.'

    def handle(self, *args, **kwargs):
        print("Consumiendo mensajes desde RabbitMQ, para salir presione CTRL+C")
        self.conectar_rabbitmq()

    def callback(self, ch, method, properties, body):
        "Callback de la cola de usuarios"
        json_data = json.loads(body)
        args = str(method.routing_key).upper().strip().split(sep='.')
        event = args[2]
        group = args[1]
        print("Procesando queue={0}, group={1}, event={2}".format(method.routing_key, group, event))
        if group == 'USER':
            UserEvents(event, json_data).event_executor()
        elif group == 'ORDER':
            OrderEvents(event, json_data).event_executor()
        elif group == 'AUCTION':
            AuctionEvents(event, json_data).event_executor()
        elif group == 'CONTRACT':
            ContractEvents(event, json_data).event_executor()
        elif group == 'PAYMENT':
            PaymentEvents(event, json_data).event_executor()
        elif group == 'PRODUCT':
            ProductEvents(event, json_data).event_executor()
        elif group == 'OFFER':
            OfferEvents(event, json_data).event_executor()         
        return

    def conectar_rabbitmq(self):
        "Conecta a la cola de mensajes de usuarios creados."
        exchange_name = 'maipogrande'
        routing_key = 'maipogrande.#'
        queue_name = 'mg-queue'
        try:
            connection = ConectarRabbitMQ().get_connection()
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type='topic', auto_delete=False)
            channel.queue_declare(queue=queue_name, exclusive=True, auto_delete=True)
            channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
            channel.basic_consume(on_message_callback=self.callback, queue=queue_name, auto_ack=True)
            channel.start_consuming()
        except KeyboardInterrupt:
            connection.close()
            print('Conexión a RabbitMQ finalizada.')
