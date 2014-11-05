# -*- coding: utf-8 -*-
from __future__ import absolute_import
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
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY SETTINGS
#
# Read all important configuration settings from files on root filesystem, not
# included in project directory (so they will be not versioned by GIT).

import json
secret_file = open(os.path.join(BASE_DIR, '.settings', 'secret_kuba.json'), 'r')
config = json.loads(secret_file.read())
secret_file.close()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

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
    #http://docs.celeryproject.org/en/latest/getting-started/brokers/django.html#broker-django
    'kombu.transport.django',
    'djcelery',
    # http://niwibe.github.io/djmail/
    'djmail',
    # https://django-modeltranslation.readthedocs.org/en/latest/
    'modeltranslation',
    # http://django-haystack.readthedocs.org/en/latest/
    'haystack',
    # https://github.com/SmileyChris/easy-thumbnails
    'easy_thumbnails',
    # http://django-mptt.github.io/django-mptt/
    'mptt',
    # http://www.django-rest-framework.org
    'rest_framework',
    'rest_framework.authtoken',
    # https://github.com/ottoyiu/django-cors-headers
    'corsheaders',
    # https://github.com/skorokithakis/django-annoying
    'annoying',
    #'python-social-auth',
    'social.apps.django_app.default',
    # django-activity-stream
    'actstream',
    #http://django-taggit.readthedocs.org/en/latest/
    'taggit',
    # http://django-easy-pdf.readthedocs.org/en/stable/
    'easy_pdf',
    # geodjango
    'django.contrib.gis',
    # Core program modules
    'places_core', # for common templates and static files
    'geonames',    # To, co powinno być w powyższym, tylko dobrze
    'userspace',   # panel użytkownika
    'locations',   # główny moduł obsługujący lokalizacje
    'ideas',       # Pomysły - core funkcjonalności
    'blog',        # sekcja News dla lokacji
    'polls',       # ankiety tworzone przez użytkowników
    'rest',        # out for django rest framework
    'topics',      # custom forum app
    'comments',    # custom comments app (using mptt)
    'gallery',     # user media app
    'south',       # Database migrations
    'maps',        # Custom app for Open Street Maps
    'staticpages', # Statyczne strony
    'civmail',     # Newsletter i obsługa maili
    'articles',    # Statyczne artykuły - support etc.
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
)
TEMPLATE_DIRS = os.path.join(BASE_DIR, 'templates')


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'places_core.middleware.SubdomainMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'places.urls'

WSGI_APPLICATION = 'places.wsgi.application'

# Django messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    50: 'danger',
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config['db_name'],
        'USER': config['db_user'],
        'PASSWORD': config['db_pass'],
        'HOST': config['db_host'],
        'PORT': 5432,
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL   = '/static/'
MEDIA_ROOT   = os.path.join(BASE_DIR, 'media')
MEDIA_URL    = '/media/'

# Haystack - search engine
#-------------------------------------------------------------------------------
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': os.path.join(BASE_DIR, '.settings/xapian_index'),
    },
}

# Social Auth
#-------------------------------------------------------------------------------
# Authentication and python-social-auth settings
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GooglePlusAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/activity/'
LOGOUT_URL = '/user/logout/'
SOCIAL_AUTH_UID_LENGTH = 255
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/places/?new_user=true'
# Custom setting - dla użytkowników Twittera
SOCIAL_AUTH_SET_TWITTER_EMAIL_URL = '/user/twitter_email/'
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'places_core.social_auth.set_twitter_email',
    'places_core.social_auth.validate_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'places_core.social_auth.create_user_profile',
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
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['email-address', 'headline',]
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
    'MODELS': ('auth.user', 'auth.group', 'locations.location', 'ideas.idea',
               'blog.news', 'polls.poll', 'comments.customcomment',
               'topics.discussion', 'userspace.userprofile', 'userspace.badge',
               'gallery.locationgalleryitem', 'topics.entry', 'articles.article'),
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

# REST framework
#-------------------------------------------------------------------------------
# django rest framework
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'per_page',
    'MAX_PAGINATE_BY': 100,
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
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
    ('de', 'Niemiecki'),
    ('pt', 'Português'),
    ('fr', 'Français'),
    ('it', 'Italiano'),
    ('cz', 'Ceština'),
)


# CACHE
#-------------------------------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    },
    'redis': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}


# Email settings
#-------------------------------------------------------------------------------
# Email account settings
EMAIL_HOST          = config['email_host']
EMAIL_PORT          = 587
EMAIL_HOST_USER     = config['email_user']
EMAIL_HOST_PASSWORD = config['email_pass']
EMAIL_USE_TLS       = True
# Enter real email address here in future
EMAIL_DEFAULT_ADDRESS = 'test@composly.com'
DEFAULT_FROM_EMAIL = 'noreply@civilhub.org'

# Email settings for testing purposes
EMAIL_BACKEND       = "djmail.backends.default.EmailBackend"
# Uncomment below line to enable sending real emails.
#DJMAIL_REAL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# Celery/Rabbit i taski
#-------------------------------------------------------------------------------
# Celery task manager settings
BROKER_URL               = 'amqp://guest:guest@localhost:5672//'
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


# Ustawienia dla miniaturek
#-------------------------------------------------------------------------------
# For each of set of size image thumbnals will be generated automatically.
THUMB_SIZES = [
    (30, 30),
    (128, 128),
    (256, 256),
]
# Maximum size for pictures in gallery. Bigger pictures will be thumbnailed.
IMAGE_MAX_SIZE = (1024,1024)
GALLERY_THUMB_SIZE = (270,170)

# Maximum size for location and profile pages background images
BACKGROUND_IMAGE_SIZE = (1920, 300)

# Settings for user avatar pictures
AVATAR_SIZE = (128, 128)
AVATAR_THUMBNAIL_SIZES = [
    (30, 30),
    (60, 60),
    (90, 90),
    (120, 120),
]


# South database migrations schemes
# ------------------------------------------------------------------------------
# http://south.readthedocs.org/en/latest/convertinganapp.html#converting-an-app
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}


# Sanitize input/output
# ------------------------------------------------------------------------------
VALID_TAGS = ['p','i','strong','b','u','a','pre','br','img','hr','ul','ol',]
VALID_ATTRS = ['href','src','width','height','style','target',]
URL_ATTRS = ['href','src',]


# GeoIP settings
#-------------------------------------------------------------------------------
GEOIP_PATH = os.path.join(BASE_DIR, 'geonames', 'data')
GEOIP_COUNTRY = 'GeoIP.dat'
GEOIP_CITY = 'GeoLiteCity.dat'

# Custom module settings
#-------------------------------------------------------------------------------
COUNTRY_STORAGE_PATH = os.path.join(BASE_DIR, 'geobase', 'markers')
DEFAULT_COUNTRY_CODE = 'PL'
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

# Customowe ustawienia dla redisa, wyłącza cache w widokach dla
# wersji developerskiej.
USE_CACHE = False

