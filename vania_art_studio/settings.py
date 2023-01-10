import cloudinary
import psycopg2
import dj_database_url
import os
from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_ENVIRONMENT = config('APP_ENVIRONMENT')

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', '').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vania_art_studio.account',
    'vania_art_studio.products',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vania_art_studio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'vania_art_studio.wsgi.application'

# Database configuration:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }
}

if APP_ENVIRONMENT == 'Production':
    DATABASE_URL = config('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     # },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files configuration:
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static_files',
)
if APP_ENVIRONMENT == 'Production':
    STATICFILES_STORAGE = config('STATICFILES_STORAGE')

# Media files configuration:
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media_files'
cloudinary.config(
    cloud_name=config('CLOUD_NAME'),
    api_key=config('API_KEY'),
    api_secret=config('API_SECRET')
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'account.AppUser'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/account/login/'
LOGOUT_REDIRECT_URL = '/'

if APP_ENVIRONMENT == 'Production':
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
