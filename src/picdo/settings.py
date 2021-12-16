#    This file is part of picdo.

#    picdo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    picdo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with picdo.  If not, see <https://www.gnu.org/licenses/>.

"""
Django settings for picdo project.
"""

import pathlib
import os
import re

# Paths and URLs
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
BASE_DIR = PROJECT_ROOT.parent
MEDIA_ROOT = BASE_DIR / 'media'
TMP_ROOT = BASE_DIR / 'tmp'
STATIC_ROOT = PROJECT_ROOT / 'staticfiles'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'


# Secret key
SECRET_KEY = os.environ.get('picdo_secret_key')
ENVIRONMENT = os.environ.get('picdo_environment')

# Debug Mode
if ENVIRONMENT in ('PRODUCTION', 'STAGING'):
    DEBUG = False
    ALLOWED_HOSTS = ['picdok.herokuapp.com']
    STATICFILES_DIRS = [PROJECT_ROOT / 'static']
else:
    DEBUG = True
    ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.0']


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

WSGI_APPLICATION = 'picdo.wsgi.application'
ROOT_URLCONF = 'picdo.urls'
IGNORABLE_404_URLS = [re.compile(r'favicon\.ico'), re.compile(r'robots\.txt')]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('picdo_db_name'),
        'USER': os.environ.get('picdo_db_user'),
        'PASSWORD': os.environ.get('picdo_db_password'),
        'HOST': os.environ.get('picdo_db_host'),
        'PORT': os.environ.get('picdo_db_port'),
    }
}
CONN_MAX_PAGE = 0
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'

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