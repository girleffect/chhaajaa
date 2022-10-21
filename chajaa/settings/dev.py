from .base import *
from dotenv import load_dotenv


env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', "127.0.0.1, ").split(', ')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

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


DATABASES = {
    'default': dj_database_url.config(
        # default=os.environ.get('DATABASE_URL', 'postgres://superuser:spider@123@localhost/chajaa'),
        default=os.environ.get('DATABASE_URL', 'postgres://superuser:spider@123@localhost/chajaa'),
        engine='django.db.backends.postgresql_psycopg2')
 }