from rest_framework import serializers

from .models import Contract


class ContratoSerializer(serializers.ModelSerializer):
    "Serializador para los contratos."

    class Meta:
        model = Contract
        fields = ('ContractId', 'ClientId', 'Customername', 'CustomerDni',
                  'CustomerEmail', 'ContractObservation', 'CustomerObservation',
                  'StartDate', 'EndDate', 'IsValid', 'ValidDescription', 'ContractDescription',
                  'CommisionValue', 'AdditionalValue', 'FineValue',
                  'Status', 'StatusDescription', 'User',)

    def create(self, data):
        "Permite recibir parámetros en el evento save()"
        con = Contract.objects.create(
            ContractId=data['ContractId'], ClientId=data['ClientId'], Customername=data['Customername'],
            CustomerDni=data['CustomerDni'], CustomerEmail=data['CustomerEmail'],
            ContractObservation=data['ContractObservation'],
            CustomerObservation=data['CustomerObservation'], StartDate=data['StartDate'],
            EndDate=data['EndDate'], IsValid=data['IsValid'], ValidDescription=data['ValidDescription'],
            ContractDescription=data['ContractDescription'], CommisionValue=data['CommisionValue'],
            AdditionalValue=data['AdditionalValue'], FineValue=data['FineValue'], Status=data['Status'],
            StatusDescription=data['StatusDescription'],
            ProfileId=data['ProfileId'], User=data['User']
        )
        return con


class ContractApiserializer(serializers.ModelSerializer):
    "Serializador para los contratos, permite aceptar o rechazar un contrato."

    class Meta:
        model = Contract
        fields = ('ProfileId', 'ContractId', 'ClientId', 'CustomerObservation', )
