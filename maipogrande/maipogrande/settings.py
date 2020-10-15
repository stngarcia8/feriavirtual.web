from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@wt_+y+*mx)jz&r2u6p3^65t+8v60(-z3eln@)6e50j7#1#r83'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Permitiendo los host que pueden acceder al programa.
ALLOWED_HOSTS = ['*']

# Definicion de las aplicaciones.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'bootstrapform',
    'core',
    'login',
    'productor',
    'transportista',
    'cinterno',
    'cexterno',
]

# Definiendo los middleware a utilizar.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Definiendo la ruta base de las aplicaciones.
ROOT_URLCONF = 'maipogrande.urls'

# Definiendo los templates a usar
TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
        ],
        },
     },
]

# Definiendo el token de la aplicacion
WSGI_APPLICATION = 'maipogrande.wsgi.application'

# Definiendo coneccion a la base de datos.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'maipogrande.db', }}

# Definiendo los estilos de validacion de las contraseñas.
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# definiendo parametros de localizacion e idiomas
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Definiendo las rutas para los archivos estaticos (js, css e imagenes)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'core/static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Definiendo la busqueda de archivos estaticos
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder')

# Definiendo las ubicaciones para carpeta media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ruta para redireccionamiento
LOGIN_REDIRECT_URL = 'home'

# Definiendo la cantidad de registros por pagina
RECORDS_PER_PAGE = 10

# Definiendo propiedades de los correos
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '4f6dbc1693a95c'
EMAIL_HOST_PASSWORD = 'b4103afb73d3cb'
EMAIL_PORT = '2525'

# Datos de conexion al servidor
SERVER_API_URL = 'http://maipogrande-fv.duckdns.org:8080/api/v1/'
SERVER_HEADERS = {"content-type": "application/json; charset=utf-8", }

# URl de servicios
LOGIN_SERVICE_URL = SERVER_API_URL + 'login/autenticate/post'

# url de datos comerciales
COMERCIAL_SERVICE_URL_POST = SERVER_API_URL + 'ComercialData/post'
COMERCIAL_SERVICE_URL_GET = SERVER_API_URL + 'ComercialData/get'
COMERCIAL_SERVICE_URL_PUT = SERVER_API_URL + 'ComercialData/put'
COMERCIAL_SERVICE_URL_DELETE = SERVER_API_URL + 'ComercialData/delete'

# url de productos
PRODUCTOR_SERVICE_URL_POST = SERVER_API_URL + 'products'
PRODUCTOR_SERVICE_URL_GET_ALL = SERVER_API_URL + 'products/all/get/'
PRODUCTOR_SERVICE_URL_PUT = SERVER_API_URL + 'products'
PRODUCTOR_SERVICE_URL_DELETE = SERVER_API_URL + 'products/delete'

# url de transportista
TRANSPORTISTA_SERVICE_URL_POST = SERVER_API_URL + 'vehicles/post'
TRANSPORTISTA_SERVICE_URL_GET = SERVER_API_URL + 'vehicles/get'
TRANSPORTISTA_SERVICE_URL_PUT = SERVER_API_URL + 'vehicles/put'
TRANSPORTISTA_SERVICE_URL_DELETE = SERVER_API_URL + 'vehicles/delete'
