from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wmskpl&6giis9se_%6hl#(p^d-5ljas4-d^51@a(ufnzc1wlv+'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: define the correct url in production!
# REDIS_SERVER_URL = "redis://127.0.0.1:6379"

# # managing cache memory (Redis, PyMemcacheCache)
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': REDIS_SERVER_URL + "/chaajaa",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "IGNORE_EXCEPTIONS": True,
#         },
#         "KEY_PREFIX": "chajaa"
#     },
#     'renditions': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
#         'LOCATION': '127.0.0.1:11211',
#         'TIMEOUT': 600,
#         'OPTIONS': {
#             'MAX_ENTRIES': 1000
#         }
#     }
# }


try:
    from .local import *
except ImportError:
    pass
