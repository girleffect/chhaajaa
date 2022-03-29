from .base import *
import os

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

# SECURITY WARNING: define the correct URL in production!
REDIS_SERVER_URL = os.environ.get('REDIS_SERVER_URL', 'redis://127.0.0.1:6379')
REDIS_CACHE_NAME = os.environ.get('REDIS_CACHE_NAME', 'chaajaa')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_SERVER_URL + "/" + REDIS_CACHE_NAME,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "KEY_PREFIX": "chaajaa"
    },
    'renditions': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 600,
        'OPTIONS': {
            # Uses example options for pymemcached here 
            # https://docs.djangoproject.com/en/3.2/topics/cache/
            'no_delay': True,
            'ignore_exc': True,
            'max_pool_size': 4,
            'use_pooling': True,
        }
    }
}



#Amazon s3 storage settings

# DEFAULT_FILE_STORAGE is configured using DEFAULT_STORAGE_DSN

# read the setting value from the environment variable
DEFAULT_STORAGE_DSN = os.environ.get('DEFAULT_STORAGE_DSN', '')

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')

if DEFAULT_STORAGE_DSN:
    # dsn_configured_storage_class() requires the name of the setting
    DefaultStorageClass = dsn_configured_storage_class('DEFAULT_STORAGE_DSN')

    # Django's DEFAULT_FILE_STORAGE requires the class name
    DEFAULT_FILE_STORAGE = 'chajaa.settings.production.DefaultStorageClass'
    CORS_ORIGIN_WHITELIST.append(
        "https://" + AWS_STORAGE_BUCKET_NAME
    )
else:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_LOCATION = 'static'

AWS_S3_CUSTOM_DOMAIN = '%s.s3-eu-west-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


DATABASES = {
    'default': dj_database_url.config(
        # default=os.environ.get('DATABASE_URL', 'postgres://superuser:spider@123@localhost/chajaa'),
        default=os.environ.get('DATABASE_URL', 'postgres://superuser:spider@123@localhost/chajaa'),
        engine='django.db.backends.postgresql_psycopg2')
 }

try:
    from .local import *
except ImportError:
    pass
