from .base import *
import os

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

# SECURITY WARNING: define the correct URL in production!
REDIS_SERVER_URL = os.environ.get('REDIS_SERVER_URL', 'redis://127.0.0.1:6379')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_SERVER_URL + "/chaajaa",
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

try:
    from .local import *
except ImportError:
    pass
