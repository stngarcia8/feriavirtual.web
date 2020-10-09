from core.models import Profile, Country, City
from transportista.models import VehicleType
from django.core.management.base import BaseCommand


# Command();
# Clase que permite ejecutar comandos personalizados desde manage.py
class Command(BaseCommand):
    help = 'Ingresa valores de prueba para feria virtual.'

    def handle(self, *args, **kwargs):
        self.CrearPerfil()
        self.CrearTiposDeTransportes()
        self.CrearPaisCiudad()
        print('Base de datos poblada para pruebas!')

    # crearPerfil()
    # Metodo para crear los perfiles necesarios para los usuarios.
    def CrearPerfil(self):
        print('Creando roles de usuario.')
        profile = Profile(ProfileID=1, ProfileName='Administrador')
        profile.save()
        profile = Profile(ProfileID=2, ProfileName='Consultor')
        profile.save()
        profile = Profile(ProfileID=3, ProfileName='Cliente externo')
        profile.save()
        profile = Profile(ProfileID=4, ProfileName='Cliente interno')
        profile.save()
        profile = Profile(ProfileID=5, ProfileName='Productor')
        profile.save()
        profile = Profile(ProfileID=6, ProfileName='Transportista')
        profile.save()
        return

    def CrearTiposDeTransportes(self):
        print('Creando tipos de medios de transportes')
        vehicleType = VehicleType(VehicleTypeID=1, VehicleTypeDescription='Aereo')
        vehicleType.save()
        vehicleType = VehicleType(VehicleTypeID=2, VehicleTypeDescription='Terrestre')
        vehicleType.save()
        vehicleType = VehicleType(VehicleTypeID=3, VehicleTypeDescription='Maritimo')
        vehicleType.save()
        return 

    # CrearPaisCiudad()
    # Metodo para crear los paises y las ciudades necesarias para los usuarios.
    def CrearPaisCiudad(self):
        print('Creando paises y ciudades.')
        country = Country(CountryID=1, CountryName='Alemania',
                          CountryPrefix='+54')
        country.save()
        city = City(CityID=1, Country=country, CityName='Berlin')
        city.save()
        city = City(CityID=2, Country=country, CityName='Munich')
        city.save()
        country = Country(
            CountryID=2, CountryName='Argentina', CountryPrefix='+49')
        country.save()
        city = City(CityID=3, Country=country, CityName='Buenos Aires')
        city.save()
        city = City(CityID=4, Country=country, CityName='Cordoba')
        city.save()
        country = Country(
            CountryID=3, CountryName='Australia', CountryPrefix='+61')
        country.save()
        city = City(CityID=5, Country=country, CityName='Sidney')
        city.save()
        city = City(CityID=6, Country=country, CityName='Melbourne')
        city.save()
        city = City(CityID=7, Country=country, CityName='Canberra')
        city.save()
        country = Country(CountryID=4, CountryName='Austria',
                          CountryPrefix='+43')
        country.save()
        city = City(CityID=8, Country=country, CityName='Viena')
        city.save()
        country = Country(CountryID=5, CountryName='Belgica',
                          CountryPrefix='+32')
        country.save()
        city = City(CityID=9, Country=country, CityName='Bruselas')
        city.save()
        city = City(CityID=10, Country=country, CityName='Brujas')
        city.save()
        country = Country(CountryID=6, CountryName='Brasil',
                          CountryPrefix='+55')
        country.save()
        city = City(CityID=11, Country=country, CityName='Brasilia')
        city.save()
        city = City(CityID=12, Country=country, CityName='Rio de janeiro')
        city.save()
        city = City(CityID=13, Country=country, CityName='Sao Paulo')
        city.save()
        country = Country(CountryID=7, CountryName='Bulgaria',
                          CountryPrefix='+359')
        country.save()
        city = City(CityID=14, Country=country, CityName='Sofia')
        city.save()
        country = Country(CountryID=8, CountryName='Canada',
                          CountryPrefix='+1')
        country.save()
        city = City(CityID=15, Country=country, CityName='Ottawa')
        city.save()
        city = City(CityID=16, Country=country, CityName='Toronto')
        city.save()
        city = City(CityID=17, Country=country, CityName='Montreal')
        city.save()
        country = Country(CountryID=9, CountryName='Chile',
                          CountryPrefix='+56')
        country.save()
        city = City(CityID=18, Country=country, CityName='Santiago')
        city.save()
        city = City(CityID=19, Country=country, CityName='Valparaiso')
        city.save()
        city = City(CityID=20, Country=country, CityName='Valdivia')
        city.save()
        city = City(CityID=21, Country=country, CityName='Concepcion')
        city.save()
        country = Country(CountryID=10, CountryName='China',
                          CountryPrefix='+86')
        country.save()
        city = City(CityID=22, Country=country, CityName='Pekin')
        city.save()
        city = City(CityID=23, Country=country, CityName='Shanghai')
        city.save()
        country = Country(
            CountryID=11, CountryName='Colombia', CountryPrefix='+57')
        country.save()
        city = City(CityID=24, Country=country, CityName='Bogota')
        city.save()
        city = City(CityID=25, Country=country, CityName='Medellin')
        city.save()
        country = Country(CountryID=12, CountryName='Croacia',
                          CountryPrefix='+385')
        country.save()
        city = City(CityID=26, Country=country, CityName='Zagreb')
        city.save()
        country = Country(
            CountryID=13, CountryName='Dinamarca', CountryPrefix='+45')
        country.save()
        city = City(CityID=27, Country=country, CityName='Copenhague')
        city.save()
        country = Country(CountryID=14, CountryName='Egipto',
                          CountryPrefix='+20')
        country.save()
        city = City(CityID=28, Country=country, CityName='El cairo')
        city.save()
        country = Country(CountryID=15, CountryName='España',
                          CountryPrefix='+34')
        country.save()
        city = City(CityID=29, Country=country, CityName='Madrid')
        city.save()
        city = City(CityID=30, Country=country, CityName='Barcelona')
        city.save()
        country = Country(CountryID=16, CountryName='Francia',
                          CountryPrefix='+33')
        country.save()
        city = City(CityID=31, Country=country, CityName='Paris')
        city.save()
        country = Country(CountryID=17, CountryName='Grecia',
                          CountryPrefix='+30')
        country.save()
        city = City(CityID=32, Country=country, CityName='Atenas')
        city.save()
        country = Country(CountryID=18, CountryName='Holanda',
                          CountryPrefix='+31')
        country.save()
        city = City(CityID=33, Country=country, CityName='Amsterdam')
        city.save()
        country = Country(CountryID=19, CountryName='India',
                          CountryPrefix='+91')
        country.save()
        city = City(CityID=34, Country=country, CityName='Nueva Delhi')
        city.save()
        city = City(CityID=35, Country=country, CityName='Bombay')
        city.save()
        country = Country(CountryID=20, CountryName='Italia',
                          CountryPrefix='+39')
        country.save()
        city = City(CityID=36, Country=country, CityName='Roma')
        city.save()
        city = City(CityID=37, Country=country, CityName='Milan')
        city.save()
        country = Country(CountryID=21, CountryName='Japon',
                          CountryPrefix='+81')
        country.save()
        city = City(CityID=38, Country=country, CityName='Tokio')
        city.save()
        country = Country(CountryID=22, CountryName='Mexico',
                          CountryPrefix='+52')
        country.save()
        city = City(CityID=39, Country=country, CityName='Ciudad de Mexico')
        city.save()
        city = City(CityID=40, Country=country, CityName='Monterrey')
        city.save()
        country = Country(CountryID=23, CountryName='Noruega',
                          CountryPrefix='+47')
        country.save()
        city = City(CityID=41, Country=country, CityName='Oslo')
        city.save()
        country = Country(CountryID=24, CountryName='Peru',
                          CountryPrefix='+51')
        country.save()
        city = City(CityID=42, Country=country, CityName='Lima')
        city.save()
        country = Country(CountryID=25, CountryName='Portugal',
                          CountryPrefix='+351')
        country.save()
        city = City(CityID=43, Country=country, CityName='Lisboa')
        city.save()
        city = City(CityID=44, Country=country, CityName='Oporto')
        city.save()
        country = Country(CountryID=26, CountryName='Qatar',
                          CountryPrefix='+974')
        country.save()
        city = City(CityID=45, Country=country, CityName='Doha')
        city.save()
        country = Country(CountryID=27, CountryName='Rusia',
                          CountryPrefix='+7')
        country.save()
        city = City(CityID=46, Country=country, CityName='Moscu')
        city.save()
        city = City(CityID=47, Country=country, CityName='San Petersburgo')
        city.save()
        country = Country(
            CountryID=28, CountryName='Reino Unido', CountryPrefix='+44')
        country.save()
        city = City(CityID=48, Country=country, CityName='Londres')
        city.save()
        country = Country(
            CountryID=29, CountryName='Sudafrica', CountryPrefix='+27')
        country.save()
        city = City(CityID=49, Country=country, CityName='Manchester')
        city.save()
        country = Country(CountryID=30, CountryName='Suecia',
                          CountryPrefix='+46')
        country.save()
        city = City(CityID=50, Country=country, CityName='Estocolmo')
        city.save()
        country = Country(CountryID=31, CountryName='Suiza',
                          CountryPrefix='+41')
        country.save()
        city = City(CityID=51, Country=country, CityName='Berna')
        city.save()
        city = City(CityID=52, Country=country, CityName='Zurich')
        city.save()
        country = Country(
            CountryID=32, CountryName='Tailandia', CountryPrefix='+66')
        country.save()
        city = City(CityID=53, Country=country, CityName='Bangkok')
        city.save()
        country = Country(CountryID=33, CountryName='Turquia',
                          CountryPrefix='+90')
        country.save()
        city = City(CityID=54, Country=country, CityName='Ankara')
        city.save()
        city = City(CityID=55, Country=country, CityName='Estambul')
        city.save()
        country = Country(CountryID=34, CountryName='Usa', CountryPrefix='+1')
        country.save()
        city = City(CityID=56, Country=country, CityName='Washington')
        city.save()
        city = City(CityID=57, Country=country, CityName='Los Angeles')
        city.save()
        city = City(CityID=58, Country=country, CityName='New York')
        city.save()
        city = City(CityID=59, Country=country, CityName='Miami')
        city.save()
        country = Country(CountryID=35, CountryName='Uruguay',
                          CountryPrefix='+598')
        country.save()
        city = City(CityID=60, Country=country, CityName='Montevideo')
        city.save()
        country = Country(CountryID=36, CountryName='Vietnam',
                          CountryPrefix='+84')
        country.save()
        city = City(CityID=61, Country=country, CityName='Hanoi')
        city.save()
        return
