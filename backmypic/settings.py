"""
Django settings for backmypic project.
"""

import json
import os
from pathlib import Path
import re

from django.core.exceptions import ImproperlyConfigured

# Paths and URLs
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'
TMP_ROOT = BASE_DIR / 'tmp'

PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = PROJECT_ROOT / 'staticfiles'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'


# loading secret settings (secret key, db password)
with open(BASE_DIR / 'secrets.json', 'r') as file:
    secrets = json.load(file)

def get_secret_setting(setting, secrets=secrets):
    """ Get secret setting or fail with ImproperlyConfigured """
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


# Secret key
SECRET_KEY = get_secret_setting('SECRET_KEY')


# Debug Mode
if os.environ.get('ENV') == 'PRODUCTION':
    DEBUG = False
else:
    DEBUG = True


# HTTP
ALLOWED_HOSTS = ['localhost', 'backmypic.herokuapp.com']
IGNORABLE_404_URLS = [re.compile(r'favicon\.ico'), re.compile(r'robots\.txt')]


# Applications and middlewares
INSTALLED_APPS = [
    'gallery.apps.GalleryConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'sass_processor',
    'django.contrib.postgres'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

WSGI_APPLICATION = 'backmypic.wsgi.application'
ROOT_URLCONF = 'backmypic.urls'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gallery',
        'USER': 'postgres',
        'PASSWORD': get_secret_setting('DB_PASSWORD'),
        'HOST': '',
        'PORT': '5432',
    },
    'old': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Etc/GMT-1'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files and templates
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]

if os.environ.get('ENV') == 'PRODUCTION':
    STATICFILES_DIRS = [
        PROJECT_ROOT / 'static'
    ]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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