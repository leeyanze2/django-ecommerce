# -*- coding: utf-8 -*-
"""
Django settings for generic_ecom project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# This settings files should be further refactored into another file
# But for convenience, I shall leave it as such in the challenge

# possible values are "shoe_shop" and "slipper_shop"
NV_CURRENT_CLIENT = 'shoe_shop'

NV_CLIENT_DETAILS = {}
if NV_CURRENT_CLIENT is 'shoe_shop':
    NV_CLIENT_DETAILS['SHOP_NAME'] = '<Shoe Shop name>'
    NV_CLIENT_DETAILS['DATABASE_NAME'] = 'shoe_shop'
    # Other client specific things that must be here:
    # Deployment related: "SECRET_KEY", "ALLOWED_HOSTS"
    # Client related: Timezone probably

if NV_CURRENT_CLIENT is 'slipper_shop':
    NV_CLIENT_DETAILS['SHOP_NAME'] = '<Slipper Shop name>'
    NV_CLIENT_DETAILS['DATABASE_NAME'] = 'slipper_shop'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x1k93#m)77hbw7256cfm)s+3pt@(dp41p5px*5l%hit%6ha1$2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # external libs
    'rest_framework',
    'enumfields',
    'drf_enum_field',
    'djmoney',
]

# This settings files should be further refactored into another file
# But for convenience, I shall leave it as such in the challenge
# Can probably refactor using https://pypi.python.org/pypi/stringcase
if NV_CURRENT_CLIENT is 'shoe_shop':
    INSTALLED_APPS.append('shoe_shop.apps.ShoeShopConfig')
if NV_CURRENT_CLIENT is 'slipper_shop':
    INSTALLED_APPS.append('slipper_shop.apps.SlipperShopConfig')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # custom middleware
    # 'lib_common.middleware.audit_log.AuditLogMiddleware',
]

ROOT_URLCONF = 'generic_ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'core', 'templates'),
            os.path.join(BASE_DIR, 'lib_common', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'lib_common.context_processors.base_html',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'generic_ecom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': NV_CURRENT_CLIENT,
        'USER': 'root',
        'PASSWORD': 'demodemo',
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

AUTH_USER_MODEL = NV_CURRENT_CLIENT + '.ExtendedUser'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/login/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(funcName)s %(process)d %(thread)d - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'debug': {
            'handlers': ['debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

LANGUAGES = [
    ('en', 'English'),
    ('zh-hans', '中文'),
]

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
