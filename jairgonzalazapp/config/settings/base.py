from pathlib import Path
from dotenv import load_dotenv
import os
# Construcción de rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv()  # take environment variables from .env.
# Configuraciones básicas
SECRET_KEY = os.getenv('SECRET_KEY')  # En producción, esto vendrá de variables de entorno

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Tus aplicaciones
    'apps.portafolio.apps.PortafolioConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jairgonzalazapp.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jairgonzalazapp.wsgi.application'

# Configuración de internacionalización
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'


#print("BASE_DIR:", BASE_DIR)
#print("STATICFILES_DIRS:", [str(path) for path in STATICFILES_DIRS])
#print("TEMPLATES", TEMPLATES)
# Configuración de archivos media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 
