from rest_framework import serializers
from.models import Comercial, City, Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('CountryID', 'CountryName', 'CountryPrefix')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('CityID', 'CityName')


class ComercialSerializer(serializers.ModelSerializer):
    Country = CountrySerializer()
    City = CitySerializer()

    class Meta:
        model = Comercial
        fields = ('ComercialID', 'ClientID', 'CompanyName', 'FantasyName', 'ComercialBusiness',
                  'Email', 'ComercialDNI', 'Address',
                  'City', 'Country', 'PhoneNumber', 'User')
        depth = 1

    def create(self, data):
        id = data['Country']['CountryID']
        country = Country.objects.get(CountryID=id)
        id = data['City']['CityID']
        city = City.objects.get(CityID=id)
        com = Comercial.objects.create(
            ComercialID=data['ComercialID'], ClientID=data['ClientID'],
            CompanyName=data['CompanyName'], FantasyName=data['FantasyName'],
            ComercialBusiness=data['ComercialBusiness'], Email=data['Email'],
            ComercialDNI=data['ComercialDNI'], Address=data['Address'],
            City=city, Country=country, PhoneNumber=data['PhoneNumber'],
            User=data['User']
        )
        return com
    
class ComercialApiSerializer(serializers.ModelSerializer):
    "Almacena los datos para enviarlos a la api feria virtual"
    Country = CountrySerializer()
    City = CitySerializer()

    class Meta:
        model = Comercial
        fields = ('ComercialID', 'ClientID',
                  'CompanyName', 'FantasyName', 'ComercialBusiness',
                  'Email', 'ComercialDNI', 'Address', 'City', 'Country', 'PhoneNumber')
        depth = 1