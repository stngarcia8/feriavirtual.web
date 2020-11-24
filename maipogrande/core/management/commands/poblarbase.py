from django.core.management.base import BaseCommand
from dcomercial.models import Profile, Country, City
from ordenes.models import PaymentCondition, PaymentMethod
from productor.models import Category
from transportista.models import VehicleType
from login.models import LoginSession
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Ingresa valores de prueba para feria virtual.'

    def handle(self, *args, **kwargs):
        self.CrearCategorias()
        self.CrearUsuarios()
        self.CrearCondicionesDePago()
        self.CrearMetodosDePago()
        self.CrearPaisCiudad()
        self.CrearPerfil()
        self.CrearTiposDeTransportes()
        print('Base de datos poblada para pruebas!')

    def CrearMetodosDePago(self):
        "Crea los metodos de pago para las ordenes de venta."
        print('Creando metodos de pago.')
        methods = PaymentMethod.objects.all().delete()
        metodo = PaymentMethod(MethodId=1, MethodDescription='VISA')
        metodo.save()
        metodo = PaymentMethod(MethodId=2, MethodDescription='MASTERCARD')
        metodo.save()
        metodo = PaymentMethod(MethodId=3, MethodDescription='TRANSFERENCIA BANCARIA')
        metodo.save()
        metodo = PaymentMethod(MethodId=4, MethodDescription='WEBPAY')
        metodo.save()
        metodo = PaymentMethod(MethodId=5, MethodDescription='PAYPAL')
        metodo.save()
        return



    def CrearCategorias(self):
        "Crea las categorías de los productos."
        print('Creando categorías de productos.')
        categories = Category.objects.all()
        categories.delete()
        category = Category(CategoryId=1, CategoryName='Exportación')
        category.save()
        category = Category(CategoryId=2, CategoryName='Venta nacional')
        category.save()
        return

    def CrearUsuarios(self):
        "Crea los usuarios de ejemplo para pruebas."
        print("Creando usuarios conocidos de pruebas")
        users = User.objects.all().delete()
        user = self.CreaUnUsuario('l.garciar', '552668dcde69cd6c10aebb8e5ee4e61dfb54050a', 'Lolita Garcia Roman', 'stngarcia8@gmail.com')
        self.CreaUnaSesion('5f950227-a59a-48ec-a358-a403ede00bca', 'd124fdef-6956-460f-9873-1953fe29f81b', 6, 'Transportista', user)
        user = self.CreaUnUsuario('f.garciar', '92d52f9c820e4e291318819f2ab5514dd8a389ea', 'Flo Garcia Roman', 'stngarcia8@gmail.com')
        self.CreaUnaSesion('08daae9c-d977-4234-a054-0b83918ed3e7', 'a3220c48-ddb2-4fe8-8e80-8bc832fb80d5', 5, 'Productor', user)
        user = self.CreaUnUsuario('d.garciar', '6f57196fd9309e992379d3c90fec691531219eea', ' Daniela Garcia Roman', 'stngarcia8@gmail.com')
        self.CreaUnaSesion('aa3ed254-ff6d-4c3c-97b6-048efdedaf69', 'd78ee803-2e99-4c87-a684-d600e6540564', 3, 'Cliente externo', user)
        user = self.CreaUnUsuario('l.romanq', '7a4013826e6cbb73d29cbea95ce32abcba60aa6e', 'Loreto Roman Quiroz', 'stngarcia8@gmail.com')
        self.CreaUnaSesion('729d6773-a60c-4dd5-9e39-9629e44c98b2', 'e7d1d546-84ad-4420-bb05-169aebc376a5',4, 'Cliente interno', user)
        return

    def CreaUnUsuario(self, usr, pwd, fname, eml):
        "Crea un usuario en la base de datos temporal."
        u = User.objects.create_user(username=usr, password=pwd,first_name=fname, email=eml)
        uis_staff = True
        u.is_active = True
        u.save()
        return u

    def CreaUnaSesion(self, clId, usrId, proId, proName, usr):
        s = LoginSession()
        s.UserId = usrId
        s.ClientId = clId
        s.Username = usr.username
        s.FullName = usr.first_name
        s.Email = usr.email
        s.ProfileId = proId
        s.ProfileName = proName
        s.User = usr
        s.save()
        return




    def CrearCondicionesDePago(self):
        "Crea las condiciones de pago para las ordenes de venta."
        print('Creando condiciones de pago.')
        conditions = PaymentCondition.objects.all().delete()
        condicion = PaymentCondition(ConditionId=1, ConditionDescription='CONTADO')
        condicion.save()
        condicion= PaymentCondition(ConditionId=2, ConditionDescription='1 MES')
        condicion.save()
        condicion = PaymentCondition(ConditionId=3, ConditionDescription='2 MESES')
        condicion.save()
        condicion = PaymentCondition(ConditionId=4, ConditionDescription='3 MESES')
        condicion.save()
        condicion = PaymentCondition(ConditionId=5, ConditionDescription='4 MESES')
        condicion.save()
        return

    def CrearPerfil(self):
        "Crea los perfiles para los usuarios del sistema."
        print('Creando roles de usuario.')
        profiles = Profile.objects.all().delete()
        profile = Profile(ProfileId=1, ProfileName='Administrador')
        profile.save()
        profile = Profile(ProfileId=2, ProfileName='Consultor')
        profile.save()
        profile = Profile(ProfileId=3, ProfileName='Cliente externo')
        profile.save()
        profile = Profile(ProfileId=4, ProfileName='Cliente interno')
        profile.save()
        profile = Profile(ProfileId=5, ProfileName='Productor')
        profile.save()
        profile = Profile(ProfileId=6, ProfileName='Transportista')
        profile.save()
        return

    def CrearTiposDeTransportes(self):
        "Crea los tipos de medios de transportes para los vehículos."
        print('Creando tipos de medios de transportes')
        vehicleTypes = VehicleType.objects.all().delete()
        vehicleType = VehicleType(VehicleTypeId=1, VehicleTypeDescription='Aereo')
        vehicleType.save()
        vehicleType = VehicleType(VehicleTypeId=2, VehicleTypeDescription='Terrestre')
        vehicleType.save()
        vehicleType = VehicleType(VehicleTypeId=3, VehicleTypeDescription='Maritimo')
        vehicleType.save()
        return

    def CrearPaisCiudad(self):
        "Crea los paises y ciudades necesarios para los datos comerciales de los clientes."
        print('Creando paises y ciudades.')
        countries = Country.objects.all().delete()
        cities = City.objects.all().delete()
        country = Country(CountryId=1, CountryName='Alemania',
                          CountryPrefix='+54')
        country.save()
        city = City(CityId=1, Country=country, CityName='Berlin')
        city.save()
        city = City(CityId=2, Country=country, CityName='Munich')
        city.save()
        country = Country(
            CountryId=2, CountryName='Argentina', CountryPrefix='+49')
        country.save()
        city = City(CityId=3, Country=country, CityName='Buenos Aires')
        city.save()
        city = City(CityId=4, Country=country, CityName='Cordoba')
        city.save()
        country = Country(
            CountryId=3, CountryName='Australia', CountryPrefix='+61')
        country.save()
        city = City(CityId=5, Country=country, CityName='Sidney')
        city.save()
        city = City(CityId=6, Country=country, CityName='Melbourne')
        city.save()
        city = City(CityId=7, Country=country, CityName='Canberra')
        city.save()
        country = Country(CountryId=4, CountryName='Austria',
                          CountryPrefix='+43')
        country.save()
        city = City(CityId=8, Country=country, CityName='Viena')
        city.save()
        country = Country(CountryId=5, CountryName='Belgica',
                          CountryPrefix='+32')
        country.save()
        city = City(CityId=9, Country=country, CityName='Bruselas')
        city.save()
        city = City(CityId=10, Country=country, CityName='Brujas')
        city.save()
        country = Country(CountryId=6, CountryName='Brasil',
                          CountryPrefix='+55')
        country.save()
        city = City(CityId=11, Country=country, CityName='Brasilia')
        city.save()
        city = City(CityId=12, Country=country, CityName='Rio de janeiro')
        city.save()
        city = City(CityId=13, Country=country, CityName='Sao Paulo')
        city.save()
        country = Country(CountryId=7, CountryName='Bulgaria',
                          CountryPrefix='+359')
        country.save()
        city = City(CityId=14, Country=country, CityName='Sofia')
        city.save()
        country = Country(CountryId=8, CountryName='Canada',
                          CountryPrefix='+1')
        country.save()
        city = City(CityId=15, Country=country, CityName='Ottawa')
        city.save()
        city = City(CityId=16, Country=country, CityName='Toronto')
        city.save()
        city = City(CityId=17, Country=country, CityName='Montreal')
        city.save()
        country = Country(CountryId=9, CountryName='Chile',
                          CountryPrefix='+56')
        country.save()
        city = City(CityId=18, Country=country, CityName='Santiago')
        city.save()
        city = City(CityId=19, Country=country, CityName='Valparaiso')
        city.save()
        city = City(CityId=20, Country=country, CityName='Valdivia')
        city.save()
        city = City(CityId=21, Country=country, CityName='Concepcion')
        city.save()
        country = Country(CountryId=10, CountryName='China',
                          CountryPrefix='+86')
        country.save()
        city = City(CityId=22, Country=country, CityName='Pekin')
        city.save()
        city = City(CityId=23, Country=country, CityName='Shanghai')
        city.save()
        country = Country(
            CountryId=11, CountryName='Colombia', CountryPrefix='+57')
        country.save()
        city = City(CityId=24, Country=country, CityName='Bogota')
        city.save()
        city = City(CityId=25, Country=country, CityName='Medellin')
        city.save()
        country = Country(CountryId=12, CountryName='Croacia',
                          CountryPrefix='+385')
        country.save()
        city = City(CityId=26, Country=country, CityName='Zagreb')
        city.save()
        country = Country(
            CountryId=13, CountryName='Dinamarca', CountryPrefix='+45')
        country.save()
        city = City(CityId=27, Country=country, CityName='Copenhague')
        city.save()
        country = Country(CountryId=14, CountryName='Egipto',
                          CountryPrefix='+20')
        country.save()
        city = City(CityId=28, Country=country, CityName='El cairo')
        city.save()
        country = Country(CountryId=15, CountryName='España',
                          CountryPrefix='+34')
        country.save()
        city = City(CityId=29, Country=country, CityName='Madrid')
        city.save()
        city = City(CityId=30, Country=country, CityName='Barcelona')
        city.save()
        country = Country(CountryId=16, CountryName='Francia',
                          CountryPrefix='+33')
        country.save()
        city = City(CityId=31, Country=country, CityName='Paris')
        city.save()
        country = Country(CountryId=17, CountryName='Grecia',
                          CountryPrefix='+30')
        country.save()
        city = City(CityId=32, Country=country, CityName='Atenas')
        city.save()
        country = Country(CountryId=18, CountryName='Holanda',
                          CountryPrefix='+31')
        country.save()
        city = City(CityId=33, Country=country, CityName='Amsterdam')
        city.save()
        country = Country(CountryId=19, CountryName='India',
                          CountryPrefix='+91')
        country.save()
        city = City(CityId=34, Country=country, CityName='Nueva Delhi')
        city.save()
        city = City(CityId=35, Country=country, CityName='Bombay')
        city.save()
        country = Country(CountryId=20, CountryName='Italia',
                          CountryPrefix='+39')
        country.save()
        city = City(CityId=36, Country=country, CityName='Roma')
        city.save()
        city = City(CityId=37, Country=country, CityName='Milan')
        city.save()
        country = Country(CountryId=21, CountryName='Japon',
                          CountryPrefix='+81')
        country.save()
        city = City(CityId=38, Country=country, CityName='Tokio')
        city.save()
        country = Country(CountryId=22, CountryName='Mexico',
                          CountryPrefix='+52')
        country.save()
        city = City(CityId=39, Country=country, CityName='Ciudad de Mexico')
        city.save()
        city = City(CityId=40, Country=country, CityName='Monterrey')
        city.save()
        country = Country(CountryId=23, CountryName='Noruega',
                          CountryPrefix='+47')
        country.save()
        city = City(CityId=41, Country=country, CityName='Oslo')
        city.save()
        country = Country(CountryId=24, CountryName='Peru',
                          CountryPrefix='+51')
        country.save()
        city = City(CityId=42, Country=country, CityName='Lima')
        city.save()
        country = Country(CountryId=25, CountryName='Portugal',
                          CountryPrefix='+351')
        country.save()
        city = City(CityId=43, Country=country, CityName='Lisboa')
        city.save()
        city = City(CityId=44, Country=country, CityName='Oporto')
        city.save()
        country = Country(CountryId=26, CountryName='Qatar',
                          CountryPrefix='+974')
        country.save()
        city = City(CityId=45, Country=country, CityName='Doha')
        city.save()
        country = Country(CountryId=27, CountryName='Rusia',
                          CountryPrefix='+7')
        country.save()
        city = City(CityId=46, Country=country, CityName='Moscu')
        city.save()
        city = City(CityId=47, Country=country, CityName='San Petersburgo')
        city.save()
        country = Country(
            CountryId=28, CountryName='Reino Unido', CountryPrefix='+44')
        country.save()
        city = City(CityId=48, Country=country, CityName='Londres')
        city.save()
        country = Country(
            CountryId=29, CountryName='Sudafrica', CountryPrefix='+27')
        country.save()
        city = City(CityId=49, Country=country, CityName='Manchester')
        city.save()
        country = Country(CountryId=30, CountryName='Suecia',
                          CountryPrefix='+46')
        country.save()
        city = City(CityId=50, Country=country, CityName='Estocolmo')
        city.save()
        country = Country(CountryId=31, CountryName='Suiza',
                          CountryPrefix='+41')
        country.save()
        city = City(CityId=51, Country=country, CityName='Berna')
        city.save()
        city = City(CityId=52, Country=country, CityName='Zurich')
        city.save()
        country = Country(
            CountryId=32, CountryName='Tailandia', CountryPrefix='+66')
        country.save()
        city = City(CityId=53, Country=country, CityName='Bangkok')
        city.save()
        country = Country(CountryId=33, CountryName='Turquia',
                          CountryPrefix='+90')
        country.save()
        city = City(CityId=54, Country=country, CityName='Ankara')
        city.save()
        city = City(CityId=55, Country=country, CityName='Estambul')
        city.save()
        country = Country(CountryId=34, CountryName='Usa', CountryPrefix='+1')
        country.save()
        city = City(CityId=56, Country=country, CityName='Washington')
        city.save()
        city = City(CityId=57, Country=country, CityName='Los Angeles')
        city.save()
        city = City(CityId=58, Country=country, CityName='New York')
        city.save()
        city = City(CityId=59, Country=country, CityName='Miami')
        city.save()
        country = Country(CountryId=35, CountryName='Uruguay',
                          CountryPrefix='+598')
        country.save()
        city = City(CityId=60, Country=country, CityName='Montevideo')
        city.save()
        country = Country(CountryId=36, CountryName='Vietnam',
                          CountryPrefix='+84')
        country.save()
        city = City(CityId=61, Country=country, CityName='Hanoi')
        city.save()
        return
