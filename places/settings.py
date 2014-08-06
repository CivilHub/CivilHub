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
DEBUG = True

TEMPLATE_DEBUG = True

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
    # geodjango
    'django.contrib.gis',
    # Core program modules
    'places_core', # for common templates and static files
    'geobase',  # Kraje, języki i wszystko, co powiązane z mapą
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
    #'import_export',
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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # odkomentować na produkcji - wyświetlanie błędów w social_auth
    #'places_core.middleware.SocialAuthExceptionMiddleware',
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    #~ 'default': {
        #~ 'ENGINE': 'django.db.backends.mysql', 
        #~ 'NAME': 'civilhub',
        #~ 'USER': 'grzegorz',
        #~ 'PASSWORD': '',
        #~ 'HOST': '10.0.0.200',   # Or an IP Address that your DB is hosted on
        #~ 'PORT': '3306',
    #~ }
    #~ 'default': {
        #~ 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #~ 'NAME': 'places',                      
        #~ 'USER': 'places',
        #~ 'PASSWORD': '987xyz',
        #~ 'HOST': '188.226.176.9' # civilhub.org
    #~ }
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
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# Social Auth
#-------------------------------------------------------------------------------
# Authentication and python-social-auth settings
AUTHENTICATION_BACKENDS = (
    'social.backends.google.GooglePlusAuth',
    #'social.backends.open_id.OpenIdAuth',
    #'social.backends.google.GoogleOpenId',
    #'social.backends.google.GoogleOAuth2',
    #'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    #'social.backends.twitter.Facebook2OAuth2',
    #'social.backends.yahoo.YahooOpenId',
    'social.backends.linkedin.LinkedinOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/activity/'
LOGOUT_URL = '/user/logout/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'
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
    'social.pipeline.user.user_details'
)

# New Google+ login
SOCIAL_AUTH_GOOGLE_PLUS_KEY = '621695853095-7p2mrjthfvma0rq0loolpoocq6f94577.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'y4xJ9Vr18aQAkhyp8DDkaz5l'

SOCIAL_AUTH_FACEBOOK_KEY = '345201478966829'
SOCIAL_AUTH_FACEBOOK_SECRET = '8581a70916d1946e76135d23c4ca271f'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile', 'user_friends']

SOCIAL_AUTH_TWITTER_KEY = 'OMqEsrvkxHgMuwEs4FZWWkr4q'
SOCIAL_AUTH_TWITTER_SECRET = 'SDlUX3bxzZdjF1quH3VtSDg34XAA8Are8pIU461kVLiRjHn5H8'

SOCIAL_AUTH_LINKEDIN_KEY = '77uveqo8v3tk5v'
SOCIAL_AUTH_LINKEDIN_SECRET = 'PSsrYr0Acg4BdKWM'
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
               'gallery.locationgalleryitem', 'topics.entry'),
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


# Email settings
#-------------------------------------------------------------------------------
# Email account settings
EMAIL_HOST          = 'mail.composly.com'
EMAIL_PORT          = 587
EMAIL_HOST_USER     = 'test@composly.com'
EMAIL_HOST_PASSWORD = 'test11'
EMAIL_USE_TLS       = True
# Enter real email address here in future
EMAIL_DEFAULT_ADDRESS = 'test@composly.com'

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
#-------------------------------------------------------------------------------
# http://south.readthedocs.org/en/latest/convertinganapp.html#converting-an-app
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}


# GeoIP settings
#-------------------------------------------------------------------------------
GEOIP_PATH = os.path.join(BASE_DIR, 'geobase', 'data')
GEOIP_COUNTRY = 'GeoIP.dat'
GEOIP_CITY = 'GeoLiteCity.dat'

# Custom module settings
#-------------------------------------------------------------------------------
COUNTRY_STORAGE_PATH = os.path.join(BASE_DIR, 'geobase', 'markers')
DEFAULT_COUNTRY_CODE = 'PL'
