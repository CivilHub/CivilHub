# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
reload(sys);
sys.setdefaultencoding("utf8")
import os

import djcelery
djcelery.setup_loader()
"""
Django settings for places project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Read all important configuration settings from external file (see README)
import json
secret_file = open(os.path.join(BASE_DIR, 'settings', 'secret.json'), 'r')
config = json.loads(secret_file.read())
secret_file.close()

from . import loggers
LOGGING = loggers.LOGGING

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

INTERNAL_IPS = config['internal_ips']

ALLOWED_HOSTS = config['allowed_hosts']

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # http://django-simple-captcha.readthedocs.org/en/latest
    'captcha',
    # https://bitbucket.org/psam/django-postman
    'postman',
    # http://docs.celeryproject.org/en/latest/getting-started/brokers/django.html#broker-django
    'kombu.transport.django',
    'djcelery',
    # http://niwibe.github.io/djmail/
    'djmail',
    # http://django-haystack.readthedocs.org/en/latest/
    'haystack',
    # http://django-mptt.github.io/django-mptt/
    'mptt',
    # http://www.django-rest-framework.org
    'rest_framework',
    'rest_framework.authtoken',
    # https://github.com/ottoyiu/django-cors-headers
    'corsheaders',
    #'python-social-auth',
    'social.apps.django_app.default',
    #http://django-taggit.readthedocs.org/en/latest/
    'taggit',
    # geodjango
    'django.contrib.gis',
    # http://django-modeltranslation.readthedocs.org/en/latest/
    'modeltranslation',
    # https://github.com/bfirsh/django-ordered-model
    'ordered_model',
    # https://django-debug-toolbar.readthedocs.org/en/
    'debug_toolbar',
    # http://django-filer.readthedocs.org/en/latest/
    'filer',
    'easy_thumbnails',

    # Core program modules
    'places_core', # for common templates and static files
    'geonames',    # Geonames database integration
    'userspace',   # Everything related to users and profiles
    'locations',   # main app module
    'ideas',       #
    'blog',        #
    'polls',       #
    'rest',        # django rest framework
    'topics',      # custom forum app
    'comments',    # custom comments app (using mptt)
    'gallery',     # user media app
    'maps',        # Custom app for Open Street Maps
    'staticpages', #
    'civmail',     # Newsletter and email delivery
    'articles',    # Staticpages with translation support
    'bookmarks',   #
    'projects',    #
    'etherpad',    # Custom Etherpad Lite integration
    'notifications', # Notify users about important events
    'hitcounter',  # Count visits for different content types
    'organizations', # Manage non-governmental organizations (NGO)
    'activities',  # Manage activity streams and different action hooks
    'simpleblog',  # Simplified blog functionality for NGO and projects
    'guides',
    'user_tracker',# Track user activities and statistics

    'raven.contrib.django.raven_compat',
    'analytical',
    # django-activity-stream - have to be last on this list
    'actstream',
)


# Core django settings
#-------------------------------------------------------------------------------
TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'comments.context_processors.ctmap',
    'places_core.context_processors.site_processor',
)
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates'), ]


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_tracker.middleware.VisitorTrackingMiddleware',
    'places_core.middleware.SubdomainMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

if not DEBUG:
    MIDDLEWARE_CLASSES += ('userspace.social_exceptions.CivilAuthExceptionMiddleware',)

ROOT_URLCONF = 'places.urls'

WSGI_APPLICATION = 'places.wsgi.application'

SESSION_COOKIE_DOMAIN = '.civilhub.org'

# Django messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    50: 'danger',
}

POSTGIS_VERSION = (2,1,3)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = config['databases']

# Baza danych do testów
if 'test' in sys.argv:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test.db'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL   = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT   = os.path.join(BASE_DIR, 'media')
MEDIA_URL    = '/media/'


# Haystack - search engine
#-------------------------------------------------------------------------------
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': os.path.join(BASE_DIR, 'settings/xapian_index'),
    },
}


# Postman - wiadomości pomiędzy użytkownikami
#-------------------------------------------------------------------------------
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_DISABLE_USER_EMAILING = False
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_SHOW_USER_AS = lambda u: u.get_full_name()


# Social Auth
#-------------------------------------------------------------------------------
# Authentication and python-social-auth settings
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GooglePlusAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'django.contrib.auth.backends.ModelBackend',
    'userspace.auth_backend.PasswordlessAuthBackend',
)
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/activity/'
LOGOUT_URL = '/user/logout/'
SOCIAL_AUTH_UID_LENGTH = 255
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/user/active/'
# Custom setting - dla użytkowników Twittera
SOCIAL_AUTH_SET_TWITTER_EMAIL_URL = '/user/twitter_email/'
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'places_core.social_auth.get_username',
    'places_core.social_auth.set_twitter_email',
    'places_core.social_auth.validate_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'places_core.social_auth.create_user_profile',
    'places_core.social_auth.get_friends',
    'places_core.social_auth.get_user_avatar',
    'places_core.social_auth.update_user_social_profile',
)
# New Google+ login
SOCIAL_AUTH_GOOGLE_PLUS_KEY = config['google_plus_key']
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = config['google_plus_secret']
SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = ['https://www.googleapis.com/auth/plus.login',
                                 'https://www.googleapis.com/auth/userinfo.email',
                                 'https://www.googleapis.com/auth/userinfo.profile',
                                 'https://www.googleapis.com/auth/plus.profile.emails.read',
                                 'https://www.googleapis.com/auth/plus.me',
                                 'https://www.google.com/m8/feeds',]

SOCIAL_AUTH_FACEBOOK_KEY = config['facebook_key']
SOCIAL_AUTH_FACEBOOK_SECRET = config['facebook_secret']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile', 'user_friends', 'user_birthday']

SOCIAL_AUTH_TWITTER_KEY = config['twitter_key']
SOCIAL_AUTH_TWITTER_SECRET = config['twitter_secret']

SOCIAL_AUTH_LINKEDIN_KEY = config['linkedin_key']
SOCIAL_AUTH_LINKEDIN_SECRET = config['linkedin_secret']
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['email-address', 'headline', 'public-profile-url']
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address'),
                                   ('headline', 'headline'),
                                   ('industry', 'industry')]


# Actstreams
#-------------------------------------------------------------------------------
# django-activity-stream settings
ACTSTREAM_SETTINGS = {
    'MANAGER': 'activities.managers.CivilActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

# REST framework
#-------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'per_page',
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

# CORS settings
# IMPORTANT - Be sure to change this settings in production
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'accept-encoding',
)

# Internationalization
#-------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('en', 'English'),
    ('pl', 'Polski'),
    ('es', 'Español'),
    ('de', 'Deutsch'),
    ('pt', 'Português'),
    ('fr', 'Français'),
)


# CACHE
#-------------------------------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'redis:6379:1',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    },
}


# Email settings
#-------------------------------------------------------------------------------
EMAIL_HOST          = config['email_host']
EMAIL_PORT          = 587
EMAIL_HOST_USER     = config['email_user']
EMAIL_HOST_PASSWORD = str(config['email_pass'])
EMAIL_USE_TLS       = False
# Enter real email address here in future
EMAIL_DEFAULT_ADDRESS = 'noreply@civilhub-mail.org'
DEFAULT_FROM_EMAIL = 'noreply@civilhub-mail.org'
# Where to redirect contact messages
CONTACT_EMAIL_ADDRESS = 'office@civilhub.org'

# Email settings for testing purposes
EMAIL_BACKEND       = "djmail.backends.default.EmailBackend"
# Uncomment below line to enable sending real emails.
DJMAIL_REAL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# Celery/Rabbit i taski
#-------------------------------------------------------------------------------
BROKER_URL               = 'amqp://guest:guest@rabbit:5672//'
CELERY_TASK_SERIALIZER   = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT    = ['json']
CELERY_TIMEZONE          = 'Europe/Warsaw'
CELERY_ENABLE_UTC        = True
CELERY_RESULT_BACKEND    = 'djcelery.backends.database:DatabaseBackend'
# Uncomment following line to enable django caching system for Celery. Remember
# to comment out above backend declaration used for development.
#CELERY_RESULT_BACKEND   = 'djcelery.backends.cache:CacheBackend'
CELERY_IMPORTS = ('places_core.tasks',)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"


COMMENT_EMAIL_NOTIFY = False


# Ustawienia dla miniaturek
#-------------------------------------------------------------------------------
DEFAULT_IMG_PATH = "img/item.png"
# "Standardowe" pole z obrazkiem (Idea, News, Poll, Discussion)
DEFAULT_IMG_SIZE = (680, 680)
DEFAULT_THUMB_SIZE = (430, 142)
# For each of set of size image thumbnals will be generated automatically.
THUMB_SIZES = [
    (30, 30),
    (128, 128),
    (256, 256),
]
# Maximum size for pictures in gallery. Bigger pictures will be thumbnailed.
IMAGE_MAX_SIZE = (1024,1024)
GALLERY_THUMB_SIZE = (270,170)

# Sizes for thumbnails related to ContentObjectGalleries
CO_THUMB_SIZES = {
    'BIG': (680, 425),
    'SMALL': (60, 60),
}

# Maximum size for location and profile pages background images
BACKGROUND_IMAGE_SIZE = (1920, 300)
# Settings for user avatar pictures
AVATAR_SIZE = (260, 260) #(128, 128)
AVATAR_THUMBNAIL_SIZES = [
    #(30, 30),
    #(60, 60),
    #(90, 90),
    #(120, 120),
    (100, 100),
]

# GeoIP settings
#-------------------------------------------------------------------------------
GEOIP_PATH = os.path.join(BASE_DIR, 'geonames', 'data')
GEOIP_COUNTRY = 'GeoIP.dat'
GEOIP_CITY = 'GeoLiteCity.dat'

# Sanitize input/output
# ------------------------------------------------------------------------------
VALID_TAGS = ['p','i','strong','b','u','a','pre','br','img','hr','ul','ol',]
VALID_ATTRS = ['href','src','width','height','style','target',]
URL_ATTRS = ['href','src',]

# Custom module settings
#-------------------------------------------------------------------------------
DEFAULT_COUNTRY_CODE = 'US'
# Limit paginatora dla widoków list (lista dyskusji, ankiet etc.)
LIST_PAGINATION_LIMIT = 50
# Limit paginatora dla innych widoków (lista pomysłów, blog etc.)
PAGE_PAGINATION_LIMIT = 5
# Limit paginatora dla actstreamu dla usera (w zamierzeniu dla wszystkich)
STREAM_PAGINATOR_LIMIT = 25
# Limit paginatora dla obrazów w galerii użytkownika
USER_GALLERY_LIMIT = 12
# Limit paginatora dla obrazów w galerii lokalizacji
PLACE_GALLERY_LIMIT = 12
# Limit paginatora dla komentarzy
COMMENT_PAGINATOR_LIMIT = 10

# Customowe ustawienia dla redisa, wyłącza cache w widokach dla
# wersji developerskiej.
USE_CACHE = True

# Etherpad Lite server

ETHERPAD_API_KEY = config['etherpad']['apikey']
# This is url used by Django to communicate with etherpad server
ETHERPAD_INTERNAL_URL = 'https://civilhub.org:9001'
# This will be usually the same as above unless your setup depends for example
# on different Docker containers. In such case address used by iframes and
# generally front-end may be different.
ETHERPAD_EXTERNAL_URL = 'https://civilhub.org:9001'


RAVEN_CONFIG = {
    'dsn': config['raven_dsn']
}

#Analitical
CLICKY_SITE_ID = config['clicky_site_id']

