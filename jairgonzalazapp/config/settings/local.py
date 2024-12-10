from .base import *
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
import os
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1','*']


# Base de datos para desarrollo


# Configuración de la base de datos


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
# Configuración de correo para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'