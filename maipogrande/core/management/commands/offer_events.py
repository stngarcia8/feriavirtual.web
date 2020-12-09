from productor.models import Producto
from cinterno.serializers import OfferSerializer, OfferDetailSerializer
from cinterno.models import Offer 

class OfferEvents(object):
    "Procesa los eventos asociados a las ofertas."
    evento = ''
    json_data = ''

    def __init__(self, evento, json_data):
        self.evento = evento
        self.json_data = json_data

    def event_executor(self):
        if self.evento == 'NEWOFFER':
            self.__crear_ofertas(self.json_data)
        elif  self.evento == 'UPDATEOFFER':
            self.__actualizar_ofertas(self.json_data)
        elif self.evento == 'DELETEOFFER':
            self.__eliminar_ofertas(self.json_data)    
        elif self.evento == 'ENABLEOFFER':
            self.__Habilitar_ofertas(self.json_data)    
        elif self.evento == 'DISABLEOFFER':
            self.__Inhabilitar_ofertas(self.json_data)    


    def __crear_ofertas(self, json_data):
        "Crea una nueva oferta de productos en la base de datos."
        try:
            oferta = OfferSerializer(data=json_data)
            oferta.is_valid()
            oferta.save()
            print("La oferta  {0} fue creada.".format(json_data['Description']))
        except Exception:
            print("No fue posible crear la oferta {0} .".format(json_data['Description']))
        return

    def __actualizar_ofertas(self, json_data):
        "Crea una nueva oferta de productos en la base de datos."
        try:
            Offer.objects.get(OfferId=json_data['OfferId']).delete()
            oferta = OfferSerializer(data=json_data)
            oferta.is_valid()
            oferta.save()
            print("La oferta  {0} fue actualizada.".format(json_data['Description']))
        except Exception:
            print("No fue posible actualizar la oferta {0} .".format(json_data['Description']))
        return


    def __eliminar_ofertas(self, json_data):
        "Elimina una oferta de productos en la base de datos."
        try:
            oferta = Offer.objects.get(OfferId=json_data['Id']).delete()
            print("La oferta con id {0} fue eliminada.".format(json_data['Id']))
        except Exception:
            print("noNo fue posible eliminar la oferta con id {0}.".format(json_data['Id']))
        return


    def __Habilitar_ofertas(self, json_data):
        "habilita una oferta en la base de datos."
        try:
            oferta = Offer.objects.get(OfferId=json_data['Id'])
            oferta.Status = 1
            oferta.StatusDescription = 'Disponible'
            oferta.save()
            print("La oferta con id {0} ha sido habilitada.".format(json_data['Id']))
        except Exception:
            print("La oferta con id {0} no ha sido habilitada.".format(json_data['Id']))
        return

    def __Inhabilitar_ofertas(self, json_data):
        "habilita una oferta en la base de datos."
        try:
            oferta = Offer.objects.get(OfferId=json_data['Id'])
            oferta.Status = 2
            oferta.StatusDescription = 'Cerrada'
            oferta.save()
            print("La oferta con id {0} ha sido inhabilitada.".format(json_data['Id']))
        except Exception:
            print("La oferta con id {0} no ha sido inhabilitada.".format(json_data['Id']))
        return