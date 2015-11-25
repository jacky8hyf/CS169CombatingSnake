"""
Django settings for combatingSnake project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1n(=xeh(7%o+k$#2%%+n&-orx7l3nu+9xb6%4!+q$tcsf%4zx-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'ws4redis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'gameStart'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'gameStart.errors.ErrorMiddleware', # Custom error handling by throwing exceptions
)

ROOT_URLCONF = 'combatingSnake.urls'

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

WSGI_APPLICATION = 'combatingSnake.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Yifan removed the following lines because it overrides the configs above
# Parse database configuration from $DATABASE_URL
import dj_database_url
HEROKU_LOCAL = os.environ.get('HEROKU_LOCAL')
HEROKU_SERVER = os.environ.get('HEROKU_SERVER')

if HEROKU_LOCAL:
    DATABASES = {'default': dj_database_url.config(default = 'postgres:///postgres')} # TODO when running locally should set up the database and do HEROKU_LOCAL=true heroku local
elif HEROKU_SERVER: # up on deployment
    DATABASES = {'default': dj_database_url.config()}
else: # django - use sqlite3 # where it goes when python manage.py runserver or heroku local
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Enforces HTTPS
if HEROKU_SERVER:
    SECURE_SSL_REDIRECT = True

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
#STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Add this code to see error logs in the console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

WS4REDIS_SUBSCRIBER = 'gameStart.redis_subscriber.RedisSubscriber'
WEBSOCKET_URL = '/ws/'
REDISCLOUD_URL = os.environ.get('REDISCLOUD_URL')
if REDISCLOUD_URL:
    import re
    mo = re.match("redis://(.*):(.*)@(.*):(.*)", REDISCLOUD_URL)
    if mo:
        WS4REDIS_CONNECTION = {
            'host': mo.group(3),
            'port': mo.group(4),
            # 'db': 17,
            'password': mo.group(2),
        }

SESSION_ID_HEADER = 'HTTP_X_SNAKE_SESSION_ID'
MASTER_KEY_HEADER = 'HTTP_X_SNAKE_MASTER_KEY'
# master key between two apps
MASTER_KEY = os.environ.get('MASTER_KEY')
if not MASTER_KEY:
    MASTER_KEY = "fake_master_key"
CHAT_BACKEND_BASE_URL = os.environ.get('CHAT_BACKEND_BASE_URL')
if not CHAT_BACKEND_BASE_URL:
    CHAT_BACKEND_BASE_URL = "ws://localhost:8081"


MAX_MEMBERS_IN_ROOM = 8
STATUS_PLAYING = 1
STATUS_WAITING = 0
