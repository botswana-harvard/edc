"""
Django settings for x project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from unipath import Path

BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
GIT_DIR = BASE_DIR.ancestor(1)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')-8xsg3omyyv^jbm5tp=p%!l#)!br+c+6k4e9$(4c3h+&anel+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'edc_base',
    'edc_base',
    'edc_constants',
    'edc_consent',
    'edc_device',
    'edc_appointment',
    'edc_visit_schedule',
    'edc.core.crypto_fields',
    'edc.export',
    'edc.device.sync',
    'edc.subject.registration',
    'edc.core.bhp_variables',
    'edc.lab.lab_clinic_api',
    'edc.core.bhp_content_type_map',
    'edc.entry_meta_data',
    'edc.subject.entry',
    'edc.apps.app_configuration',
    'edc.data_manager',
    'edc.testing',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'edc.urls'

WSGI_APPLICATION = 'edc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
SITE_CODE = '10'
SUBJECT_TYPES = ['test_subject_type']
DEVICE_ID = '10'
SERVER_DEVICE_ID_LIST = [99]
MIDDLEMAN_DEVICE_ID_LIST = []
PROJECT_ROOT = BASE_DIR.ancestor(1)
FIELD_MAX_LENGTH = 'default'
IS_SECURE_DEVICE = True
KEY_PATH = os.path.join(BASE_DIR.ancestor(1), 'test_keys')
KEY_PREFIX = 'user'
ALLOW_MODEL_SERIALIZATION = False
MAX_SUBJECTS = 0
DISPATCH_APP_LABELS = []
