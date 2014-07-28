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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c1ahg2n8_qtu36pg+qp7f92&bugk6k2mpm=qh#y@jtzi-(^rl-'

#~ RECAPTCHA_PUBLIC_KEY = '6LdNLPQSAAAAAIUZQ14Atth5VBL45JwN-8_G0BiU'
#~ RECAPTCHA_PRIVATE_KEY = '98dfg6df7g56df6gdfgdfg65JHJH656565GFGFGs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

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
    # https://github.com/ottoyiu/django-cors-headers/
    'corsheaders',
    # http://niwibe.github.io/djmail/
    'djmail',
    # https://django-modeltranslation.readthedocs.org/en/latest/
    'modeltranslation',
    # http://django-haystack.readthedocs.org/en/latest/
    'haystack',
    # https://github.com/praekelt/django-recaptcha
    #'captcha',
    # http://django-generic-bookmarks.readthedocs.org/en/latest
    'bookmarks',
    # https://github.com/SmileyChris/easy-thumbnails
    'easy_thumbnails',
    # http://django-mptt.github.io/django-mptt/
    'mptt',
    # https://github.com/thoas/django-discussions
    # disabled because of problems with south migrations.
    #'discussions',
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
    # Core program modules
    'places_core', # for common templates and static files
    'userspace',# panel użytkownika
    'locations',
    'ideas',     
    'blog',
    'polls',
    'rest',     # out for django rest framework
    'topics',   # custom forum app
    'comments', # custom comments app (using mptt)
    'gallery',  # user media app
    'south',    # Database migrations
    'maps',     # Custom app for Google Maps
    'staticpages', # Statyczne strony
    'civmail',  # Newsletter i obsługa maili
)


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


# Authentication and python-social-auth settings
AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.yahoo.YahooOpenId',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/activity/'
LOGOUT_URL = '/user/logout/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'
# Google API keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '764247090603.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'AIzaSyCxWK_o_FPyxWMn_NUNP4xOqY_NnAmIMkc'


# django-activity-stream settings
ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'auth.group', 'locations.location', 'ideas.idea',
               'blog.news', 'polls.poll', 'comments.customcomment',
               'topics.discussion', 'userspace.userprofile', 'userspace.badge',
               'gallery.locationgalleryitem', 'topics.entry'),
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

# django rest framework
REST_FRAMEWORK = {
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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'rest.disable.DisableCSRF',
)

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
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', 
#        'NAME': 'places',
#        'USER': 'places',
#        'PASSWORD': '987xyz',
#        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#        'PORT': '3306',
#    }
#
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'places',                      
        'USER': 'places',
        'PASSWORD': '987xyz',
        'HOST': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL   = 'http://civilhub.org:8080/static/'
STATIC_ROOT  = '/html/static/'
MEDIA_ROOT   = os.path.join(BASE_DIR, 'media')
MEDIA_URL    = '/media/'


# Email account settings
EMAIL_HOST          = 'mail.composly.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = 'test@composly.com'
EMAIL_HOST_PASSWORD = 'test11'
EMAIL_USE_TLS       = True
# Enter real email address here in future
EMAIL_DEFAULT_ADDRESS = 'test@composly.com'

# Email settings for testing purposes
#EMAIL_BACKEND       = "djmail.backends.default.EmailBackend"
# Uncomment below line to enable sending real emails.
DJMAIL_REAL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


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
# For each of set of size image thumbnals will be generated automatically.
THUMB_SIZES = [
    (30, 30),
    (128, 128),
]
# Maximum size for pictures in gallery. Bigger pictures will be thumbnailed.
IMAGE_MAX_SIZE = (1024,1024)

# Maximum size for location and profile pages background images
BACKGROUND_IMAGE_SIZE = 2080

# Settings for user avatar pictures
AVATAR_SIZE = (128, 128)
AVATAR_THUMBNAIL_SIZES = [
    (30, 30),
    (60, 60),
    (90, 90),
]


# South database migrations schemes
# http://south.readthedocs.org/en/latest/convertinganapp.html#converting-an-app
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
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
