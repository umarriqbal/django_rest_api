
from .base import *

MYSQL_USER = 'root'
MYSQL_PWD = '123456'
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'

DATABASES = {
    # Can add multiple DB connections here using same or different engines.
    # Currently added MySQL, Postgres, and Mongo.

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PWD,
        'NAME': 'django_test',
    },
    'pg_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    },
    'mongo_db': {
        'ENGINE': 'djongo',
        'HOST': 'mongodb://127.0.0.1:27017/django_test'
    }
}
