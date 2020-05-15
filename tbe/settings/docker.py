from datetime import timedelta

from .base import *

SECRET_KEY = 'xt84x5_)*o7am2#*1=rckv_gw%b=8_zg!z0e!@i5nxkihngbzs'
DEBUG = True
ALLOWED_HOSTS = []

# Config from rest_framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 1
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

SIMPLE_JWT = {
    'SIGNING_KEY': 'secret_token_docker',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
}
