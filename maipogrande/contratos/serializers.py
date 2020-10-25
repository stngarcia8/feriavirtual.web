from rest_framework import serializers
from .models import Contract


class ContratoSerializer(serializers.ModelSerializer):
    "Serializador para los contratos."

    class Meta:
        model = Contract
        fields = ('ContractID', 'ClientID', 'Customername', 'CustomerDNI',
                  'CustomerEmail', 'ContractObservation', 'CustomerObservation',
                  'StartDate', 'EndDate', 'IsValid', 'ValidDescription', 'ContractDescription',
                  'CommisionValue', 'AdditionalValue', 'FineValue',
                  'Status', 'StatusDescription', 'User',)

    def create(self, data):
        "Permite recibir parámetros en el evento save()"
        con = Contract.objects.create(
            ContractID=data['ContractID'], ClientID=data['ClientID'], Customername=data['Customername'],
            CustomerDNI=data['CustomerDNI'], CustomerEmail=data['CustomerEmail'],
            ContractObservation=data['ContractObservation'],
            CustomerObservation=data['CustomerObservation'], StartDate=data['StartDate'],
            EndDate=data['EndDate'], IsValid=data['IsValid'], ValidDescription=data['ValidDescription'],
            ContractDescription=data['ContractDescription'], CommisionValue=data['CommisionValue'],
            AdditionalValue=data['AdditionalValue'], FineValue=data['FineValue'], Status=data['Status'],
            StatusDescription=data['StatusDescription'],
            ProfileID=data['ProfileID'], User=data['User']
        )
        return con


class ContractApiserializer(serializers.ModelSerializer):
    "Serializador para los contratos, permite aceptar o rechazar un contrato."

    class Meta:
        model = Contract
        fields = ('ProfileID', 'ContractID', 'ClientID', 'CustomerObservation', )
